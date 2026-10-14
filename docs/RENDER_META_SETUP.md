# JARVIS: exact Render and Meta steps

## What the earlier success proves

Meta's “Send successfully” confirms the dashboard sample was accepted at that time. It does not prove real inbound routing, WhatsApp delivery, AI quality or Live readiness. Render's “Your service is live” is independent of the Meta app's Development/Live setting.

The supplied screenshot shows Render service `jarvis-whatsapp`, source commit `a0f641d`, start command `node index.js`, and primary URL `https://jarvis-whatsapp-61du.onrender.com`. Confirm the URL is still current in Render. Keep the existing service and connected deployment branch. Merge the changes into that branch rather than pointing Render at a temporary branch. The reviewed repository's default is `main`.

## 1. Prepare Render before deploying

Keep Meta in Development. Open **Render → jarvis-whatsapp → Environment → Edit**:

| Variable | Value |
| --- | --- |
| `VERIFY_TOKEN` | New password-manager-generated random secret, preferably 32 random bytes. Use the exact same value in Meta. Do not reuse the old source-code token. |
| `META_APP_SECRET` | Secret from the same Meta developer app: **App settings → Basic → App secret**. Different from the verify token and WhatsApp access token. |
| `REPLY_MODE` | `off` |

Keep existing `WHATSAPP_TOKEN`, `PHONE_NUMBER_ID` and `OPENAI_API_KEY` entries. Off mode does not use them; OpenAI is unused in every mode of this release. Do not copy secrets into GitHub or chat.

Choose **Save only** while the old commit is running, if available. Setting `REPLY_MODE=off` does NOT disable the old code's replies: the protection only applies after deploying the new code. Avoid real test/client messages until the new revision is confirmed.

Merge the reviewed PR into the branch already connected to Render. Let normal auto-deploy run, or use **Manual Deploy → Deploy latest commit** if automatic deployment is disabled. If variables still need applying, choose **Save, rebuild, and deploy** after the new commit is on the connected branch. Keep the build and start commands unchanged. Both npm and Yarn lockfiles are supplied for the existing install flow.

Wait for **Deploy succeeded**. Verify the source commit is the new change. In **Logs → Live tail**, expect:

```json
{"event":"service_started","reply_mode":"off","test_expires_at":null}
```

Open `https://jarvis-whatsapp-61du.onrender.com/health`; expect `{"status":"ok"}`. Missing required variables cause startup failure. Fix the named variable and redeploy, without bypassing validation. A failed deploy can leave the previous unsafe revision serving traffic: check the deployed commit and startup log, not only the green service status.

## 2. Verify Meta and a dashboard sample in off mode

In the same Meta app, open **WhatsApp → Configuration → Webhooks → Edit**, or **Webhooks → WhatsApp Business Account**, depending on the dashboard layout.

1. Callback URL: `https://jarvis-whatsapp-61du.onrender.com/webhook`.
2. Verify token: exact new `VERIFY_TOKEN` value saved in Render.
3. Click **Verify and save**. Expect `verification_succeeded` and request status 200 in Render.
4. Subscribe the WhatsApp Business Account **messages** field.
5. Click **messages → Test → Send to server v26.0**, matching the supplied screenshot. Keep the sample unchanged. Expect `webhook_received`, `reply_skipped` with `reason: "replies_disabled"` for an incoming-message sample, and status 200. Status-only samples have no reply skip.

No WhatsApp reply is expected. If `signature_rejected` appears, verify the secret belongs to the app sending the callback and is current. Do not disable signature validation. A sample without a valid signature is intentionally rejected.

## 3. Arm one short controlled test

In Meta **WhatsApp → API Setup / API Testing**, select the test business number and add/verify only your intended personal test recipient. `PHONE_NUMBER_ID` must be that business sender's ID, not its visible phone number, WABA ID or App ID. Incoming webhook metadata must match it. `WHATSAPP_TOKEN` must be valid for the app/account/number with WhatsApp messaging access; temporary tokens may have expired.

Set these in Render:

| Variable | Value |
| --- | --- |
| `REPLY_MODE` | `test` |
| `TEST_ALLOWED_NUMBERS` | Your own personal test WhatsApp number in international digits, country code included, without `+`, spaces or punctuation. Multiple approved test phones may be comma-separated. Do not add clients. |
| `PHONE_NUMBER_ID` | Meta test business phone number ID. |
| `WHATSAPP_TOKEN` | Valid token for that number. |
| `GRAPH_API_VERSION` | `v26.0`, matching the version in your screenshot; confirm support in your app. |
| `TEST_MODE_EXPIRES_AT` | ISO time 30 minutes from starting the test, with Dubai `+04:00` or UTC `Z`. Must be future and within one hour at startup. Format: `YYYY-MM-DDTHH:mm:ss+04:00`. |

Click **Save, rebuild, and deploy** and confirm startup shows test mode and the intended expiry. Use one service instance; avoid redeploys during testing.

From your allowlisted personal phone, send exactly **JARVIS TEST** to the Meta test business number. This is an intentional real message. The synthetic dashboard sample is not a replacement and should not trigger a reply.

Expect `webhook_received` → `test_reply_attempted` → `test_reply_accepted` → HTTP 200. The phone should receive:

> JARVIS controlled test successful. Automatic client replies are disabled.

“Accepted” means Meta accepted the send request; verify actual receipt on the phone. Status callbacks are acknowledged/counted but not stored as delivery records.

Send “hello” from the same phone: expect `test_command_required` and no reply. Non-allowlisted senders get `sender_not_allowed`; local tests verify this without contacting clients. There is one response per sender per minute and a maximum of five attempts per process. Duplicate IDs are suppressed within the process. Expiry stops sending automatically.

If the sample arrives but real messages do not, check the selected test number/recipient and the correct WABA's app subscription. `GET /{WABA-ID}/subscribed_apps` lists subscriptions; the documented `POST /{WABA-ID}/subscribed_apps` subscribes your app using an appropriate account token when absent. This is separate from the messages-field subscription. Do not switch Live merely to troubleshoot; inspect your app's current access/testing requirements first.

For `test_reply_failed`, provider status 401 suggests authentication, 403 suggests permission/account access, and 400 suggests request/number/recipient configuration. These are diagnostic starting points. Check Meta's dashboard for specifics. Null status may indicate timeout or transport failure; check the phone before retrying manually. Never paste full provider payloads or tokens into logs/chat.

## 4. Disarm and prepare for Live

Immediately set **`REPLY_MODE=off` → Save, rebuild, and deploy** after testing. Confirm startup shows off, then repeat a signed sample: expect acknowledgement, `replies_disabled` and no outbound attempt. This is the kill switch. Never roll back to `a0f641d`, which automatically replied.

Before switching Meta Live, complete the requirements shown for your app/use case: business/phone registration, permissions/access level, privacy policy and data deletion information, and app/business verification or review where required. Use an appropriately managed production token. Account-specific readiness cannot be established by repository tests.

Keep `REPLY_MODE=off` during the eventual Live switch. Meta Live will not enable client replies in this code. Observe authenticated real events before planning a broader response rollout. Client AI messaging requires separately reviewed durable queueing/idempotency and a response policy; it cannot be enabled through a flag in this release.

## Validation boundary and sources

Repository tests use fake credentials, localhost requests and a mocked transport. No real WhatsApp message was sent during validation. GitHub changes do not confirm Render environment values, deployment, Meta subscriptions, valid tokens or actual delivery; complete the account steps above.

- [Render environment variables and save/deploy actions](https://render.com/docs/configure-environment-variables)
- [Render deployment behavior](https://render.com/docs/deploys)
- [Meta-hosted verification and signature reference](https://whatsapp.github.io/WhatsApp-Nodejs-SDK/api-reference/webhooks/start/)
- [Meta-hosted receiving-message setup](https://whatsapp.github.io/WhatsApp-Nodejs-SDK/receivingMessages/)
- [Meta's WABA subscription API collection](https://www.postman.com/meta/whatsapp-business-platform/request/ju40fld/subscribe-app-to-waba-s-webhooks)

The SDK pages are older protocol references, not a recommendation to install that SDK. Direct developers.facebook.com documentation was rate-limited during review; check your dashboard for current account-specific Live requirements.
