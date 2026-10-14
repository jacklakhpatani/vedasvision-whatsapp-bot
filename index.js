const express = require("express");
const axios = require("axios");
const { createHmac, timingSafeEqual, randomUUID } = require("node:crypto");

const TEST_REPLY = "JARVIS controlled test successful. Automatic client replies are disabled.";
const list = (value) => Array.isArray(value) ? value : [];

function loadConfig(env = process.env, now = Date.now()) {
  const required = (key) => {
    if (!env[key]?.trim()) throw new Error(`Missing required environment variable: ${key}`);
    return env[key].trim();
  };
  const config = {
    verifyToken: required("VERIFY_TOKEN"),
    appSecret: required("META_APP_SECRET"),
    replyMode: env.REPLY_MODE ?? "off",
    allowedNumbers: new Set(),
  };
  if (!["off", "test"].includes(config.replyMode)) {
    throw new Error("REPLY_MODE must be off or test; unrestricted replies are not supported");
  }
  if (config.replyMode === "test") {
    config.whatsappToken = required("WHATSAPP_TOKEN");
    config.phoneNumberId = required("PHONE_NUMBER_ID");
    config.graphVersion = required("GRAPH_API_VERSION");
    config.allowedNumbers = new Set(required("TEST_ALLOWED_NUMBERS").split(",").map(n => n.trim()));
    const expiry = required("TEST_MODE_EXPIRES_AT");
    if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(expiry)) {
      throw new Error("TEST_MODE_EXPIRES_AT must include an ISO date/time and timezone (Z or +04:00)");
    }
    config.testExpiresAt = Date.parse(expiry);
    if (!/^\d+$/.test(config.phoneNumberId) || !/^v\d+\.0$/.test(config.graphVersion)) {
      throw new Error("Invalid PHONE_NUMBER_ID or GRAPH_API_VERSION format");
    }
    if ([...config.allowedNumbers].some(n => !/^[1-9]\d{7,14}$/.test(n))) {
      throw new Error("TEST_ALLOWED_NUMBERS must contain international digits only, without + or spaces");
    }
    if (!Number.isFinite(config.testExpiresAt) || config.testExpiresAt <= now || config.testExpiresAt > now + 3600000) {
      throw new Error("TEST_MODE_EXPIRES_AT must be a future ISO date within one hour");
    }
  }
  return config;
}

function validSignature(body, signature, secret) {
  if (!Buffer.isBuffer(body) || typeof signature !== "string" || !/^sha256=[a-fA-F0-9]{64}$/.test(signature)) return false;
  const expected = createHmac("sha256", secret).update(body).digest();
  return timingSafeEqual(expected, Buffer.from(signature.slice(7), "hex"));
}

function createApp({ config = loadConfig(), http = axios, now = Date.now, logger = console.log } = {}) {
  const app = express();
  app.disable("x-powered-by");
  const log = (event, details = {}) => logger(JSON.stringify({ time: new Date(now()).toISOString(), event, ...details }));
  // Bounded, process-local safeguards for a single-instance controlled test only.
  const seen = new Map();
  const lastAttempt = new Map();
  let attempts = 0;
  app.use((req, res, next) => {
    req.requestId = randomUUID();
    const start = now();
    const route = req.path === "/webhook" ? "/webhook" : req.path === "/health" ? "/health" : "other";
    log("request_received", { request_id: req.requestId, method: req.method, route });
    res.on("finish", () => log("request_completed", {
      request_id: req.requestId, status: res.statusCode, duration_ms: now() - start,
    }));
    next();
  });
  app.get("/health", (req, res) => res.json({ status: "ok" }));
  app.get("/webhook", (req, res) => {
    const token = req.query["hub.verify_token"];
    const challenge = req.query["hub.challenge"];
    const matches = typeof token === "string" && Buffer.byteLength(token) === Buffer.byteLength(config.verifyToken)
      && timingSafeEqual(Buffer.from(token), Buffer.from(config.verifyToken));
    if (req.query["hub.mode"] !== "subscribe" || typeof challenge !== "string" || !challenge || !matches) {
      log("verification_rejected", { request_id: req.requestId });
      return res.sendStatus(403);
    }
    log("verification_succeeded", { request_id: req.requestId });
    return res.status(200).type("text/plain").send(challenge);
  });

  app.post("/webhook", express.raw({ type: "application/json", limit: "256kb", inflate: false }), async (req, res) => {
    const context = { request_id: req.requestId };
    if (!validSignature(req.body, req.get("x-hub-signature-256"), config.appSecret)) {
      log("signature_rejected", context);
      return res.sendStatus(401);
    }
    let body;
    try { body = JSON.parse(req.body.toString("utf8")); }
    catch { log("invalid_json", context); return res.sendStatus(400); }
    if (body?.object !== "whatsapp_business_account") {
      log("webhook_ignored", { ...context, reason: "unsupported_object" });
      return res.sendStatus(200);
    }
    const messages = [];
    let statuses = 0;
    for (const entry of list(body.entry)) {
      for (const change of list(entry?.changes)) {
        if (change?.field !== "messages") continue;
        const value = change.value;
        statuses += list(value?.statuses).length;
        for (const message of list(value?.messages)) messages.push({ message, phoneId: value?.metadata?.phone_number_id });
      }
    }
    log("webhook_received", { ...context, messages: messages.length, statuses, reply_mode: config.replyMode });
    for (const { message, phoneId } of messages) {
      const skip = reason => log("reply_skipped", { ...context, reason });
      if (config.replyMode === "off") { skip("replies_disabled"); continue; }
      if (now() >= config.testExpiresAt) { skip("test_expired"); continue; }
      if (phoneId !== config.phoneNumberId) { skip("phone_number_mismatch"); continue; }
      if (!config.allowedNumbers.has(message?.from)) { skip("sender_not_allowed"); continue; }
      if (message.type !== "text" || message.text?.body !== "JARVIS TEST") { skip("test_command_required"); continue; }
      const sentAt = Number(message.timestamp) * 1000;
      if (!Number.isFinite(sentAt) || sentAt > now() + 30000 || now() - sentAt > 300000) { skip("stale_or_invalid_timestamp"); continue; }
      if (typeof message.id !== "string" || !message.id || message.id.length > 512) { skip("invalid_message_id"); continue; }
      for (const [id, expires] of seen) if (expires <= now()) seen.delete(id);
      if (seen.has(message.id)) { skip("duplicate_message"); continue; }
      if (seen.size >= 10000) { skip("dedup_capacity"); continue; }
      // Reserve before awaiting a provider; failures/unknown outcomes are never automatically retried.
      seen.set(message.id, now() + 7 * 86400000);
      if (attempts >= 5) { skip("test_budget_exhausted"); continue; }
      if (lastAttempt.has(message.from) && now() - lastAttempt.get(message.from) < 60000) { skip("test_cooldown"); continue; }
      attempts++;
      lastAttempt.set(message.from, now());
      log("test_reply_attempted", context);
      try {
        await http.post(`https://graph.facebook.com/${config.graphVersion}/${config.phoneNumberId}/messages`, {
          messaging_product: "whatsapp", to: message.from, type: "text", text: { body: TEST_REPLY },
        }, {
          headers: { Authorization: `Bearer ${config.whatsappToken}`, "Content-Type": "application/json" },
          timeout: 5000, maxRedirects: 0,
        });
        log("test_reply_accepted", context);
      } catch (error) {
        // Provider errors can contain tokens, phone numbers and message bodies. Never serialize them.
        log("test_reply_failed", { ...context, provider_status: Number.isInteger(error.response?.status) ? error.response.status : null });
      }
    }
    // No AI calls, customer replies, background jobs, or outbound retries in this release.
    return res.sendStatus(200);
  });
  app.use((error, req, res, next) => {
    log("request_rejected", { request_id: req.requestId, reason: error.type === "entity.too.large" ? "body_too_large" : "invalid_request" });
    res.sendStatus(error.status === 413 ? 413 : 400);
  });
  return app;
}

if (require.main === module) {
  try {
    const config = loadConfig();
    createApp({ config }).listen(process.env.PORT || 3000, "0.0.0.0", () => {
      console.log(JSON.stringify({ event: "service_started", reply_mode: config.replyMode, test_expires_at: config.testExpiresAt ? new Date(config.testExpiresAt).toISOString() : null }));
    });
  } catch (error) {
    console.error(JSON.stringify({ event: "startup_failed", reason: error.message }));
    process.exitCode = 1;
  }
}

module.exports = { createApp, loadConfig, validSignature, TEST_REPLY };
