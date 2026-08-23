#!/usr/bin/env python3
"""
Professional Current Focus & Objectives Card Generator for Chandru M (@Chandru9842).
- Designed in the exact typography, color palette, and layout of GitHub Developer Stats (Ocean Theme) and Terminal Telemetry (Pic 2 & Pic 3).
- Uses 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, Roboto, sans-serif.
- Clean dotted leader alignment, strictly non-overlapping column bounds.
- Supports both dark and light modes.
"""

import os
import sys
import xml.sax.saxutils as saxutils

OUTPUT_DARK = "assets/focus-card-dark.svg"
OUTPUT_LIGHT = "assets/focus-card-light.svg"
OUTPUT_MAIN = "assets/focus-card.svg"

def esc(text):
    return saxutils.escape(str(text))

FOCUS_ITEMS_LEFT = [
    ("System Design", "Distributed Systems, Caching, Event Queues"),
    ("Containerization", "Docker, Multi-Stage Builds, CI/CD Pipelines"),
    ("Enterprise Java", "Spring Boot 3, Spring Security, OAuth2/JWT"),
    ("Algorithmic Mastery", "Advanced DSA, Dynamic Programming, Graphs")
]

FOCUS_ITEMS_RIGHT = [
    ("AI Resume Parser", "LLM Semantic Analysis & Scoring Pipeline"),
    ("Developer Platform", "Portfolio CMS & Modern Backend Engine"),
    ("Cloud Infrastructure", "Dockerized Services, Resilient Deployments"),
    ("Career Objective", "Full Stack & Backend Engineering Roles")
]

def build_focus_svg(theme="dark"):
    is_dark = (theme == "dark")
    
    bg = "#040F1D" if is_dark else "#FFFFFF"
    card_bg = "#0B1E3B" if is_dark else "#F8FAFC"
    border = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(15, 23, 42, 0.12)"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#8BB9FE" if is_dark else "#475569"
    text_dots = "#3B597E" if is_dark else "#CBD5E1"
    accent_cyan = "#00E8FF" if is_dark else "#0284C7"
    accent_emerald = "#10B981" if is_dark else "#059669"
    badge_bg = "rgba(0, 232, 255, 0.1)" if is_dark else "rgba(2, 132, 199, 0.1)"

    # Width: 880 to ensure zero overlap between columns
    # Left column: x = 28 to 430
    # Right column: x = 450 to 852
    left_rows = []
    y_pos = 96
    for key, val in FOCUS_ITEMS_LEFT:
        left_rows.append(f"""
        <g transform="translate(28, {y_pos})">
          <circle cx="4" cy="5" r="3.5" fill="{accent_cyan}"/>
          <text x="14" y="9" class="font-sans" font-size="12px" font-weight="600" fill="{text_secondary}">{esc(key)}</text>
          <text x="135" y="9" class="font-mono" font-size="11px" fill="{text_dots}">: . .</text>
          <text x="165" y="9" class="font-sans" font-size="11.5px" font-weight="600" fill="{text_primary}">{esc(val)}</text>
        </g>
        """)
        y_pos += 32

    right_rows = []
    y_pos = 96
    for key, val in FOCUS_ITEMS_RIGHT:
        right_rows.append(f"""
        <g transform="translate(450, {y_pos})">
          <circle cx="4" cy="5" r="3.5" fill="{accent_emerald}"/>
          <text x="14" y="9" class="font-sans" font-size="12px" font-weight="600" fill="{text_secondary}">{esc(key)}</text>
          <text x="135" y="9" class="font-mono" font-size="11px" fill="{text_dots}">: . .</text>
          <text x="165" y="9" class="font-sans" font-size="11.5px" font-weight="600" fill="{text_primary}">{esc(val)}</text>
        </g>
        """)
        y_pos += 32

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="236" viewBox="0 0 880 236" role="img" aria-label="Current Focus and Objectives">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Roboto, sans-serif; }}
      .font-mono {{ font-family: 'Consolas', 'Courier New', 'Fira Code', 'JetBrains Mono', monospace; }}
    </style>
    <linearGradient id="focusCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{card_bg}"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="880" height="236" rx="12" fill="url(#focusCardBg)" stroke="{border}" stroke-width="1.2"/>

  <!-- Header Section (Matching Pic 2 Header) -->
  <g transform="translate(28, 22)">
    <circle cx="6" cy="11" r="4.5" fill="{accent_cyan}"/>
    <text x="18" y="15" class="font-sans" font-size="15px" font-weight="700" fill="{accent_cyan}">Current Focus &amp; Objectives</text>
    <text x="210" y="15" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">// Technical Vectors &amp; Active Roadmaps</text>

    <!-- Status Badge -->
    <g transform="translate(720, 0)">
      <rect width="94" height="24" rx="6" fill="{badge_bg}" stroke="{accent_cyan}" stroke-width="0.8"/>
      <text x="47" y="16" class="font-mono" font-size="10px" font-weight="700" fill="{accent_cyan}" text-anchor="middle">ACTIVE</text>
    </g>
  </g>

  <!-- Divider -->
  <line x1="28" y1="56" x2="852" y2="56" stroke="{border}" stroke-width="1"/>

  <!-- Column Headers -->
  <g transform="translate(28, 72)">
    <text x="0" y="0" class="font-sans" font-size="12px" font-weight="700" fill="{accent_cyan}" letter-spacing="0.5px">📚 CURRENTLY MASTERING</text>
  </g>
  <g transform="translate(450, 72)">
    <text x="0" y="0" class="font-sans" font-size="12px" font-weight="700" fill="{accent_emerald}" letter-spacing="0.5px">🚀 ACTIVE ENGINEERING</text>
  </g>

  <!-- Left Column Items -->
  {''.join(left_rows)}

  <!-- Right Column Items -->
  {''.join(right_rows)}

</svg>
'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    dark_svg = build_focus_svg("dark")
    light_svg = build_focus_svg("light")

    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(OUTPUT_MAIN, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print("Generated professional non-overlapping Current Focus card successfully!")

if __name__ == "__main__":
    main()
