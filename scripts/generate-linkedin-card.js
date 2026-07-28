#!/usr/bin/env node
/**
 * Generates a large, theme-matched LinkedIn profile card as a static,
 * fully self-contained SVG.
 *
 * USAGE:
 *   node scripts/generate-linkedin-card.js
 */

const fs = require("fs");
const path = require("path");
const theme = require("./lib/theme");

const DATA_PATH = path.join(__dirname, "..", "data", "profile-info.json");
const OUT_PATH = path.join(__dirname, "..", "assets", "linkedin-card.svg");

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function buildSvg(data) {
  const {
    width,
    height,
    radius,
    bg,
    bgAlt,
    border,
    accent,
    accentSoft,
    text,
    textMuted,
    font,
    icons,
  } = theme;

  const li = icons.linkedin;

  return `<svg
    width="${width}"
    height="${height}"
    viewBox="0 0 ${width} ${height}"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="LinkedIn profile card for ${escapeXml(data.name)}">

  <title>Connect with ${escapeXml(data.name)} on LinkedIn</title>

  <rect
    x="1"
    y="1"
    width="${width - 2}"
    height="${height - 2}"
    rx="${radius}"
    fill="${bg}"
    stroke="${border}"
    stroke-width="1.4"/>

  <!-- LinkedIn Icon -->
  <rect
    x="24"
    y="20"
    width="56"
    height="56"
    rx="12"
    fill="${bgAlt}"
    stroke="${border}"
    stroke-opacity="0.35"/>

  <g transform="translate(38,34) scale(1.75)">
    <path d="${li.path}" fill="#0A66C2"/>
  </g>

  <!-- Name -->
  <text
    x="96"
    y="42"
    font-family="${font}"
    font-size="22"
    font-weight="700"
    fill="${text}">
    ${escapeXml(data.name)}
  </text>

  <!-- Headline -->
  <text
    x="96"
    y="66"
    font-family="${font}"
    font-size="13"
    fill="${accentSoft}">
    ${escapeXml(data.headline)}
  </text>

  <!-- Divider -->
  <line
    x1="24"
    y1="92"
    x2="${width - 24}"
    y2="92"
    stroke="${border}"
    stroke-opacity="0.25"/>

  <!-- Description -->
  <text
    x="24"
    y="122"
    font-family="${font}"
    font-size="14"
    fill="${textMuted}">
    Let's connect professionally on LinkedIn.
  </text>

  <!-- CTA Button -->
  <rect
    x="24"
    y="145"
    width="185"
    height="36"
    rx="18"
    fill="${accent}"/>

  <text
    x="116"
    y="168"
    font-family="${font}"
    font-size="14"
    font-weight="700"
    fill="${bg}"
    text-anchor="middle">
    ${escapeXml(data.cta)}
  </text>

  <!-- Footer -->
  <text
    x="${width - 24}"
    y="${height - 18}"
    font-family="${font}"
    font-size="10"
    fill="${textMuted}"
    text-anchor="end">
    linkedin.com/in/chandru9842
  </text>

</svg>`;
}

function main() {
  const data = JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));

  const svg = buildSvg(data);

  fs.mkdirSync(path.dirname(OUT_PATH), {
    recursive: true,
  });

  fs.writeFileSync(OUT_PATH, svg, "utf8");

  console.log(`Wrote ${OUT_PATH}`);
}

main();
