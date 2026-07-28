#!/usr/bin/env node
/**
 * Renders assets/trophies-card.svg from live GitHub GraphQL data.
 */

const fs = require("fs");
const path = require("path");
const theme = require("./lib/theme");
const { fetchGitHubData } = require("./lib/fetch-github-data");

const OUT_PATH = path.join(__dirname, "..", "assets", "trophies-card.svg");

const TIERS = [
  { min: 0, label: "C" },
  { min: 10, label: "B" },
  { min: 50, label: "A" },
  { min: 150, label: "S" },
  { min: 500, label: "SS" },
];

function tierFor(value) {
  let label = TIERS[0].label;

  for (const tier of TIERS) {
    if (value >= tier.min) {
      label = tier.label;
    }
  }

  return label;
}

const TIER_COLOR = {
  C: "#94A3B8",
  B: "#A78BFA",
  A: "#8B5CF6",
  S: "#F8FAFC",
  SS: "#F8FAFC",
};

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function chip(x, label, value) {
  const tier = tierFor(value);
  const color = TIER_COLOR[tier] || theme.text;

  return `
    <g transform="translate(${x},54)">

      <rect
        x="0"
        y="0"
        width="75"
        height="120"
        rx="12"
        fill="${theme.bgAlt}"
        stroke="${theme.border}"
        stroke-opacity="0.35"/>

      <text
        x="37.5"
        y="34"
        font-family="${theme.font}"
        font-size="24"
        font-weight="700"
        fill="${color}"
        text-anchor="middle">
        ${tier}
      </text>

      <text
        x="37.5"
        y="70"
        font-family="${theme.font}"
        font-size="18"
        font-weight="700"
        fill="${theme.text}"
        text-anchor="middle">
        ${escapeXml(value)}
      </text>

      <text
        x="37.5"
        y="98"
        font-family="${theme.font}"
        font-size="10"
        fill="${theme.textMuted}"
        text-anchor="middle">
        ${escapeXml(label)}
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

  const chipWidth = 75;
  const gap = 18;

  const colX = (i) => 24 + i * (chipWidth + gap);

  const chips = [
    chip(colX(0), "Stars", data.totalStars),
    chip(colX(1), "Followers", data.followers),
    chip(colX(2), "Repos", data.publicRepos),
    chip(colX(3), "Commits (1y)", data.commitsPastYear),
    chip(colX(4), "PRs (1y)", data.prsPastYear),
  ].join("\n");

  return `<svg
    width="${width}"
    height="${height}"
    viewBox="0 0 ${width} ${height}"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="${escapeXml(data.login)}'s GitHub milestones">

  <title>GitHub Milestones — ${escapeXml(data.login)}</title>

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
    GitHub Milestones
  </text>

  ${chips}

  <text
    x="24"
    y="${height - 18}"
    font-family="${font}"
    font-size="10"
    fill="${textMuted}">
    Tiers: C &lt; 10 • B &lt; 50 • A &lt; 150 • S &lt; 500 • SS 500+
  </text>

</svg>`;
}

async function main() {
  try {
    const data = await fetchGitHubData();

    const svg = buildSvg(data);

    fs.mkdirSync(path.dirname(OUT_PATH), {
      recursive: true,
    });

    fs.writeFileSync(OUT_PATH, svg, "utf8");

    console.log(`Wrote ${OUT_PATH}`);
  } catch (err) {
    console.error(
      "Trophies card: falling back to pending-sync placeholder —",
      err.message
    );

    const svg = theme.pendingCard(
      "GitHub Milestones",
      "waiting for GH_TOKEN / next run"
    );

    fs.mkdirSync(path.dirname(OUT_PATH), {
      recursive: true,
    });

    fs.writeFileSync(OUT_PATH, svg, "utf8");
  }
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = {
  buildSvg,
  tierFor,
};
