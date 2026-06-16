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
  "emotions. Consistent character design across every panel: the Customer is a " +
  "50-year-old Indian uncle with a thick grey mustache, wearing a white dhoti, a " +
  "sleeveless baniyan (vest), and a checkered gamcha draped around his neck, talking " +
  "on an old black rotary telephone. The Bijli Vibhag worker is a 40-45 year old " +
  "Indian man wearing a khaki government uniform shirt, khaki pants, and a khaki cap. " +
  "The panel includes one clear comic-style speech bubble with accurately spelled, " +
  "legible text showing the speaking character's dialogue line, and nothing else " +
  "written anywhere else in the image.";

const dialogue = [
  {
    name: "01-hello",
    speaker: "Customer",
    line: "Hello",
    scene:
      "the Customer sits on a wooden stool at home holding an old black rotary " +
      "telephone receiver to his ear with his other hand on the phone base, greeting " +
      "warmly. Only the Customer is visible in this panel."
  }
  // Further lines will be appended here one at a time as each panel gets approved.
];

async function generatePanel(panel) {
  const prompt =
    `${STYLE} Scene: ${panel.scene} Speech bubble text (render exactly, ` +
    `correctly spelled): "${panel.line}" coming from the ${panel.speaker}.`;

  const res = await axios.post(
    "https://api.openai.com/v1/images/generations",
    {
      model: "gpt-image-1",
      prompt,
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
  const targets = only ? dialogue.filter((p) => p.name === only) : dialogue;

  for (const panel of targets) {
    try {
      await generatePanel(panel);
    } catch (err) {
      console.error(`Failed panel ${panel.name}:`, err.response?.data || err.message);
    }
  }
}

main();
