const { test } = require("node:test");
const assert = require("node:assert/strict");
const { createHmac } = require("node:crypto");
const { createApp, loadConfig, TEST_REPLY } = require("../index");

const NOW = Date.parse("2026-10-14T18:00:00Z");
const base = { VERIFY_TOKEN: "unit-test-verify-secret", META_APP_SECRET: "unit-test-app-secret" };
const testEnv = {
  ...base, REPLY_MODE: "test", WHATSAPP_TOKEN: "unit-test-access-secret", PHONE_NUMBER_ID: "123456",
  GRAPH_API_VERSION: "v26.0", TEST_ALLOWED_NUMBERS: "971500000001,971500000002",
  TEST_MODE_EXPIRES_AT: "2026-10-14T18:30:00Z",
};
const msg = (id = "message-1", overrides = {}) => ({
  id, from: "971500000001", timestamp: String(NOW / 1000), type: "text", text: { body: "JARVIS TEST" }, ...overrides,
});
const payload = (messages = [msg()], phoneId = "123456") => ({
  object: "whatsapp_business_account", entry: [{ changes: [{ field: "messages", value: {
    metadata: { phone_number_id: phoneId }, messages,
  } }] }],
});

async function fixture(t, env = base, post) {
  const logs = [], calls = [];
  let time = NOW;
  const app = createApp({ config: loadConfig(env, NOW), now: () => time,
    logger: line => logs.push(JSON.parse(line)), http: { post: async (...args) => { calls.push(args); return post?.(...args); } },
  });
  const server = app.listen(0, "127.0.0.1");
  await new Promise(resolve => server.once("listening", resolve));
  t.after(() => new Promise(resolve => { server.close(resolve); server.closeAllConnections(); }));
  const url = `http://127.0.0.1:${server.address().port}`;
  return { logs, calls, url, setTime: value => { time = value; },
    send: async (body = payload(), signature) => {
      const raw = typeof body === "string" ? body : JSON.stringify(body);
      const signed = "sha256=" + createHmac("sha256", base.META_APP_SECRET).update(raw).digest("hex");
      return fetch(url + "/webhook", { method: "POST", headers: {
        "Content-Type": "application/json", ...(signature === null ? {} : { "X-Hub-Signature-256": signature ?? signed }),
      }, body: raw });
    },
  };
}

test("configuration fails closed; only off/test supported; test requires a bounded expiry and exact allowlist", () => {
  assert.equal(loadConfig(base, NOW).replyMode, "off");
  for (const env of [{}, { ...base, META_APP_SECRET: "" }, { ...base, REPLY_MODE: "live" },
    { ...base, REPLY_MODE: "true" }, { ...base, REPLY_MODE: "test" },
    { ...testEnv, TEST_ALLOWED_NUMBERS: "" }, { ...testEnv, TEST_ALLOWED_NUMBERS: "+971500000001" },
    { ...testEnv, TEST_MODE_EXPIRES_AT: "2026-10-14T18:30:00" },
    { ...testEnv, TEST_MODE_EXPIRES_AT: "2026-10-14T17:00:00Z" },
    { ...testEnv, TEST_MODE_EXPIRES_AT: "2026-10-15T18:00:00Z" }]) assert.throws(() => loadConfig(env, NOW));
});

test("GET verification requires mode, configured token and challenge; never logs query secrets", async t => {
  const f = await fixture(t);
  const correct = new URLSearchParams({ "hub.mode": "subscribe", "hub.verify_token": base.VERIFY_TOKEN, "hub.challenge": "4567" });
  const response = await fetch(f.url + "/webhook?" + correct);
  assert.equal(response.status, 200); assert.equal(await response.text(), "4567");
  for (const query of ["hub.verify_token=vedasvision2024&hub.challenge=123", "hub.mode=subscribe&hub.challenge=123", "hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=123", "hub.mode=unsubscribe&hub.verify_token=" + base.VERIFY_TOKEN + "&hub.challenge=123", "hub.mode=subscribe&hub.verify_token=" + base.VERIFY_TOKEN]) {
    assert.equal((await fetch(f.url + "/webhook?" + query)).status, 403);
  }
  assert.ok(!JSON.stringify(f.logs).includes(base.VERIFY_TOKEN));
});

test("unsigned, invalid, tampered, malformed and oversized requests cannot send messages", async t => {
  const f = await fixture(t, testEnv);
  for (const signature of [null, "invalid", "sha256=" + "0".repeat(64)]) assert.equal((await f.send(payload(), signature)).status, 401);
  const signedOriginal = "sha256=" + createHmac("sha256", base.META_APP_SECRET).update(JSON.stringify(payload())).digest("hex");
  assert.equal((await f.send(payload([msg("changed")]), signedOriginal)).status, 401);
  assert.equal((await f.send("{bad json")).status, 400);
  assert.equal((await f.send("x".repeat(270000))).status, 413);
  assert.equal(f.calls.length, 0);
});

test("default off acknowledges batched messages and statuses with zero outbound calls or sensitive logs", async t => {
  const f = await fixture(t);
  const data = payload([msg("private-message-id", { text: { body: "confidential client text" } })]);
  data.entry.push(...payload([msg("second")]).entry);
  data.entry[0].changes[0].value.statuses = [{ id: "private-status-id", status: "delivered" }];
  assert.equal((await f.send(data)).status, 200);
  assert.equal(f.calls.length, 0);
  const event = f.logs.find(x => x.event === "webhook_received");
  assert.equal(event.messages, 2); assert.equal(event.statuses, 1);
  for (const secret of ["confidential client text", "971500000001", "private-message-id", "private-status-id", base.META_APP_SECRET]) assert.ok(!JSON.stringify(f.logs).includes(secret));
});

test("test mode requires allowlist, correct phone id, fresh text command, and message id", async t => {
  const f = await fixture(t, testEnv);
  for (const m of [msg("a", { from: "971599999999" }), msg("b", { type: "image" }), msg("c", { text: { body: "hello" } }),
    msg("d", { timestamp: "0" }), msg("e", { timestamp: String(NOW / 1000 + 60) }), msg("", {}), null]) {
    assert.equal((await f.send(payload([m]))).status, 200);
  }
  await f.send(payload([msg()], "999999"));
  await f.send(payload([]));
  await f.send({ object: "other" });
  await f.send({ object: "whatsapp_business_account", entry: [null, { changes: [null] }] });
  assert.equal(f.calls.length, 0);
  assert.equal((await f.send()).status, 200);
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0][0], "https://graph.facebook.com/v26.0/123456/messages");
  assert.equal(f.calls[0][1].text.body, TEST_REPLY);
  assert.equal(f.calls[0][1].to, "971500000001");
  assert.equal(f.calls[0][2].timeout, 5000);
  assert.ok(f.logs.some(x => x.event === "test_reply_accepted"));
});

test("duplicate deliveries including concurrent ones send once", async t => {
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const f = await fixture(t, testEnv, () => gate);
  const first = f.send();
  while (!f.calls.length) await new Promise(resolve => setImmediate(resolve));
  assert.equal((await f.send()).status, 200);
  release();
  await first;
  await f.send();
  assert.equal(f.calls.length, 1);
});

test("test mode processes multiple entries while status-only callbacks never trigger sends", async t => {
  const f = await fixture(t, testEnv);
  const data = payload();
  data.entry.push(...payload([msg("second", { from: "971500000002" })]).entry);
  assert.equal((await f.send(data)).status, 200);
  assert.equal(f.calls.length, 2);
  const status = payload([]);
  status.entry[0].changes[0].value.statuses = [{ status: "delivered" }];
  await f.send(status);
  assert.equal(f.calls.length, 2);
});

test("cooldown, five-attempt budget, and expiry prevent further sends", async t => {
  const f = await fixture(t, testEnv);
  await f.send();
  await f.send(payload([msg("cooldown")]));
  assert.equal(f.calls.length, 1);
  for (let i = 1; i <= 5; i++) {
    f.setTime(NOW + i * 61000);
    await f.send(payload([msg(`budget-${i}`, { timestamp: String((NOW + i * 61000) / 1000) })]));
  }
  assert.equal(f.calls.length, 5);
  assert.ok(f.logs.some(x => x.reason === "test_budget_exhausted"));
  f.setTime(NOW + 1800000);
  await f.send(payload([msg("expired", { timestamp: String((NOW + 1800000) / 1000) })]));
  assert.ok(f.logs.some(x => x.reason === "test_expired"));
  assert.equal(f.calls.length, 5);
});

test("provider errors/timeouts are acknowledged, redacted and never automatically retried", async t => {
  const f = await fixture(t, testEnv, () => { throw Object.assign(new Error("secret token and client data"), { response: { status: 401, data: "secret body" } }); });
  assert.equal((await f.send()).status, 200);
  await f.send();
  assert.equal(f.calls.length, 1);
  assert.ok(f.logs.some(x => x.event === "test_reply_failed" && x.provider_status === 401));
  assert.ok(!JSON.stringify(f.logs).includes("secret token"));
  assert.ok(!JSON.stringify(f.logs).includes("secret body"));
});
