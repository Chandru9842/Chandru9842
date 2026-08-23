#!/usr/bin/env python3
"""
Ultra-Sleek Connect & Developer Collaboration Hub Generator for Chandru M (@Chandru9842).
- Renders high-end glowing glassmorphism SVG card with direct action buttons.
- Connects LinkedIn, GitHub, Gmail, LeetCode, and GeeksforGeeks with glowing pill designs.
- Strictly valid XML.
- Supports both dark and light modes.
"""

import os
import sys

OUTPUT_DARK = "assets/connect-card-dark.svg"
OUTPUT_LIGHT = "assets/connect-card-light.svg"
OUTPUT_MAIN = "assets/connect-card.svg"

SOCIAL_BUTTONS = [
    {"label": "LINKEDIN", "handle": "in/chandru9842", "color": "#0A66C2", "icon_color": "#38BDF8"},
    {"label": "GMAIL", "handle": "chandrumohan550", "color": "#EA4335", "icon_color": "#F87171"},
    {"label": "GITHUB", "handle": "@Chandru9842", "color": "#7C3AED", "icon_color": "#A78BFA"},
    {"label": "LEETCODE", "handle": "@Chandrum06", "color": "#FFA116", "icon_color": "#FCD34D"},
    {"label": "GFG", "handle": "@chandrum06", "color": "#2F8D46", "icon_color": "#34D399"}
]

def build_connect_svg(theme="dark"):
    is_dark = (theme == "dark")
    
    bg = "#0B1120" if is_dark else "#FFFFFF"
    card_bg = "#0F172A" if is_dark else "#F8FAFC"
    border = "rgba(56, 189, 248, 0.35)" if is_dark else "rgba(2, 132, 199, 0.25)"
    btn_bg = "#1E293B" if is_dark else "#E2E8F0"
    btn_border = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.08)"
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    accent_emerald = "#10B981" if is_dark else "#059669"

    # Build 5 social connection badges
    buttons = []
    x_start = 24
    btn_w = 142
    for idx, b in enumerate(SOCIAL_BUTTONS):
        bx = x_start + (idx * (btn_w + 8))
        color = b["color"]
        label = b["label"]
        handle = b["handle"]

        buttons.append(f"""
        <g transform="translate({bx}, 78)">
          <rect width="{btn_w}" height="48" rx="10" fill="{btn_bg}" stroke="{btn_border}" stroke-width="1.2"/>
          <rect x="0" y="0" width="4" height="48" rx="2" fill="{color}"/>
          <text x="14" y="20" class="font-mono" font-size="10.5px" font-weight="800" fill="{color}">{label}</text>
          <text x="14" y="36" class="font-sans" font-size="11.5px" font-weight="700" fill="{text_primary}">{handle}</text>
        </g>
        """)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="790" height="186" viewBox="0 0 790 186" role="img" aria-label="Connect and Developer Collaboration Hub">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif; }}
      .font-mono {{ font-family: 'Segoe UI', Ubuntu, monospace; }}
    </style>
    <linearGradient id="connectGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{card_bg}"/>
      <stop offset="100%" stop-color="{bg}"/>
    </linearGradient>
    <linearGradient id="glowBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0A66C2"/>
      <stop offset="25%" stop-color="#7C3AED"/>
      <stop offset="50%" stop-color="#FFA116"/>
      <stop offset="75%" stop-color="#2F8D46"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="790" height="186" rx="16" fill="url(#connectGrad)" stroke="{border}" stroke-width="1.5"/>
  <rect x="0" y="0" width="790" height="3" fill="url(#glowBar)" rx="1.5"/>

  <!-- Header Telemetry -->
  <g transform="translate(32, 24)">
    <circle cx="8" cy="14" r="5" fill="{accent_emerald}">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="22" y="19" class="font-sans" font-size="15px" font-weight="800" fill="{text_primary}">📫 LET&apos;S CONNECT &amp; COLLABORATE</text>
    <text x="22" y="34" class="font-mono" font-size="10.5px" font-weight="600" fill="{text_secondary}">Open for Full Stack &amp; Backend Engineering roles // Networking &amp; Research</text>

    <!-- Available Status Badge -->
    <g transform="translate(605, 2)">
      <rect width="122" height="26" rx="7" fill="{accent_emerald}" fill-opacity="0.15" stroke="{accent_emerald}" stroke-width="1"/>
      <text x="61" y="17" class="font-mono" font-size="10px" font-weight="700" fill="{accent_emerald}" text-anchor="middle">OPEN TO WORK</text>
    </g>
  </g>

  <!-- Social Link Badges -->
  {''.join(buttons)}

  <!-- Footer Philosophy -->
  <g transform="translate(395, 156)">
    <text x="0" y="0" class="font-sans" font-size="11px" font-style="italic" font-weight="600" fill="{text_muted}" text-anchor="middle">&quot;Great software is not just about writing code &#8212; it&apos;s about solving real problems with simplicity and scalability.&quot;</text>
  </g>
</svg>
'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    dark_svg = build_connect_svg("dark")
    light_svg = build_connect_svg("light")

    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(OUTPUT_MAIN, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print("Generated ultra-sleek Connect hub cards successfully!")

if __name__ == "__main__":
    main()
