#!/usr/bin/env node
/**
 * Pac-Man Contribution Heatmap Generator for GitHub Profile
 * Generates animated retro-arcade SVGs with real user contribution data.
 */

import fs from "node:fs";
import path from "node:path";

const USERNAME = process.env.GH_USERNAME || "Chandru9842";
const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;

const COLS = 46;
const ROWS = 7;
const CELL = 12;
const GAP = 3;
const STEP = CELL + GAP;
const GRID_X = 50;
const GRID_Y = 48;
const WIDTH = 840;
const HEIGHT = 200;

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
        "User-Agent": "pacman-generator",
      },
      body: JSON.stringify({ query: GRAPHQL_QUERY, variables: { login: USERNAME } }),
    });
    const json = await res.json();
    const weeks = json?.data?.user?.contributionsCollection?.contributionCalendar?.weeks;
    if (Array.isArray(weeks) && weeks.length > 0) return weeks;
  } catch (err) {
    console.warn("GraphQL error:", err.message);
  }
  return null;
}

async function fetchFromPublicAPI() {
  try {
    const res = await fetch(`https://github-contributions-api.jogruber.de/v4/${USERNAME}?y=last`);
    const json = await res.json();
    if (json?.contributions && Array.isArray(json.contributions)) {
      const byDate = new Map();
      for (const item of json.contributions) byDate.set(item.date, item);

      const days = [];
      const end = new Date();
      const start = new Date(end);
      start.setDate(start.getDate() - COLS * 7);

      for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
        const key = d.toISOString().slice(0, 10);
        const match = byDate.get(key);
        days.push({
          date: key,
          contributionCount: match ? match.count : 0,
          color: match ? match.level : 0,
        });
      }

      const weeks = [];
      for (let i = 0; i < days.length; i += 7) {
        weeks.push({ contributionDays: days.slice(i, i + 7) });
      }
      return weeks;
    }
  } catch (err) {
    console.warn("Public API error:", err.message);
  }
  return null;
}

function buildPacmanSVG(theme, weeks) {
  const isDark = theme === "dark";
  const bg = isDark ? "#0D1117" : "#FFFFFF";
  const border = isDark ? "rgba(255, 255, 255, 0.12)" : "rgba(0, 0, 0, 0.12)";
  const textPrimary = isDark ? "#F0F6FC" : "#1F2328";
  const textSecondary = isDark ? "#8B949E" : "#656D76";
  const gridEmpty = isDark ? "#161B22" : "#EBEDF0";
  const mazeWall = isDark ? "#1F6FEB" : "#0969DA";

  // Flatten last COLS weeks
  const displayWeeks = (weeks || []).slice(-COLS);
  while (displayWeeks.length < COLS) {
    displayWeeks.unshift({ contributionDays: Array(7).fill({ contributionCount: 0 }) });
  }

  // Generate Grid Pellets & Tiles
  let tilesSVG = "";
  let totalScore = 0;
  for (let c = 0; c < COLS; c++) {
    const days = displayWeeks[c]?.contributionDays || [];
    for (let r = 0; r < ROWS; r++) {
      const count = days[r]?.contributionCount || 0;
      totalScore += count * 10;
      const x = GRID_X + c * STEP;
      const y = GRID_Y + r * STEP;

      let cellColor = gridEmpty;
      if (count >= 10) cellColor = isDark ? "#39D353" : "#216E39";
      else if (count >= 5) cellColor = isDark ? "#26A641" : "#30A14E";
      else if (count >= 2) cellColor = isDark ? "#006D32" : "#40C463";
      else if (count >= 1) cellColor = isDark ? "#0E4429" : "#9BE9A8";

      // Background Grid Tile
      tilesSVG += `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="2.5" fill="${cellColor}" opacity="${count > 0 ? "0.9" : "0.35"}"/>\n`;

      // Food Pellet for Pac-Man
      if (count > 0) {
        tilesSVG += `<circle cx="${x + CELL / 2}" cy="${y + CELL / 2}" r="2" fill="#FFE600">
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" begin="${(c * 0.1).toFixed(1)}s" repeatCount="indefinite"/>
        </circle>\n`;
      }
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="Pac-Man Contribution Heatmap">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&amp;family=JetBrains+Mono:wght@700&amp;display=swap');
      .arcade-font { font-family: 'Press Start 2P', monospace; }
      .mono-font { font-family: 'JetBrains Mono', monospace; font-weight: 700; }
    </style>
    <!-- Pac-Man Chomp Shapes -->
    <path id="pacmanChomp" d="M 0 0 L 10 -8 A 12 12 0 1 0 10 8 Z" fill="#FFE600"/>
    
    <!-- Retro Ghost Shape -->
    <g id="ghostBlinky">
      <path d="M -8 6 L -8 -2 A 8 8 0 0 1 8 -2 L 8 6 L 5 4 L 2 6 L -1 4 L -4 6 L -8 4 Z" fill="#FF0000"/>
      <circle cx="-3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="-2" cy="-2" r="1.2" fill="#0000FF"/>
      <circle cx="3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="4" cy="-2" r="1.2" fill="#0000FF"/>
    </g>
    <g id="ghostPinky">
      <path d="M -8 6 L -8 -2 A 8 8 0 0 1 8 -2 L 8 6 L 5 4 L 2 6 L -1 4 L -4 6 L -8 4 Z" fill="#FFB8FF"/>
      <circle cx="-3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="-2" cy="-2" r="1.2" fill="#0000FF"/>
      <circle cx="3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="4" cy="-2" r="1.2" fill="#0000FF"/>
    </g>
    <g id="ghostInky">
      <path d="M -8 6 L -8 -2 A 8 8 0 0 1 8 -2 L 8 6 L 5 4 L 2 6 L -1 4 L -4 6 L -8 4 Z" fill="#00FFFF"/>
      <circle cx="-3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="-2" cy="-2" r="1.2" fill="#0000FF"/>
      <circle cx="3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="4" cy="-2" r="1.2" fill="#0000FF"/>
    </g>
    <g id="ghostClyde">
      <path d="M -8 6 L -8 -2 A 8 8 0 0 1 8 -2 L 8 6 L 5 4 L 2 6 L -1 4 L -4 6 L -8 4 Z" fill="#FFB852"/>
      <circle cx="-3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="-2" cy="-2" r="1.2" fill="#0000FF"/>
      <circle cx="3" cy="-2" r="2.5" fill="#FFFFFF"/><circle cx="4" cy="-2" r="1.2" fill="#0000FF"/>
    </g>
  </defs>

  <!-- Container Box -->
  <rect width="${WIDTH}" height="${HEIGHT}" rx="12" fill="${bg}" stroke="${border}" stroke-width="1.2"/>

  <!-- Top Arcade HUD -->
  <g transform="translate(50, 26)">
    <text x="0" y="0" class="arcade-font" font-size="8.5px" fill="#FF0000">1UP</text>
    <text x="0" y="12" class="arcade-font" font-size="8.5px" fill="${textPrimary}">00${totalScore || 2480}</text>
    
    <text x="280" y="0" class="arcade-font" font-size="8.5px" fill="#FF0000" text-anchor="middle">HIGH SCORE</text>
    <text x="280" y="12" class="arcade-font" font-size="8.5px" fill="${textPrimary}" text-anchor="middle">99990</text>
    
    <text x="690" y="6" class="arcade-font" font-size="8.5px" fill="#00FFFF" text-anchor="end">PAC-MAN HEATMAP</text>
  </g>

  <!-- Maze Grid Bounds -->
  <rect x="${GRID_X - 10}" y="${GRID_Y - 8}" width="${COLS * STEP + 14}" height="${ROWS * STEP + 10}" rx="6" fill="none" stroke="${mazeWall}" stroke-width="2" opacity="0.65"/>

  <!-- Contribution Tiles & Pellets -->
  <g>
${tilesSVG}
  </g>

  <!-- Animated Pac-Man & Ghost Chase Across the Rows -->
  <g transform="translate(0, 0)">
    <!-- Path Animation for Pac-Man -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="
          ${GRID_X - 25} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP + 20} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP + 20} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 25} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 25} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X + COLS * STEP + 20} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X - 25} ${GRID_Y + 1 * STEP + 6}
        "
        keyTimes="0; 0.30; 0.33; 0.63; 0.66; 0.96; 1"
        dur="18s" repeatCount="indefinite"/>
      
      <!-- Pacman Character with Chomping Animation -->
      <use href="#pacmanChomp">
        <animateTransform attributeName="transform" type="scale" values="1 1; 1 0.2; 1 1" dur="0.25s" repeatCount="indefinite"/>
      </use>
    </g>

    <!-- Ghosts Chasing Pac-Man -->
    <!-- Blinky -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="
          ${GRID_X - 55} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 10} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 10} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 55} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 55} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X + COLS * STEP - 10} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X - 55} ${GRID_Y + 1 * STEP + 6}
        "
        keyTimes="0; 0.30; 0.33; 0.63; 0.66; 0.96; 1"
        dur="18s" repeatCount="indefinite"/>
      <use href="#ghostBlinky"/>
    </g>

    <!-- Pinky -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="
          ${GRID_X - 80} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 35} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 35} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 80} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 80} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X + COLS * STEP - 35} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X - 80} ${GRID_Y + 1 * STEP + 6}
        "
        keyTimes="0; 0.30; 0.33; 0.63; 0.66; 0.96; 1"
        dur="18s" repeatCount="indefinite"/>
      <use href="#ghostPinky"/>
    </g>

    <!-- Inky -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="
          ${GRID_X - 105} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 60} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 60} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 105} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 105} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X + COLS * STEP - 60} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X - 105} ${GRID_Y + 1 * STEP + 6}
        "
        keyTimes="0; 0.30; 0.33; 0.63; 0.66; 0.96; 1"
        dur="18s" repeatCount="indefinite"/>
      <use href="#ghostInky"/>
    </g>

    <!-- Clyde -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="
          ${GRID_X - 130} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 85} ${GRID_Y + 1 * STEP + 6};
          ${GRID_X + COLS * STEP - 85} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 130} ${GRID_Y + 3 * STEP + 6};
          ${GRID_X - 130} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X + COLS * STEP - 85} ${GRID_Y + 5 * STEP + 6};
          ${GRID_X - 130} ${GRID_Y + 1 * STEP + 6}
        "
        keyTimes="0; 0.30; 0.33; 0.63; 0.66; 0.96; 1"
        dur="18s" repeatCount="indefinite"/>
      <use href="#ghostClyde"/>
    </g>
  </g>

  <!-- Bottom Retro Fruit & Lives Bar -->
  <g transform="translate(50, 182)">
    <!-- Pac-Man Lives Icons -->
    <circle cx="6" cy="0" r="5" fill="#FFE600"/>
    <circle cx="20" cy="0" r="5" fill="#FFE600"/>
    <circle cx="34" cy="0" r="5" fill="#FFE600"/>
    <text x="50" y="4" class="arcade-font" font-size="7px" fill="${textSecondary}">LIVES: 3</text>
    
    <!-- Cherry Bonus Fruit -->
    <g transform="translate(710, -5)">
      <circle cx="0" cy="4" r="3.5" fill="#FF0000"/>
      <circle cx="6" cy="4" r="3.5" fill="#FF0000"/>
      <path d="M 0 2 Q 3 -4 7 -6 Q 4 -2 6 2" stroke="#8B5A2B" stroke-width="1.2" fill="none"/>
    </g>
    <text x="698" y="4" class="arcade-font" font-size="7px" fill="#FFE600" text-anchor="end">LEVEL 1</text>
  </g>
</svg>
`;
}

async function main() {
  console.log(`Generating Pac-Man Contribution Heatmap for ${USERNAME}...`);
  let weeks = await fetchFromGraphQL();
  if (!weeks) weeks = await fetchFromPublicAPI();

  const distDir = path.resolve("dist");
  if (!fs.existsSync(distDir)) fs.mkdirSync(distDir, { recursive: true });

  const darkSVG = buildPacmanSVG("dark", weeks);
  const lightSVG = buildPacmanSVG("light", weeks);

  fs.writeFileSync(path.join(distDir, "pacman-dark.svg"), darkSVG, "utf-8");
  fs.writeFileSync(path.join(distDir, "pacman-light.svg"), lightSVG, "utf-8");
  fs.writeFileSync(path.join(distDir, "pacman.svg"), darkSVG, "utf-8");

  console.log("Successfully generated Pac-Man Heatmaps in dist/!");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
