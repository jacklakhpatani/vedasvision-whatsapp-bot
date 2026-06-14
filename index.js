const express = require("express");
const axios = require("axios");
const { collectFullReport } = require("./instagram");

const app = express();
app.use(express.json());

const VERIFY_TOKEN = "vedasvision2024";
const WHATSAPP_TOKEN = process.env.WHATSAPP_TOKEN;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const PHONE_NUMBER_ID = process.env.PHONE_NUMBER_ID;

const SYSTEM_PROMPT = `You are Jack Lakhpatani's AI assistant at Vedas Vision Accounting & Auditing LLC, Dubai, UAE. Jack is a Senior Compliance Advisor specializing in AML/CFT compliance, KYC audits, VAT returns, goAML/DPMSR reporting for UAE DNFBP clients in gold and jewellery sector. Reply professionally on Jack's behalf. Keep replies concise. For complex matters say: "Thank you for your message. Jack sir will personally review this and revert shortly."`;

const INSTAGRAM_ANALYST_PROMPT = `You are a Senior Instagram Growth Analyst with deep expertise in the Instagram algorithm, Meta's content distribution systems, and social media growth strategy. You have access to raw Instagram Graph API data for an account.

Analyze the provided data thoroughly and deliver a structured diagnostic report covering:

1. ACCOUNT HEALTH CHECK
- Trust signals (account age, consistency, policy compliance)
- Distribution limit indicators (sudden reach drops, content suppression patterns)
- Shadowban-like signals (hashtag reach disabled, Explore suppression)
- Hashtag audit (overuse, banned tags, irrelevant tags, tag-to-niche fit)
- Spam behavior flags (posting frequency, comment/DM patterns)
- Follower-to-engagement ratio health

2. CONTENT PERFORMANCE ANALYSIS
For each recent reel/post, diagnose:
- Hook strength (first 1-3 seconds based on caption/thumbnail patterns)
- Pacing issues (avg watch time vs video length ratio)
- Retention drop-off points (plays vs avg watch time delta)
- Rewatch rate (total play time / plays / duration)
- Caption effectiveness (length, CTA presence, keyword richness)
- Thumbnail/cover quality signals
- Niche confusion (does content theme drift across posts?)
- CTA weaknesses (saves, shares, comments prompts)
- Engagement rate per post vs follower baseline

3. AUDIENCE & ALGORITHM FIT
- Who Instagram currently thinks the content is for (based on engaged audience demographics)
- Reached vs engaged audience mismatch
- Follower vs non-follower reach ratio (is content being pushed to Explore/Reels tab?)
- Geographic reach quality (tier-1 vs tier-3 country mix)
- Age/gender alignment with ideal customer profile
- Algorithm confusion signals (inconsistent niche, language mixing)

4. ENGAGEMENT SIGNAL ANALYSIS
- Watch-through rate (key signal: >30% = algorithm push)
- Save rate (high-value signal: >1% of reach is strong)
- Share rate (viral coefficient)
- Comment quality (generic vs meaningful)
- Like-to-reach ratio
- Story reply and poll engagement
- Profile visit rate from posts

5. GROWTH VELOCITY DIAGNOSIS
- Follower growth trend (gaining/losing/stagnant)
- Best vs worst performing content patterns
- Posting frequency vs reach correlation
- Time-of-post patterns

6. EXACT ROOT CAUSES
List the top 3-5 specific reasons reach is low for this account with evidence from the data.

7. PRIORITY FIX PLAN
Give 5 specific, actionable steps ranked by impact. Be direct and data-driven.

Format your response with clear section headers. Be brutally honest. Use the exact metric numbers from the data to support every claim.`;

async function sendWhatsApp(to, text) {
  await axios.post(
    `https://graph.facebook.com/v18.0/${PHONE_NUMBER_ID}/messages`,
    {
      messaging_product: "whatsapp",
      to,
      text: { body: text },
    },
    {
      headers: {
        Authorization: `Bearer ${WHATSAPP_TOKEN}`,
        "Content-Type": "application/json",
      },
    }
  );
}

async function callOpenAI(systemPrompt, userContent, maxTokens = 500) {
  const res = await axios.post(
    "https://api.openai.com/v1/chat/completions",
    {
      model: "gpt-4",
      max_tokens: maxTokens,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userContent },
      ],
    },
    {
      headers: {
        Authorization: `Bearer ${OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
    }
  );
  return res.data.choices[0].message.content;
}

// Split long text into WhatsApp-safe chunks (4096 char limit)
function chunkText(text, maxLen = 4000) {
  const chunks = [];
  let remaining = text;
  while (remaining.length > maxLen) {
    let split = remaining.lastIndexOf("\n", maxLen);
    if (split === -1) split = maxLen;
    chunks.push(remaining.slice(0, split).trim());
    remaining = remaining.slice(split).trim();
  }
  if (remaining) chunks.push(remaining);
  return chunks;
}

function isInstagramCommand(text) {
  const normalized = text.toLowerCase().trim();
  return (
    normalized.includes("analyze my instagram") ||
    normalized.includes("instagram reach") ||
    normalized.includes("instagram analysis") ||
    normalized.includes("why are my reels not getting views") ||
    normalized.includes("instagram audit") ||
    normalized.includes("ig audit") ||
    normalized.includes("ig analysis") ||
    normalized.includes("ig reach") ||
    normalized === "/igaudit" ||
    normalized === "/instagram"
  );
}

async function handleInstagramAnalysis(from) {
  if (!process.env.INSTAGRAM_TOKEN || !process.env.INSTAGRAM_USER_ID) {
    await sendWhatsApp(
      from,
      "Instagram analysis is not configured yet. Please set INSTAGRAM_TOKEN and INSTAGRAM_USER_ID environment variables."
    );
    return;
  }

  await sendWhatsApp(
    from,
    "Fetching your Instagram data now... This may take 30-60 seconds. I'll send a full diagnostic report shortly."
  );

  const report = await collectFullReport();

  const dataContext = `
INSTAGRAM ACCOUNT DATA:
${JSON.stringify(report, null, 2)}
`.slice(0, 12000); // keep within GPT-4 context limits

  const analysis = await callOpenAI(
    INSTAGRAM_ANALYST_PROMPT,
    `Please analyze this Instagram account data and provide a full diagnostic report:\n\n${dataContext}`,
    3000
  );

  const chunks = chunkText(
    `INSTAGRAM REACH ANALYSIS REPORT\n${"=".repeat(32)}\n\n${analysis}`
  );

  for (const chunk of chunks) {
    await sendWhatsApp(from, chunk);
  }
}

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

    if (isInstagramCommand(text)) {
      res.sendStatus(200);
      await handleInstagramAnalysis(from);
      return;
    }

    const reply = await callOpenAI(SYSTEM_PROMPT, text, 500);
    await sendWhatsApp(from, reply);
    res.sendStatus(200);
  } catch (err) {
    console.error(err.message);
    res.sendStatus(500);
  }
});

app.listen(process.env.PORT || 3000, () => {
  console.log("VedasVision Bot running!");
});
