const express = require("express");
const axios = require("axios");
const app = express();
app.use(express.json());

const VERIFY_TOKEN = "vedasvision2024";
const WHATSAPP_TOKEN = process.env.WHATSAPP_TOKEN;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const PHONE_NUMBER_ID = process.env.PHONE_NUMBER_ID;

const SYSTEM_PROMPT = `You are Jack Lakhpatani's AI assistant at Vedas Vision Accounting & Auditing LLC, Dubai, UAE. Jack is a Senior Compliance Advisor specializing in AML/CFT compliance, KYC audits, VAT returns, goAML/DPMSR reporting for UAE DNFBP clients in gold and jewellery sector. Reply professionally on Jack's behalf. Keep replies concise. For complex matters say: "Thank you for your message. Jack sir will personally review this and revert shortly."`;

app.get("/webhook", (req, res) => {
  if (req.query["hub.verify_token"] === VERIFY_TOKEN) {
    res.send(req.query["hub.challenge"]);
  } else {
    res.sendStatus(403);
  }
});

app.post("/webhook", async (req, res) => {
  try {
    const message = req.body.entry?.[0]?.changes?.[0]?.value?.messages?.[0];
    if (!message || message.type !== "text") return res.sendStatus(200);

    const from = message.from;
    const text = message.text.body;

    const openaiRes = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4",
        max_tokens: 500,
        messages: [
          { role: "system", content: SYSTEM_PROMPT },
          { role: "user", content: text }
        ]
      },
      {
        headers: {
          "Authorization": `Bearer ${OPENAI_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    const reply = openaiRes.data.choices[0].message.content;

    await axios.post(
      `https://graph.facebook.com/v18.0/${PHONE_NUMBER_ID}/messages`,
      {
        messaging_product: "whatsapp",
        to: from,
        text: { body: reply }
      },
      {
        headers: {
          Authorization: `Bearer ${WHATSAPP_TOKEN}`,
          "Content-Type": "application/json"
        }
      }
    );

    res.sendStatus(200);
  } catch (err) {
    console.error(err.message);
    res.sendStatus(500);
  }
});

app.listen(process.env.PORT || 3000, () => {
  console.log("VedasVision Bot running!");
});
