#!/usr/bin/env node
/**
 * Generates animated "jet over contribution grid" SVGs using a GitHub
 * user's REAL contribution calendar (34 weeks x 7 rows).
 *
 * Env vars:
 *   GH_USERNAME  - GitHub login to fetch contributions for (default: Chandru9842)
 *   GH_TOKEN     - token with access to the GraphQL API (optional, falls back to public API)
 */

import fs from "node:fs";
import path from "node:path";

const USERNAME = process.env.GH_USERNAME || "Chandru9842";
const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;

const COLS = 34; // weeks shown, matches the reference design
const ROWS = 7;
const CELL = 11;
const STEP = 14; // cell + gap
const GRID_X = 20;
const GRID_Y = 15;
const WIDTH = 513;
const HEIGHT = 170;
const JET_X_START = 35;
const JET_X_END = 478;
const LOOP_DUR = 20; // seconds, one full there-and-back pass
const MAX_TARGETS = 12; // how many "busiest" days the jet fires on
const PAD_Y = 128; // where bullets launch from (just under the grid)

const GRAPHQL_QUERY = `
  query($login: String!) {
    user(login: $login) {
      contributionsCollection {
        contributionCalendar {
          weeks {
            contributionDays {
              date
              contributionCount
              color
            }
          }
        }
      }
    }
  }
`;

async function fetchFromGraphQL() {
  if (!TOKEN) return null;
  try {
    const res = await fetch("https://api.github.com/graphql", {
      method: "POST",
      headers: {
        Authorization: `bearer ${TOKEN}`,
        "Content-Type": "application/json",
        "User-Agent": "github-jet-generator",
      },
      body: JSON.stringify({ query: GRAPHQL_QUERY, variables: { login: USERNAME } }),
    });
    if (!res.ok) {
      console.warn(`GraphQL response not OK (${res.status}), falling back to public endpoint...`);
      return null;
    }
    const json = await res.json();
    if (json.errors || !json.data?.user?.contributionsCollection?.contributionCalendar?.weeks) {
      return null;
    }
    return json.data.user.contributionsCollection.contributionCalendar.weeks;
  } catch (err) {
    console.warn("GraphQL fetch failed, falling back:", err.message);
    return null;
  }
}

async function fetchFromPublicAPI() {
  const res = await fetch(`https://github-contributions-api.jogruber.de/v4/${USERNAME}`);
  if (!res.ok) {
    throw new Error(`Public contribution API error: ${res.status} ${res.statusText}`);
  }
  const json = await res.json();
  const rawContribs = json.contributions || [];
  
  // Sort contributions by date
  rawContribs.sort((a, b) => new Date(a.date) - new Date(b.date));
  
  // Convert list of days into weekly chunks of 7
  const weeks = [];
  let currentWeek = [];
  
  for (const day of rawContribs) {
    currentWeek.push({
      date: day.date,
      contributionCount: day.count || 0,
      level: day.level || 0,
    });
    if (currentWeek.length === 7) {
      weeks.push({ contributionDays: currentWeek });
      currentWeek = [];
    }
  }
  if (currentWeek.length > 0) {
    weeks.push({ contributionDays: currentWeek });
  }
  
  return weeks;
}

async function fetchWeeks() {
  const gqlWeeks = await fetchFromGraphQL();
  if (gqlWeeks && gqlWeeks.length > 0) {
    return { weeks: gqlWeeks, isGql: true };
  }
  const pubWeeks = await fetchFromPublicAPI();
  return { weeks: pubWeeks, isGql: false };
}

const THEMES = {
  dark: {
    bg: "#0d1117",
    cardBorder: "#30363d",
    emptyCell: "#161b22",
    levels: ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    starColor: "#8b949e",
    flashColor: "#39d353",
    bulletColor: "#7ee787",
    blastColor: "#56d364",
    jetBody: "#58a6ff",
    jetStroke: "#1f6feb",
    jetWing: "#388bfd",
    jetCockpit: "#c9e6ff",
    jetFlame: "#f0883e",
  },
  light: {
    bg: "#ffffff",
    cardBorder: "#d0d7de",
    emptyCell: "#ebedf0",
    levels: ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    starColor: "#8c959f",
    flashColor: "#216e39",
    bulletColor: "#2ea043",
    blastColor: "#3fb950",
    jetBody: "#0969da",
    jetStroke: "#0550ae",
    jetWing: "#218bff",
    jetCockpit: "#ffffff",
    jetFlame: "#f0883e",
  },
};

function getCellColor(day, themeName) {
  const theme = THEMES[themeName];
  if (day.color && day.color !== "#ebedf0" && day.color !== "#161b22") {
    if (themeName === "dark") return day.color;
  }
  
  const count = day.contributionCount || 0;
  if (count === 0) return theme.emptyCell;
  if (count <= 2) return theme.levels[1];
  if (count <= 5) return theme.levels[2];
  if (count <= 9) return theme.levels[3];
  return theme.levels[4];
}

function buildCells(weeks, themeName) {
  const theme = THEMES[themeName];
  const recent = weeks.slice(-COLS);
  const padCount = COLS - recent.length;
  const padded = Array.from({ length: Math.max(0, padCount) }, () => ({
    contributionDays: Array.from({ length: ROWS }, () => ({
      contributionCount: 0,
      color: theme.emptyCell,
      date: null,
    })),
  })).concat(recent);

  const cells = [];
  padded.forEach((week, col) => {
    week.contributionDays.forEach((day, row) => {
      cells.push({
        col,
        row,
        x: GRID_X + col * STEP,
        y: GRID_Y + row * STEP,
        color: getCellColor(day, themeName),
        count: day.contributionCount || 0,
        date: day.date,
      });
    });
  });
  return cells;
}

function pickTargets(cells) {
  return [...cells]
    .filter((c) => c.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, MAX_TARGETS)
    .sort((a, b) => a.col - b.col || a.row - b.row);
}

function keyTimeForCol(col, direction) {
  const span = 0.46;
  const t = 0.02 + (col / (COLS - 1)) * span;
  return direction === "forward" ? t : 1 - t;
}

function fmt(n) {
  return Number(n.toFixed(4));
}

function buildGrid(cells, targets, theme) {
  const targetKey = new Set(targets.map((t) => `${t.col}-${t.row}`));
  let svg = "";
  for (const c of cells) {
    const isTarget = targetKey.has(`${c.col}-${c.row}`);
    if (!isTarget) {
      svg += `<rect x="${c.x.toFixed(2)}" y="${c.y.toFixed(2)}" width="${CELL}" height="${CELL}" rx="2" ry="2" fill="${c.color}"/>\n`;
      continue;
    }
    const tFwd = keyTimeForCol(c.col, "forward");
    const tBack = keyTimeForCol(c.col, "backward");
    const [t1, t2] = [Math.min(tFwd, tBack), Math.max(tFwd, tBack)];
    const dur = 0.006;
    svg += `<rect x="${c.x.toFixed(2)}" y="${c.y.toFixed(2)}" width="${CELL}" height="${CELL}" rx="2" ry="2" fill="${c.color}">` +
      `<animate attributeName="fill" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
      `keyTimes="0;${fmt(t1)};${fmt(t1 + dur)};${fmt(t2)};${fmt(t2 + dur)};1" ` +
      `values="${c.color};${c.color};${theme.flashColor};${c.color};${theme.flashColor};${c.color}"/>` +
      `</rect>\n`;
  }
  return svg;
}

function buildBulletsAndBlasts(targets, theme) {
  let bullets = "";
  let blasts = "";
  const dur = 0.006;

  for (const dir of ["forward", "backward"]) {
    const ordered = dir === "forward" ? targets : [...targets].reverse();
    for (const c of ordered) {
      const t = keyTimeForCol(c.col, dir);
      const rise = t - dur * 3;
      const arrive = t;
      const fadeEnd = t + dur;
      const cx = fmt(c.x + CELL / 2);
      const targetY = fmt(c.y + CELL / 2);

      bullets += `<circle cx="${cx}" cy="${PAD_Y}" r="2.4" fill="${theme.bulletColor}">` +
        `<animate attributeName="cy" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(rise)};${fmt(arrive)};1" values="${PAD_Y};${PAD_Y};${targetY};${targetY}"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(rise)};${fmt(arrive)};${fmt(fadeEnd)};1" values="0;1;1;0;0"/>` +
        `</circle>\n`;

      blasts += `<circle cx="${cx}" cy="${targetY}" r="0" fill="none" stroke="${theme.blastColor}" stroke-width="1.6" opacity="0">` +
        `<animate attributeName="r" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(arrive)};${fmt(arrive + dur * 3)};1" values="0;1;9;9"/>` +
        `<animate attributeName="opacity" dur="${LOOP_DUR}s" repeatCount="indefinite" ` +
        `keyTimes="0;${fmt(arrive)};${fmt(arrive + dur * 3)};1" values="0;1;1;0"/>` +
        `</circle>\n`;
    }
  }
  return { bullets, blasts };
}

function buildStars(theme) {
  const pts = [
    [8, 20, 1.2], [8, 60, 1.6], [8, 100, 2.0],
    [505, 25, 1.2], [505, 70, 1.6], [505, 110, 2.0],
    [30, 164, 1.2], [483, 164, 1.6],
  ];
  return pts.map(([x, y, dur]) =>
    `<circle cx="${x}" cy="${y}" r="1.1" fill="${theme.starColor}"><animate attributeName="opacity" values="0.2;1;0.2" dur="${dur}s" repeatCount="indefinite"/></circle>`
  ).join("\n");
}

function buildJet(theme) {
  return `<g id="jet">
  <g transform="translate(0,0)">
    <polygon points="0,-16 8,6 4,3 -4,3 -8,6" fill="${theme.jetBody}" stroke="${theme.jetStroke}" stroke-width="1"/>
    <polygon points="-8,6 -14,12 -4,7" fill="${theme.jetWing}"/>
    <polygon points="8,6 14,12 4,7" fill="${theme.jetWing}"/>
    <circle cx="0" cy="-6" r="2.2" fill="${theme.jetCockpit}"/>
    <polygon points="-3,7 3,7 0,15" fill="${theme.jetFlame}">
      <animate attributeName="opacity" values="0.5;1;0.6;1" dur="0.18s" repeatCount="indefinite"/>
    </polygon>
  </g>
  <animateTransform attributeName="transform" attributeType="XML" type="translate"
    dur="${LOOP_DUR}s" repeatCount="indefinite"
    keyTimes="0;0.5;1"
    values="${JET_X_START}.00,140.00;${JET_X_END}.00,140.00;${JET_X_START}.00,140.00"/>
</g>`;
}

function generateSvgContent(weeks, themeName) {
  const theme = THEMES[themeName];
  const cells = buildCells(weeks, themeName);
  const targets = pickTargets(cells);
  const { bullets, blasts } = buildBulletsAndBlasts(targets, theme);

  return `<svg viewBox="0 0 ${WIDTH} ${HEIGHT}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GitHub Jet Heatmap for ${USERNAME}">
<rect x="0.5" y="0.5" width="${WIDTH - 1}" height="${HEIGHT - 1}" rx="8" fill="${theme.bg}" stroke="${theme.cardBorder}"/>
${buildStars(theme)}
<g id="grid">
${buildGrid(cells, targets, theme)}</g>
<g id="bullets">
${bullets}</g>
<g id="blasts">
${blasts}</g>
${buildJet(theme)}
</svg>
`;
}

async function main() {
  console.log(`Fetching contribution calendar for ${USERNAME}...`);
  const { weeks, isGql } = await fetchWeeks();
  console.log(`Successfully fetched ${weeks.length} weeks of contributions (source: ${isGql ? "GraphQL" : "Public API"}).`);

  // Ensure output dirs
  const outDir = path.resolve(".");
  const distDir = path.resolve("dist");
  fs.mkdirSync(distDir, { recursive: true });

  const darkSvg = generateSvgContent(weeks, "dark");
  const lightSvg = generateSvgContent(weeks, "light");

  // Write root files
  fs.writeFileSync(path.join(outDir, "dark.svg"), darkSvg, "utf8");
  fs.writeFileSync(path.join(outDir, "light.svg"), lightSvg, "utf8");

  // Also write dist/ copies
  fs.writeFileSync(path.join(distDir, "dark.svg"), darkSvg, "utf8");
  fs.writeFileSync(path.join(distDir, "light.svg"), lightSvg, "utf8");
  fs.writeFileSync(path.join(distDir, "github-jet.svg"), darkSvg, "utf8");

  console.log("Generated:");
  console.log("  - dark.svg");
  console.log("  - light.svg");
  console.log("  - dist/dark.svg");
  console.log("  - dist/light.svg");
  console.log("  - dist/github-jet.svg");
}

main().catch((err) => {
  console.error("Fatal error generating jet animation:", err);
  process.exit(1);
});
