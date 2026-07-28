#!/usr/bin/env node
/**
 * Generates a theme-matched GeeksforGeeks stats card as a static SVG.
 */

const fs = require("fs");
const path = require("path");
const theme = require("./lib/theme");

const DATA_PATH = path.join(__dirname, "..", "data", "gfg-stats.json");
const OUT_PATH = path.join(__dirname, "..", "assets", "gfg-card.svg");

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function formatRank(rank) {
  const n = Number(rank);
  if (!n || n <= 0) return "Unranked";
  return `#${n.toLocaleString("en-IN")}`;
}

function statTile(x, y, label, value) {
  return `
    <g transform="translate(${x}, ${y})">
      <rect
        x="0"
        y="0"
        width="215"
        height="58"
        rx="10"
        fill="${theme.bgAlt}"
        stroke="${theme.border}"
        stroke-opacity="0.35"/>

      <text
        x="16"
        y="24"
        font-family="${theme.font}"
        font-size="12"
        fill="${theme.textMuted}"
        letter-spacing="0.3">
        ${escapeXml(label)}
      </text>

      <text
        x="16"
        y="46"
        font-family="${theme.font}"
        font-size="22"
        font-weight="700"
        fill="${theme.text}">
        ${escapeXml(value)}
      </text>
    </g>`;
}

function buildSvg(data) {
  const {
    width,
    height,
    radius,
    bg,
    border,
    accentSoft,
    textMuted,
    font,
  } = theme;

  const tiles = [
    statTile(24, 66, "Problems Solved", data.problemsSolved),
    statTile(256, 66, "Coding Score", data.codingScore),
    statTile(24, 122, "Institute Rank", formatRank(data.instituteRank)),
    statTile(256, 122, "POTD Solved", data.potdSolved),
  ].join("\n");

  return `<svg
    width="${width}"
    height="${height}"
    viewBox="0 0 ${width} ${height}"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="GeeksforGeeks Stats">

  <title>GeeksforGeeks Stats — ${escapeXml(data.username)}</title>

  <rect
    x="1"
    y="1"
    width="${width - 2}"
    height="${height - 2}"
    rx="${radius}"
    fill="${bg}"
    stroke="${border}"
    stroke-width="1.4"/>

  <text
    x="24"
    y="33"
    font-family="${font}"
    font-size="16"
    font-weight="700"
    fill="${accentSoft}">
    GeeksforGeeks Stats
  </text>

  ${tiles}

  <text
    x="24"
    y="${height - 18}"
    font-family="${font}"
    font-size="10"
    fill="${textMuted}">
    @${escapeXml(data.username)} &#8226; verified ${escapeXml(data.lastVerified)}
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
