const fs = require("fs");
const path = require("path");
const axios = require("axios");

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY) {
  console.error("Set OPENAI_API_KEY before running this script.");
  process.exit(1);
}

const STYLE =
  "2D flat cartoon illustration, Indian comic book style, bold black outlines, " +
  "bright saturated colors, simple clean background, expressive exaggerated facial " +
  "emotions, no text, no speech bubbles, no captions, no letters or signage text. " +
  "Consistent character design across the image: the Customer is an Indian woman " +
  "wearing a salwar kameez; the Bijli Vibhag worker is an Indian electricity-department " +
  "employee wearing a khaki uniform.";

const panels = [
  {
    name: "01-the-call",
    prompt:
      `${STYLE} Scene: split composition. On the left, the Customer stands in a dim, ` +
      "powerless room holding a phone to her ear, eyebrows raised expectantly. On the " +
      "right, the Bijli Vibhag worker sits at a small government desk with a phone to " +
      "his ear, a desk fan and stacked files in front of him, giving a guilty sheepish smile."
  },
  {
    name: "02-windy-excuse",
    prompt:
      `${STYLE} Scene: the Bijli Vibhag worker stands by a window with both palms raised ` +
      "defensively, sweat drop on his forehead, gesturing toward a stormy window where " +
      "trees bend and leaves fly in strong wind. The Customer, arms crossed, glares at him " +
      "with a deeply unimpressed expression."
  },
  {
    name: "03-catching-cold",
    prompt:
      `${STYLE} Scene: the Customer is wrapped tightly in a shawl, shivering with an ` +
      "exaggerated sneeze captured as a pure motion burst with no lettering of any kind, " +
      "eyes watering comically, standing in a dark room with a dead ceiling fan above her. " +
      "The Bijli Vibhag worker stands at the doorway shrugging with an indifferent half-smile. " +
      "Absolutely no onomatopoeia, no written words, no sound-effect lettering anywhere in the image."
  },
  {
    name: "04-danger-wire",
    prompt:
      `${STYLE} Scene: the Bijli Vibhag worker strikes a proud heroic pose, one hand on ` +
      "his chest, the other pointing dramatically at a snapped electrical wire dangling " +
      "with sparks from a leaning power pole toward a small house roof in the background. " +
      "His face shows exaggerated alarm mixed with pride."
  },
  {
    name: "05-shocked-reaction",
    prompt:
      `${STYLE} Scene: the Customer stands at her doorway with both hands on her hips, ` +
      "mouth wide open mid-demand, finger pointing forward insistently. The Bijli Vibhag " +
      "worker recoils backward with an exaggerated startled expression, eyes wide as " +
      "saucers, sweat drops flying off his head."
  },
  {
    name: "06-pointing-at-wires",
    prompt:
      `${STYLE} Scene: outdoors near a row of power poles strung with wires overhead. The ` +
      "Customer points upward with a sarcastic raised eyebrow and a smug half-smile. The " +
      "Bijli Vibhag worker, standing beside her, scratches the back of his head looking up " +
      "at the wires with a baffled, stumped expression."
  },
  {
    name: "07-let-it-be",
    prompt:
      `${STYLE} Scene: the Bijli Vibhag worker leans back lazily in his office chair, ` +
      "hands behind his head, feet propped up on the desk, totally carefree expression " +
      "with closed relaxed eyes. In the background the Customer stands fuming with arms " +
      "tightly crossed, cartoon steam puffing out of her ears."
  },
  {
    name: "08-final-threat",
    prompt:
      `${STYLE} Scene: the Customer leans forward with a furious red-tinted face, fist ` +
      "raised and the other hand pointing sharply upward as if threatening to escalate to " +
      "higher authorities. The Bijli Vibhag worker stands with arms crossed, shrugging one " +
      "shoulder, wearing a completely unbothered sarcastic smirk."
  }
];

async function generatePanel(panel) {
  const res = await axios.post(
    "https://api.openai.com/v1/images/generations",
    {
      model: "gpt-image-1",
      prompt: panel.prompt,
      size: "1024x1024",
      quality: "high",
      n: 1
    },
    {
      headers: {
        Authorization: `Bearer ${OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      }
    }
  );

  const b64 = res.data.data[0].b64_json;
  const outDir = path.join(__dirname, "output");
  fs.mkdirSync(outDir, { recursive: true });
  const filePath = path.join(outDir, `${panel.name}.png`);
  fs.writeFileSync(filePath, Buffer.from(b64, "base64"));
  console.log("Saved", filePath);
}

async function main() {
  const only = process.argv[2];
  const targets = only ? panels.filter((p) => p.name === only) : panels;

  for (const panel of targets) {
    try {
      await generatePanel(panel);
    } catch (err) {
      console.error(`Failed panel ${panel.name}:`, err.response?.data || err.message);
    }
  }
}

main();
