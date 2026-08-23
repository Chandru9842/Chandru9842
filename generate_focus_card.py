#!/usr/bin/env python3
"""
Ultra-Sleek Current Focus & Engineering Objectives Card Generator for Chandru M (@Chandru9842).
- Renders high-end glowing glassmorphism SVG card with dual-column architecture.
- Displays Active Engineering, Core Mastery, Cloud Architecture, and Career Status.
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

FOCUS_DATA = {
    "mastering": [
        {"title": "System Design & Distributed Systems", "desc": "Scalability, Caching, Event-Driven", "badge": "CORE"},
        {"title": "Docker & Containerization", "desc": "Multi-stage builds, Container Orchestration", "badge": "DEVOPS"},
        {"title": "Spring Boot & Security", "desc": "Microservices, JWT, OAuth2 Auth Flows", "badge": "BACKEND"},
        {"title": "Advanced DSA & Algorithms", "desc": "Problem Solving, Optimization, Complexity", "badge": "LEETCODE"}
    ],
    "engineering": [
        {"title": "AI Resume Analyzer & Parser", "desc": "Intelligent LLM Semantic Scoring Pipeline", "badge": "ACTIVE"},
        {"title": "Developer CMS Platform", "desc": "High-throughput modern portfolio engine", "badge": "BUILDING"},
        {"title": "Cloud CI/CD & Deployments", "desc": "Automated pipelines on Docker & Cloudflare", "badge": "INFRA"},
        {"title": "Open to New Opportunities", "desc": "Full Stack & Backend Engineering roles", "badge": "OPEN"}
    ]
}

def build_focus_svg(theme="dark"):
    is_dark = (theme == "dark")
    
    bg = "#0B1120" if is_dark else "#FFFFFF"
    card_bg = "#0F172A" if is_dark else "#F8FAFC"
    column_bg = "rgba(30, 41, 59, 0.6)" if is_dark else "rgba(241, 245, 249, 0.9)"
    column_border = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.06)"
    border = "rgba(56, 189, 248, 0.35)" if is_dark else "rgba(2, 132, 199, 0.25)"
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    accent_cyan = "#38BDF8" if is_dark else "#0284C7"
    accent_emerald = "#10B981" if is_dark else "#059669"
    accent_purple = "#818CF8" if is_dark else "#4F46E5"
    accent_pink = "#F472B6" if is_dark else "#DB2777"

    # Build Left Column Items (Mastering)
    left_items = []
    y_pos = 18
    for item in FOCUS_DATA["mastering"]:
        left_items.append(f"""
        <g transform="translate(16, {y_pos})">
          <circle cx="6" cy="10" r="3.5" fill="{accent_cyan}"/>
          <text x="16" y="14" class="font-sans" font-size="12.5px" font-weight="700" fill="{text_primary}">{esc(item['title'])}</text>
          <text x="16" y="28" class="font-mono" font-size="10.5px" font-weight="600" fill="{text_secondary}">{esc(item['desc'])}</text>
          <g transform="translate(300, 2)">
            <rect width="48" height="18" rx="4" fill="{accent_cyan}" fill-opacity="0.15" stroke="{accent_cyan}" stroke-width="0.8"/>
            <text x="24" y="12.5" class="font-mono" font-size="8.5px" font-weight="700" fill="{accent_cyan}" text-anchor="middle">{item['badge']}</text>
          </g>
        </g>
        """)
        y_pos += 42

    # Build Right Column Items (Engineering)
    right_items = []
    y_pos = 18
    for item in FOCUS_DATA["engineering"]:
        badge_color = accent_emerald if item['badge'] in ['ACTIVE', 'OPEN'] else accent_purple
        right_items.append(f"""
        <g transform="translate(16, {y_pos})">
          <circle cx="6" cy="10" r="3.5" fill="{badge_color}"/>
          <text x="16" y="14" class="font-sans" font-size="12.5px" font-weight="700" fill="{text_primary}">{esc(item['title'])}</text>
          <text x="16" y="28" class="font-mono" font-size="10.5px" font-weight="600" fill="{text_secondary}">{esc(item['desc'])}</text>
          <g transform="translate(300, 2)">
            <rect width="48" height="18" rx="4" fill="{badge_color}" fill-opacity="0.15" stroke="{badge_color}" stroke-width="0.8"/>
            <text x="24" y="12.5" class="font-mono" font-size="8.5px" font-weight="700" fill="{badge_color}" text-anchor="middle">{item['badge']}</text>
          </g>
        </g>
        """)
        y_pos += 42

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="790" height="280" viewBox="0 0 790 280" role="img" aria-label="Current Focus and Objectives Dashboard">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif; }}
      .font-mono {{ font-family: 'Segoe UI', Ubuntu, monospace; }}
    </style>
    <linearGradient id="focusGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{card_bg}"/>
      <stop offset="100%" stop-color="{bg}"/>
    </linearGradient>
    <linearGradient id="glowTop" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F472B6"/>
      <stop offset="50%" stop-color="#818CF8"/>
      <stop offset="100%" stop-color="#22D3EE"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="790" height="280" rx="16" fill="url(#focusGrad)" stroke="{border}" stroke-width="1.5"/>
  <rect x="0" y="0" width="790" height="3" fill="url(#glowTop)" rx="1.5"/>

  <!-- Header Header Telemetry -->
  <g transform="translate(32, 24)">
    <circle cx="8" cy="14" r="5" fill="{accent_pink}">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="22" y="19" class="font-sans" font-size="15.5px" font-weight="800" fill="{text_primary}">🎯 CURRENT FOCUS &amp; ENGINEERING OBJECTIVES</text>
    <text x="22" y="34" class="font-mono" font-size="10.5px" font-weight="600" fill="{text_secondary}">Active Technical Roadmaps // Core Engineering Vectors</text>

    <!-- Telemetry Status Badge -->
    <g transform="translate(605, 2)">
      <rect width="122" height="26" rx="7" fill="{accent_emerald}" fill-opacity="0.15" stroke="{accent_emerald}" stroke-width="1"/>
      <text x="61" y="17" class="font-mono" font-size="10px" font-weight="700" fill="{accent_emerald}" text-anchor="middle">ACTIVE MATRIX</text>
    </g>
  </g>

  <!-- Left Column Card: Core Mastery -->
  <g transform="translate(24, 76)">
    <rect width="362" height="184" rx="10" fill="{column_bg}" stroke="{column_border}" stroke-width="1.2"/>
    <g transform="translate(16, -10)">
      <rect width="144" height="20" rx="5" fill="{accent_cyan}" fill-opacity="0.2" stroke="{accent_cyan}" stroke-width="1"/>
      <text x="72" y="14" class="font-sans" font-size="10px" font-weight="800" fill="{accent_cyan}" text-anchor="middle">📚 CURRENTLY MASTERING</text>
    </g>
    {''.join(left_items)}
  </g>

  <!-- Right Column Card: Active Engineering -->
  <g transform="translate(404, 76)">
    <rect width="362" height="184" rx="10" fill="{column_bg}" stroke="{column_border}" stroke-width="1.2"/>
    <g transform="translate(16, -10)">
      <rect width="138" height="20" rx="5" fill="{accent_emerald}" fill-opacity="0.2" stroke="{accent_emerald}" stroke-width="1"/>
      <text x="69" y="14" class="font-sans" font-size="10px" font-weight="800" fill="{accent_emerald}" text-anchor="middle">🚀 ACTIVE ENGINEERING</text>
    </g>
    {''.join(right_items)}
  </g>

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

    print("Generated ultra-sleek Current Focus cards successfully!")

if __name__ == "__main__":
    main()
