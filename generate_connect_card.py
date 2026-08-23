#!/usr/bin/env python3
"""
Professional Connect & Developer Collaboration Card Generator for Chandru M (@Chandru9842).
- Designed in the exact typography, color palette, and layout of GitHub Developer Stats (Ocean Theme) and Terminal Telemetry (Pic 2 & Pic 3).
- Uses 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, Roboto, sans-serif.
- Clean dotted leader alignment, wide non-overlapping column bounds.
- Supports both dark and light modes.
"""

import os
import sys
import xml.sax.saxutils as saxutils

OUTPUT_DARK = "assets/connect-card-dark.svg"
OUTPUT_LIGHT = "assets/connect-card-light.svg"
OUTPUT_MAIN = "assets/connect-card.svg"

def esc(text):
    return saxutils.escape(str(text))

CONNECT_LINKS = [
    ("LinkedIn", "linkedin.com/in/chandru9842", "https://www.linkedin.com/in/chandru9842", "#00E8FF"),
    ("Gmail", "chandrumohan550@gmail.com", "mailto:chandrumohan550@gmail.com", "#F87171"),
    ("GitHub", "github.com/Chandru9842", "https://github.com/Chandru9842", "#A78BFA"),
    ("LeetCode", "leetcode.com/u/Chandrum06/", "https://leetcode.com/u/Chandrum06/", "#FFA116"),
    ("GeeksforGeeks", "geeksforgeeks.org/profile/chandrum06", "https://www.geeksforgeeks.org/profile/chandrum06", "#34D399")
]

def build_connect_svg(theme="dark"):
    is_dark = (theme == "dark")
    
    bg = "#040F1D" if is_dark else "#FFFFFF"
    card_bg = "#0B1E3B" if is_dark else "#F8FAFC"
    border = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(15, 23, 42, 0.12)"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#8BB9FE" if is_dark else "#475569"
    text_dots = "#3B597E" if is_dark else "#CBD5E1"
    text_muted = "#5B7CA3" if is_dark else "#94A3B8"
    accent_cyan = "#00E8FF" if is_dark else "#0284C7"
    accent_emerald = "#10B981" if is_dark else "#059669"
    badge_bg = "rgba(0, 232, 255, 0.1)" if is_dark else "rgba(2, 132, 199, 0.1)"

    left_rows = []
    y_pos = 78
    for name, handle, url, dot_col in CONNECT_LINKS[:3]:
        left_rows.append(f"""
        <g transform="translate(28, {y_pos})">
          <circle cx="4" cy="5" r="3.5" fill="{dot_col}"/>
          <text x="14" y="9" class="font-sans" font-size="12px" font-weight="600" fill="{text_secondary}">{esc(name)}</text>
          <text x="100" y="9" class="font-mono" font-size="11px" fill="{text_dots}">: . . .</text>
          <text x="140" y="9" class="font-sans" font-size="11.5px" font-weight="600" fill="{text_primary}">{esc(handle)}</text>
        </g>
        """)
        y_pos += 30

    right_rows = []
    y_pos = 78
    for name, handle, url, dot_col in CONNECT_LINKS[3:]:
        right_rows.append(f"""
        <g transform="translate(450, {y_pos})">
          <circle cx="4" cy="5" r="3.5" fill="{dot_col}"/>
          <text x="14" y="9" class="font-sans" font-size="12px" font-weight="600" fill="{text_secondary}">{esc(name)}</text>
          <text x="100" y="9" class="font-mono" font-size="11px" fill="{text_dots}">: . . .</text>
          <text x="140" y="9" class="font-sans" font-size="11.5px" font-weight="600" fill="{text_primary}">{esc(handle)}</text>
        </g>
        """)
        y_pos += 30

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="200" viewBox="0 0 880 200" role="img" aria-label="Connect and Developer Collaboration">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Roboto, sans-serif; }}
      .font-mono {{ font-family: 'Consolas', 'Courier New', 'Fira Code', 'JetBrains Mono', monospace; }}
    </style>
    <linearGradient id="connectCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{card_bg}"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="880" height="200" rx="12" fill="url(#connectCardBg)" stroke="{border}" stroke-width="1.2"/>

  <!-- Header Section (Matching Pic 2 Header) -->
  <g transform="translate(28, 22)">
    <circle cx="6" cy="11" r="4.5" fill="{accent_cyan}"/>
    <text x="18" y="15" class="font-sans" font-size="15px" font-weight="700" fill="{accent_cyan}">Connect &amp; Collaborate</text>
    <text x="180" y="15" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">// Open for Full Stack &amp; Backend Roles</text>

    <!-- Status Badge -->
    <g transform="translate(710, 0)">
      <rect width="112" height="24" rx="6" fill="{badge_bg}" stroke="{accent_cyan}" stroke-width="0.8"/>
      <text x="56" y="16" class="font-mono" font-size="10px" font-weight="700" fill="{accent_cyan}" text-anchor="middle">OPEN TO WORK</text>
    </g>
  </g>

  <!-- Divider -->
  <line x1="28" y1="56" x2="852" y2="56" stroke="{border}" stroke-width="1"/>

  <!-- Left Column Items -->
  {''.join(left_rows)}

  <!-- Right Column Items -->
  {''.join(right_rows)}

  <!-- Footer Philosophy -->
  <g transform="translate(440, 178)">
    <text x="0" y="0" class="font-sans" font-size="11.5px" font-weight="500" fill="{text_muted}" text-anchor="middle">&quot;Great software is not just about writing code &#8212; it&apos;s about solving real problems with simplicity and scalability.&quot;</text>
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

    print("Generated professional Connect card successfully!")

if __name__ == "__main__":
    main()
