#!/usr/bin/env node
/**
 * Renders assets/top-langs-card.svg from live GitHub GraphQL data.
 */

const fs = require("fs");
const path = require("path");
const theme = require("./lib/theme");
const { fetchGitHubData } = require("./lib/fetch-github-data");

const OUT_PATH = path.join(__dirname, "..", "assets", "top-langs-card.svg");

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function langRow(y, lang, barMaxWidth) {
  const barWidth = Math.max(4, (lang.percent / 100) * barMaxWidth);
  const pct = lang.percent.toFixed(1);

  return `
    <g transform="translate(24, ${y})">

      <circle
        cx="5"
        cy="5"
        r="5"
        fill="${lang.color}"/>

      <text
        x="16"
        y="9"
        font-family="${theme.font}"
        font-size="12"
        fill="${theme.text}">
        ${escapeXml(lang.name)}
      </text>

      <text
        x="${barMaxWidth}"
        y="9"
        font-family="${theme.font}"
        font-size="11"
        fill="${theme.textMuted}"
        text-anchor="end">
        ${pct}%
      </text>

      <rect
        x="0"
        y="16"
        width="${barMaxWidth}"
        height="7"
        rx="3.5"
        fill="${theme.bgAlt}"/>

      <rect
        x="0"
        y="16"
        width="${barWidth}"
        height="7"
        rx="3.5"
        fill="${lang.color}"/>

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

  const barMaxWidth = width - 48;

  const langs = data.topLanguages.length
    ? data.topLanguages
    : [
        {
          name: "No public language data",
          color: theme.textMuted,
          percent: 0,
        },
      ];

  const rowHeight = 30;

  const rows = langs
    .map((lang, index) => langRow(54 + index * rowHeight, lang, barMaxWidth))
    .join("\n");

  const summary = langs
    .map((lang) => `${lang.name} ${lang.percent.toFixed(1)}%`)
    .join(", ");

  return `<svg
    width="${width}"
    height="${height}"
    viewBox="0 0 ${width} ${height}"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="${escapeXml(data.login)}'s most used languages: ${escapeXml(summary)}">

  <title>Most Used Languages — ${escapeXml(data.login)}</title>

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
    Most Used Languages
  </text>

  ${rows}

  <text
    x="24"
    y="${height - 18}"
    font-family="${font}"
    font-size="10"
    fill="${textMuted}">
    by bytes across public, non-fork repositories
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
      "Top Languages card: falling back to pending-sync placeholder —",
      err.message
    );

    const svg = theme.pendingCard(
      "Most Used Languages",
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

module.exports = { buildSvg };
