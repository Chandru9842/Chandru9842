#!/usr/bin/env node
/**
 * Renders assets/github-stats-card.svg from live GitHub GraphQL data.
 * Self-hosted replacement for the previously-broken github-readme-stats.vercel.app
 * card.
 */

const fs = require("fs");
const path = require("path");
const theme = require("./lib/theme");
const { fetchGitHubData } = require("./lib/fetch-github-data");

const OUT_PATH = path.join(__dirname, "..", "assets", "github-stats-card.svg");

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function tile(x, y, w, label, value) {
  return `
    <g transform="translate(${x}, ${y})">
      <rect
        x="0"
        y="0"
        width="${w}"
        height="58"
        rx="10"
        fill="${theme.bgAlt}"
        stroke="${theme.border}"
        stroke-opacity="0.35"
      />
      <text
        x="14"
        y="24"
        font-family="${theme.font}"
        font-size="11"
        fill="${theme.textMuted}"
        letter-spacing="0.3">
        ${escapeXml(label)}
      </text>
      <text
        x="14"
        y="46"
        font-family="${theme.font}"
        font-size="20"
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

  const colW = 149;
  const gap = 8;
  const col = (i) => 24 + i * (colW + gap);

  const row1 = [
    tile(col(0), 66, colW, "Public Repos", data.publicRepos),
    tile(col(1), 66, colW, "Total Stars", data.totalStars),
    tile(col(2), 66, colW, "Followers", data.followers),
  ].join("\n");

  const row2 = [
    tile(col(0), 122, colW, "Commits (1y)", data.commitsPastYear),
    tile(col(1), 122, colW, "PRs (1y)", data.prsPastYear),
    tile(col(2), 122, colW, "Issues (1y)", data.issuesPastYear),
  ].join("\n");

  return `<svg
    width="${width}"
    height="${height}"
    viewBox="0 0 ${width} ${height}"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="${escapeXml(
      data.login
    )}'s GitHub stats: ${data.publicRepos} public repos, ${
    data.totalStars
  } total stars, ${data.followers} followers, ${
    data.commitsPastYear
  } commits in the past year, ${data.prsPastYear} pull requests in the past year, ${
    data.issuesPastYear
  } issues in the past year">

  <title>GitHub Stats — ${escapeXml(data.login)}</title>

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
    GitHub Stats
  </text>

  ${row1}

  ${row2}

  <text
    x="24"
    y="${height - 18}"
    font-family="${font}"
    font-size="10"
    fill="${textMuted}">
    @${escapeXml(
      data.login
    )} &#8226; commits/PRs/issues are past 12 months
  </text>

</svg>`;
}

async function main() {
  try {
    const data = await fetchGitHubData();
    const svg = buildSvg(data);

    fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
    fs.writeFileSync(OUT_PATH, svg, "utf8");

    console.log(`Wrote ${OUT_PATH}`);
  } catch (err) {
    console.error(
      "GitHub Stats card: falling back to pending-sync placeholder —",
      err.message
    );

    const svg = theme.pendingCard(
      "GitHub Stats",
      "waiting for GH_TOKEN / next run"
    );

    fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
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
