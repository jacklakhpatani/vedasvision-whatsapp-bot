# JARVIS / Vedas Vision WhatsApp webhook

Authenticated receive-only webhook and short, allowlisted connectivity tests. **Automatic client replies are disabled by default; unrestricted reply mode is unavailable.** This release replaces the previous automatic GPT-4 path with a fixed test confirmation. No message is sent to OpenAI; existing `OPENAI_API_KEY` is unused.

## Render setup

Keep the existing Render service, GitHub integration, build command, `node index.js` / `npm start`, `PORT` and `/webhook` callback path. No hosting migration or new service is required. Follow [the exact Render/Meta rollout guide](docs/RENDER_META_SETUP.md). Set secrets before merging/deploying: missing `VERIFY_TOKEN` or `META_APP_SECRET` causes startup to fail. The old hard-coded verification token has no fallback.

## Modes

| Setting | Behavior |
| --- | --- |
| `REPLY_MODE=off` (default) | Authenticate and acknowledge events, log redacted counts and skip reasons, make zero outbound API calls. |
| `REPLY_MODE=test` | Only a fresh text exactly equal to `JARVIS TEST` from an exact allowlisted sender for the configured business phone ID receives a fixed confirmation. |
| Anything else | Startup fails; there is no unrestricted AI mode. |

Test mode requires `WHATSAPP_TOKEN`, `PHONE_NUMBER_ID`, `GRAPH_API_VERSION`, `TEST_ALLOWED_NUMBERS` (comma-separated international digits without `+`), and `TEST_MODE_EXPIRES_AT` (future ISO time, within one hour at startup). Sending stops at expiry. An expired test configuration fails on restart; use `REPLY_MODE=off` to restore receive-only operation.

At most five attempts per process and one per sender per minute. Messages must be no older than five minutes, with 30-second future clock tolerance. IDs are reserved before sending. Failed/ambiguous provider requests are acknowledged without automatic resend because a timed-out send may already have delivered. Each outbound request has a five-second timeout and no redirects. There is no arbitrary send endpoint.

## Security and logs

- GET `/webhook` requires subscribe mode, the configured token and a nonempty challenge, returned as plain text.
- POST `/webhook` verifies `X-Hub-Signature-256` against the exact raw body with `META_APP_SECRET` before JSON processing. Invalid/missing signatures return 401, malformed signed JSON 400 and oversized bodies 413. Limit: 256 KiB; compressed bodies rejected.
- All entries/changes/messages are processed; status-only/unsupported events are acknowledged without replies.
- JSON logs include request IDs, route category, response status/duration, event counts and skip reasons. Application logs omit raw bodies, query strings, headers, tokens, phone numbers, message IDs and provider error bodies. Review Render's own access logging separately.
- GET `/health` returns `{"status":"ok"}`; this proves process availability, not Meta routing or token validity.

## Local verification

Use a current supported Node.js release (verified with Node 24): `npm ci`, then `npm test`. Tests use signed localhost requests and fake outbound transport; no WhatsApp or OpenAI calls. Coverage includes verification, tampering, unsigned requests, limits, privacy, off mode, allowlists, timestamps, concurrency, duplicates, cooldown, budget, expiry and provider errors.

`.env.example` is a reference only; the app does not automatically load `.env`. Set deployment values in Render Environment. Never commit secrets. npm and Yarn lockfiles preserve either install flow; retain the existing Render build command.

## Boundaries before broader client messaging

This release supports receiving authenticated events and small, single-instance controlled tests. It is not a durable message inbox or a production AI responder. Receive-only content is acknowledged without storage; diagnostic logs are not a business message archive.

Deduplication (seven-day retention, 10,000-ID cap), counters and cooldowns live in process memory. They reset on restart/redeploy and are not shared between replicas. Keep one instance during testing. A restart inside the freshness window could allow a repeated response; a crash may lose a test response. Before client messaging, add a durable queue/inbox and shared idempotency, retention/access controls, delivery monitoring and a reviewed response policy. Never roll back to the old automatic-reply code as a safety measure.
