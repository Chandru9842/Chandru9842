#!/usr/bin/env node
/**
 * Conway's Game of Life Contribution Automaton Generator for GitHub Profile
 * Simulates cellular automata evolution seeded from real GitHub commit density.
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
const GRID_Y = 52;
const WIDTH = 840;
const HEIGHT = 200;
const NUM_GENS = 8;
const DURATION = 16; // seconds per full loop

async function fetchContributions() {
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
        days.push(match && match.count > 0 ? 1 : 0);
      }

      // 2D matrix [row][col]
      const grid = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
      for (let c = 0; c < COLS; c++) {
        for (let r = 0; r < ROWS; r++) {
          const idx = c * 7 + r;
          grid[r][c] = days[idx] || 0;
        }
      }
      return grid;
    }
  } catch (err) {
    console.warn("Public API error:", err.message);
  }
  // Fallback random seed
  return Array.from({ length: ROWS }, () =>
    Array.from({ length: COLS }, () => (Math.random() > 0.65 ? 1 : 0))
  );
}

// Conway's Game of Life simulation step
function getNextGeneration(current) {
  const next = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      let neighbors = 0;
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (dr === 0 && dc === 0) continue;
          const nr = (r + dr + ROWS) % ROWS;
          const nc = (c + dc + COLS) % COLS;
          neighbors += current[nr][nc];
        }
      }
      if (current[r][c] === 1) {
        next[r][c] = neighbors === 2 || neighbors === 3 ? 1 : 0;
      } else {
        next[r][c] = neighbors === 3 ? 1 : 0;
      }
    }
  }
  return next;
}

function buildGameOfLifeSVG(theme, initialGrid) {
  const isDark = theme === "dark";
  const bg = isDark ? "#030712" : "#FFFFFF";
  const border = isDark ? "rgba(34, 211, 238, 0.25)" : "rgba(37, 99, 235, 0.2)";
  const cellDead = isDark ? "#0F172A" : "#F1F5F9";
  const cellLive1 = isDark ? "#22D3EE" : "#0284C7"; // Cyan
  const cellLive2 = isDark ? "#10B981" : "#059669"; // Emerald
  const cellLive3 = isDark ? "#A855F7" : "#7C3AED"; // Purple
  const textPrimary = isDark ? "#F8FAFC" : "#0F172A";
  const textMuted = isDark ? "#64748B" : "#94A3B8";

  // Simulate NUM_GENS generations
  const generations = [initialGrid];
  for (let g = 1; g < NUM_GENS; g++) {
    generations.push(getNextGeneration(generations[g - 1]));
  }

  // Build keytimes and cell values
  let cellsSVG = "";
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const x = GRID_X + c * STEP;
      const y = GRID_Y + r * STEP;

      // Extract states across generations
      const states = generations.map((gen) => gen[r][c]);
      states.push(states[0]); // loop back to 0

      const opacityValues = states
        .map((s) => (s === 1 ? "0.95" : "0.22"))
        .join(";");
      const colorValues = states
        .map((s) => (s === 1 ? ((r + c) % 2 === 0 ? cellLive1 : cellLive2) : cellDead))
        .join(";");

      cellsSVG += `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="2.5" fill="${colorValues.split(";")[0]}" opacity="${opacityValues.split(";")[0]}">
        <animate attributeName="opacity" values="${opacityValues}" dur="${DURATION}s" repeatCount="indefinite"/>
        <animate attributeName="fill" values="${colorValues}" dur="${DURATION}s" repeatCount="indefinite"/>
      </rect>\n`;
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="Conway's Game of Life Contribution Automaton">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&amp;display=swap');
      .mono-title { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; }
      .mono-dim { font-family: 'JetBrains Mono', monospace; font-size: 8.5px; font-weight: 500; }
    </style>
    <linearGradient id="cyberBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#A855F7" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#10B981" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="scanBeam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
      <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Container Box -->
  <rect width="${WIDTH}" height="${HEIGHT}" rx="12" fill="${bg}" stroke="${border}" stroke-width="1.2"/>

  <!-- Top Simulation HUD Bar -->
  <g transform="translate(50, 28)">
    <text x="0" y="0" class="mono-title" fill="#22D3EE">🧬 CONWAY'S GAME OF LIFE // CELLULAR AUTOMATON</text>
    <text x="740" y="0" text-anchor="end" class="mono-dim" fill="${textMuted}">SEED: ${USERNAME} COMMITS • 8 GENS</text>
  </g>

  <!-- Simulation Grid Frame -->
  <rect x="${GRID_X - 8}" y="${GRID_Y - 8}" width="${COLS * STEP + 10}" height="${ROWS * STEP + 10}" rx="6" fill="none" stroke="${border}" stroke-width="1.5"/>

  <!-- Cellular Automata Grid -->
  <g>
${cellsSVG}
  </g>

  <!-- Scanning Sweep Line -->
  <rect x="42" y="${GRID_Y - 8}" width="60" height="${ROWS * STEP + 10}" fill="url(#scanBeam)">
    <animateTransform attributeName="transform" type="translate" from="-60 0" to="720 0" dur="4s" repeatCount="indefinite"/>
  </rect>

  <!-- Bottom Stats HUD -->
  <g transform="translate(50, 182)">
    <circle cx="4" cy="-3" r="3.5" fill="#10B981"><animate attributeName="opacity" values="1;0.3;1" dur="1.2s" repeatCount="indefinite"/></circle>
    <text x="14" y="0" class="mono-dim" fill="#10B981">SIMULATION RUNNING</text>
    <text x="360" y="0" text-anchor="middle" class="mono-dim" fill="${textMuted}">RULE: B3/S23 (CONWAY STANDARD)</text>
    <text x="740" y="0" text-anchor="end" class="mono-dim" fill="#A855F7">EVOLUTION: CYCLIC SMIL</text>
  </g>
</svg>
`;
}

async function main() {
  console.log(`Generating Conway's Game of Life Contribution Automaton for ${USERNAME}...`);
  const initialGrid = await fetchContributions();

  const distDir = path.resolve("dist");
  if (!fs.existsSync(distDir)) fs.mkdirSync(distDir, { recursive: true });

  const darkSVG = buildGameOfLifeSVG("dark", initialGrid);
  const lightSVG = buildGameOfLifeSVG("light", initialGrid);

  fs.writeFileSync(path.join(distDir, "game-of-life-dark.svg"), darkSVG, "utf-8");
  fs.writeFileSync(path.join(distDir, "game-of-life-light.svg"), lightSVG, "utf-8");
  fs.writeFileSync(path.join(distDir, "game-of-life.svg"), darkSVG, "utf-8");

  console.log("Successfully generated Conway's Game of Life SVGs in dist/!");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
