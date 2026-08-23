#!/usr/bin/env python3
"""
Custom GeeksforGeeks Stats Card Generator for Chandru M (@chandrum06).
Matches the sleek dark/light aesthetic of LeetCard & ghstats.dev with 
accurate problem breakdowns, progress donut chart, coding score, and streak.
"""

import os
import math

USERNAME = "chandrum06"
NAME = "Chandru M"
COLLEGE = "SRM TRP Engineering College"

# Live Stats from GFG Profile
CODING_SCORE = 514
TOTAL_SOLVED = 168
SCHOOL = 0
BASIC = 26
EASY = 55
MEDIUM = 81
HARD = 6
STREAK = 1
POTD = 1

def build_gfg_card(theme="dark"):
    is_dark = (theme == "dark")

    bg = "#0B1120" if is_dark else "#FFFFFF"
    card_bg = "#0F172A" if is_dark else "#F8FAFC"
    border_color = "rgba(47, 141, 70, 0.35)" if is_dark else "rgba(47, 141, 70, 0.25)"
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    gfg_green = "#2F8D46"
    gfg_green_glow = "#34D399"
    color_basic = "#94A3B8"
    color_easy = "#10B981"
    color_medium = "#F59E0B"
    color_hard = "#EF4444"
    pill_bg = "#1E293B" if is_dark else "#EDF2F7"

    # SVG Ring Calculations (Radius = 46, Circumference = 289)
    R = 46
    C = 2 * math.pi * R  # ~289.02
    
    # Proportions
    p_basic = (BASIC / TOTAL_SOLVED) * C if TOTAL_SOLVED else 0
    p_easy = (EASY / TOTAL_SOLVED) * C if TOTAL_SOLVED else 0
    p_medium = (MEDIUM / TOTAL_SOLVED) * C if TOTAL_SOLVED else 0
    p_hard = (HARD / TOTAL_SOLVED) * C if TOTAL_SOLVED else 0

    off_hard = 0
    off_medium = p_hard
    off_easy = p_hard + p_medium
    off_basic = p_hard + p_medium + p_easy

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="300" viewBox="0 0 500 300" role="img" aria-label="Chandru M - GeeksforGeeks Stats">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&amp;family=JetBrains+Mono:wght@600;700;800&amp;display=swap');
      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
      .t-title {{ font-size: 16px; font-weight: 800; fill: {text_primary}; letter-spacing: -0.3px; }}
      .t-sub {{ font-size: 11px; font-weight: 600; fill: {text_secondary}; }}
      .t-num-big {{ font-size: 26px; font-weight: 800; fill: {text_primary}; }}
      .t-lbl-sm {{ font-size: 10px; font-weight: 600; fill: {text_muted}; letter-spacing: 0.5px; text-transform: uppercase; }}
      .t-diff-name {{ font-size: 12px; font-weight: 700; }}
      .t-diff-val {{ font-size: 12px; font-weight: 800; fill: {text_primary}; }}
      .t-bottom-num {{ font-size: 18px; font-weight: 800; fill: {text_primary}; }}
      .t-bottom-lbl {{ font-size: 10px; font-weight: 600; fill: {text_muted}; text-transform: uppercase; letter-spacing: 0.5px; }}
    </style>
    <linearGradient id="gfgGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{gfg_green}"/>
      <stop offset="100%" stop-color="{gfg_green_glow}"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="500" height="300" rx="16" fill="{bg}" stroke="{border_color}" stroke-width="1.5"/>
  <rect x="8" y="8" width="484" height="284" rx="12" fill="{card_bg}" fill-opacity="{0.7 if is_dark else 0.9}"/>

  <!-- Header -->
  <g transform="translate(24, 20)">
    <!-- GFG Logo -->
    <g transform="translate(0, 2)">
      <rect width="28" height="28" rx="7" fill="{gfg_green}" fill-opacity="0.15"/>
      <path d="M 14,7 C 10.13,7 7,10.13 7,14 C 7,17.87 10.13,21 14,21 C 17.87,21 21,17.87 21,14 C 21,13.4 20.92,12.82 20.78,12.26 L 14,12.26 L 14,15.74 L 17.58,15.74 C 17.06,17.06 15.68,18 14,18 C 11.79,18 10,16.21 10,14 C 10,11.79 11.79,10 14,10 C 15.08,10 16.06,10.43 16.78,11.13 L 19.38,8.53 C 18,7.24 16.1,7 14,7 Z" fill="{gfg_green}"/>
    </g>
    <text x="36" y="16" class="font-sans t-title">GeeksforGeeks</text>
    <text x="36" y="29" class="font-mono t-sub">@{USERNAME}</text>

    <!-- Coding Score Badge -->
    <g transform="translate(340, 2)">
      <rect width="112" height="28" rx="8" fill="{gfg_green}" fill-opacity="0.15" stroke="{gfg_green}" stroke-width="1"/>
      <text x="56" y="18" text-anchor="middle" class="font-mono" font-size="11px" font-weight="700" fill="{gfg_green}">SCORE: {CODING_SCORE}</text>
    </g>
  </g>

  <!-- Divider -->
  <line x1="24" y1="62" x2="476" y2="62" stroke="{border_color}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Center Section: Ring & Breakdown -->
  <g transform="translate(24, 76)">
    <!-- Circular Progress Donut Chart -->
    <g transform="translate(68, 62)">
      <!-- Background track -->
      <circle cx="0" cy="0" r="{R}" fill="none" stroke="{pill_bg}" stroke-width="9"/>
      
      <!-- Colored Segments (rotate -90 so starts at top) -->
      <g transform="rotate(-90)">
        <!-- Hard -->
        <circle cx="0" cy="0" r="{R}" fill="none" stroke="{color_hard}" stroke-width="9"
          stroke-dasharray="{p_hard:.2f} {C:.2f}" stroke-dashoffset="-{off_hard:.2f}"/>
        <!-- Medium -->
        <circle cx="0" cy="0" r="{R}" fill="none" stroke="{color_medium}" stroke-width="9"
          stroke-dasharray="{p_medium:.2f} {C:.2f}" stroke-dashoffset="-{off_medium:.2f}"/>
        <!-- Easy -->
        <circle cx="0" cy="0" r="{R}" fill="none" stroke="{color_easy}" stroke-width="9"
          stroke-dasharray="{p_easy:.2f} {C:.2f}" stroke-dashoffset="-{off_easy:.2f}"/>
        <!-- Basic -->
        <circle cx="0" cy="0" r="{R}" fill="none" stroke="{color_basic}" stroke-width="9"
          stroke-dasharray="{p_basic:.2f} {C:.2f}" stroke-dashoffset="-{off_basic:.2f}"/>
      </g>

      <!-- Center Text -->
      <text x="0" y="4" text-anchor="middle" class="font-mono t-num-big">{TOTAL_SOLVED}</text>
      <text x="0" y="19" text-anchor="middle" class="font-sans t-lbl-sm">SOLVED</text>
    </g>

    <!-- Difficulty Breakdown List -->
    <g transform="translate(160, 10)">
      <!-- Basic Row -->
      <g transform="translate(0, 0)">
        <rect width="292" height="24" rx="6" fill="{pill_bg}"/>
        <circle cx="14" cy="12" r="4.5" fill="{color_basic}"/>
        <text x="26" y="16" class="font-sans t-diff-name" fill="{color_basic}">Basic</text>
        <text x="280" y="16" text-anchor="end" class="font-mono t-diff-val">{BASIC}</text>
      </g>

      <!-- Easy Row -->
      <g transform="translate(0, 29)">
        <rect width="292" height="24" rx="6" fill="{pill_bg}"/>
        <circle cx="14" cy="12" r="4.5" fill="{color_easy}"/>
        <text x="26" y="16" class="font-sans t-diff-name" fill="{color_easy}">Easy</text>
        <text x="280" y="16" text-anchor="end" class="font-mono t-diff-val">{EASY}</text>
      </g>

      <!-- Medium Row -->
      <g transform="translate(0, 58)">
        <rect width="292" height="24" rx="6" fill="{pill_bg}"/>
        <circle cx="14" cy="12" r="4.5" fill="{color_medium}"/>
        <text x="26" y="16" class="font-sans t-diff-name" fill="{color_medium}">Medium</text>
        <text x="280" y="16" text-anchor="end" class="font-mono t-diff-val">{MEDIUM}</text>
      </g>

      <!-- Hard Row -->
      <g transform="translate(0, 87)">
        <rect width="292" height="24" rx="6" fill="{pill_bg}"/>
        <circle cx="14" cy="12" r="4.5" fill="{color_hard}"/>
        <text x="26" y="16" class="font-sans t-diff-name" fill="{color_hard}">Hard</text>
        <text x="280" y="16" text-anchor="end" class="font-mono t-diff-val">{HARD}</text>
      </g>
    </g>
  </g>

  <!-- Divider -->
  <line x1="24" y1="214" x2="476" y2="214" stroke="{border_color}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Bottom Stats Metric Cards -->
  <g transform="translate(24, 226)">
    <!-- Metric 1: Coding Score -->
    <g transform="translate(0, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num" fill="{gfg_green}">{CODING_SCORE}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">CODING SCORE</text>
    </g>

    <!-- Metric 2: Total Solved -->
    <g transform="translate(116, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num">{TOTAL_SOLVED}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">PROBLEMS</text>
    </g>

    <!-- Metric 3: POTD Solved -->
    <g transform="translate(232, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num">{POTD}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">POTD SOLVED</text>
    </g>

    <!-- Metric 4: Streak -->
    <g transform="translate(348, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num" fill="#F59E0B">🔥 {STREAK} Day</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">STREAK</text>
    </g>
  </g>
</svg>
'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    dark_svg = build_gfg_card("dark")
    light_svg = build_gfg_card("light")

    with open("assets/gfg-card.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/gfg-card-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/gfg-card-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Generated assets/gfg-card.svg and assets/gfg-card-light.svg successfully!")

if __name__ == "__main__":
    main()
