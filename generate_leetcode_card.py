#!/usr/bin/env python3
"""
Custom Premium LeetCode Stats Card Generator for Chandru M (@Chandrum06).
Fetches live stats from LeetCode GraphQL API with reliable fallback.
Matches the sleek dark/light aesthetic of the GitHub & GFG profile cards.
"""

import os
import math
import json
import urllib.request

USERNAME = "Chandrum06"

# Verified live stats
DEFAULT_STATS = {
    "total_solved": 263,
    "total_questions": 4033,
    "easy": 105,
    "easy_total": 961,
    "medium": 144,
    "medium_total": 2105,
    "hard": 14,
    "hard_total": 967,
    "ranking": 594489,
    "total_submissions": 794,
    "ac_submissions": 476,
    "acceptance_rate": 60.0,
    "badges_count": 3,
}

def fetch_live_leetcode_stats(username=USERNAME):
    """
    Fetches real-time stats from official LeetCode GraphQL API.
    """
    stats = dict(DEFAULT_STATS)
    query = """
    query getUserProfile($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
          totalSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        profile {
          ranking
          reputation
        }
        badges {
          displayName
        }
      }
    }
    """
    try:
        req = urllib.request.Request(
            "https://leetcode.com/graphql",
            data=json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode("utf-8"))
        
        # All questions available in LeetCode
        all_q = data.get("data", {}).get("allQuestionsCount", [])
        for q in all_q:
            diff = q.get("difficulty")
            cnt = q.get("count", 0)
            if diff == "All": stats["total_questions"] = cnt
            elif diff == "Easy": stats["easy_total"] = cnt
            elif diff == "Medium": stats["medium_total"] = cnt
            elif diff == "Hard": stats["hard_total"] = cnt

        matched = data.get("data", {}).get("matchedUser")
        if matched:
            # AC Submissions (Solved)
            ac_nums = matched.get("submitStats", {}).get("acSubmissionNum", [])
            for item in ac_nums:
                diff = item.get("difficulty")
                count = item.get("count", 0)
                if diff == "All": 
                    stats["total_solved"] = count
                    stats["ac_submissions"] = item.get("submissions", 476)
                elif diff == "Easy": stats["easy"] = count
                elif diff == "Medium": stats["medium"] = count
                elif diff == "Hard": stats["hard"] = count
            
            # Total Submissions (All attempts)
            tot_nums = matched.get("submitStats", {}).get("totalSubmissionNum", [])
            for item in tot_nums:
                if item.get("difficulty") == "All":
                    stats["total_submissions"] = item.get("submissions", 794)

            # Global Ranking
            rank = matched.get("profile", {}).get("ranking")
            if rank: stats["ranking"] = int(rank)

            # Badges
            badges = matched.get("badges", [])
            if badges: stats["badges_count"] = len(badges)

            # Accurate Acceptance Rate
            if stats["total_submissions"] > 0 and stats["ac_submissions"] > 0:
                stats["acceptance_rate"] = round((stats["ac_submissions"] / stats["total_submissions"]) * 100, 1)

            print(f"Fetched live LeetCode stats: {stats}")
            return stats
    except Exception as e:
        print(f"Warning: LeetCode GraphQL fetch fallback ({e})")

    return stats

def build_leetcode_card(theme="dark", stats=DEFAULT_STATS):
    is_dark = (theme == "dark")

    bg = "#040F1D" if is_dark else "#FFFFFF"
    card_bg = "#0B1E3B" if is_dark else "#F8FAFC"
    border_color = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(15, 23, 42, 0.12)"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#8BB9FE" if is_dark else "#475569"
    text_muted = "#5B7CA3" if is_dark else "#94A3B8"
    lc_amber = "#FFA116"
    lc_amber_glow = "#FBBF24"
    color_easy = "#00B8A3"
    color_medium = "#FFC01E"
    color_hard = "#FF375F"
    pill_bg = "#1E293B" if is_dark else "#EDF2F7"

    total_solved = stats["total_solved"]
    total_questions = stats["total_questions"]
    easy = stats["easy"]
    easy_total = stats["easy_total"]
    medium = stats["medium"]
    medium_total = stats["medium_total"]
    hard = stats["hard"]
    hard_total = stats["hard_total"]
    ranking = stats["ranking"]
    acceptance_rate = stats["acceptance_rate"]
    total_submissions = stats["total_submissions"]
    badges_count = stats.get("badges_count", 3)

    rank_str = f"#{ranking:,}" if ranking else "#594K"
    rank_short = f"#{ranking/1000:.1f}K" if ranking >= 1000 else f"#{ranking}"

    # SVG Ring Calculations (Radius = 46, Circumference = 289.02)
    R = 46
    C = 2 * math.pi * R
    
    p_easy = (easy / total_solved) * C if total_solved else 0
    p_medium = (medium / total_solved) * C if total_solved else 0
    p_hard = (hard / total_solved) * C if total_solved else 0

    off_hard = 0
    off_medium = p_hard
    off_easy = p_hard + p_medium

    # Progress bar widths (max width = 140px)
    w_easy_bar = max(4, int((easy / easy_total) * 140))
    w_med_bar = max(4, int((medium / medium_total) * 140))
    w_hard_bar = max(4, int((hard / hard_total) * 140))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="300" viewBox="0 0 500 300" role="img" aria-label="Chandru M - LeetCode Stats">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif; }}
      .font-mono {{ font-family: 'Segoe UI', Ubuntu, monospace; }}
      .t-title {{ font-size: 16px; font-weight: 700; fill: {text_primary}; letter-spacing: -0.2px; }}
      .t-sub {{ font-size: 11.5px; font-weight: 600; fill: #8BB9FE; }}
      .t-num-big {{ font-size: 26px; font-weight: 700; fill: {text_primary}; }}
      .t-lbl-sm {{ font-size: 10px; font-weight: 600; fill: #8BB9FE; letter-spacing: 0.5px; text-transform: uppercase; }}
      .t-diff-name {{ font-size: 12.5px; font-weight: 600; }}
      .t-diff-val {{ font-size: 12.5px; font-weight: 700; fill: {text_primary}; }}
      .t-diff-total {{ font-size: 11px; font-weight: 600; fill: #8BB9FE; }}
      .t-bottom-num {{ font-size: 18px; font-weight: 700; fill: {text_primary}; }}
      .t-bottom-lbl {{ font-size: 10px; font-weight: 600; fill: #8BB9FE; text-transform: uppercase; letter-spacing: 0.5px; }}
    </style>
    <linearGradient id="lcGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{lc_amber}"/>
      <stop offset="100%" stop-color="{lc_amber_glow}"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="500" height="300" rx="16" fill="{bg}" stroke="{border_color}" stroke-width="1.5"/>
  <rect x="8" y="8" width="484" height="284" rx="12" fill="{card_bg}" fill-opacity="{0.7 if is_dark else 0.9}"/>

  <!-- Header -->
  <g transform="translate(24, 20)">
    <!-- LeetCode Icon -->
    <g transform="translate(0, 2)">
      <rect width="28" height="28" rx="7" fill="{lc_amber}" fill-opacity="0.15"/>
      <path d="M 16.5,7.5 L 9.5,14.5 C 8.6,15.4 8.6,16.8 9.5,17.7 L 13.5,21.7 C 14.4,22.6 15.8,22.6 16.7,21.7 L 20.5,17.9 L 18.5,15.9 L 15.1,19.3 L 11.5,15.7 L 18.5,8.7 Z" fill="{lc_amber}"/>
      <path d="M 14,13.5 L 21.5,13.5 L 21.5,11 L 14,11 Z" fill="{lc_amber_glow}"/>
    </g>
    <text x="36" y="16" class="font-sans t-title">LeetCode</text>
    <text x="36" y="29" class="font-mono t-sub">@{USERNAME}</text>

    <!-- Global Rank Badge -->
    <g transform="translate(320, 2)">
      <rect width="132" height="28" rx="8" fill="{lc_amber}" fill-opacity="0.15" stroke="{lc_amber}" stroke-width="1"/>
      <text x="66" y="18" text-anchor="middle" class="font-mono" font-size="11px" font-weight="700" fill="{lc_amber}">RANK: {rank_str}</text>
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
      </g>

      <!-- Center Text -->
      <text x="0" y="4" text-anchor="middle" class="font-mono t-num-big">{total_solved}</text>
      <text x="0" y="19" text-anchor="middle" class="font-sans t-lbl-sm">SOLVED</text>
    </g>

    <!-- Difficulty Breakdown List with Progress Bars & Totals (e.g. 105/961) -->
    <g transform="translate(160, 15)">
      <!-- Easy Row -->
      <g transform="translate(0, 0)">
        <rect width="292" height="28" rx="7" fill="{pill_bg}"/>
        <circle cx="16" cy="14" r="5" fill="{color_easy}"/>
        <text x="28" y="18" class="font-sans t-diff-name" fill="{color_easy}">Easy</text>
        <!-- Mini Progress Bar -->
        <rect x="74" y="11" width="100" height="6" rx="3" fill="{card_bg}"/>
        <rect x="74" y="11" width="{int(w_easy_bar*100/140)}" height="6" rx="3" fill="{color_easy}"/>
        <text x="280" y="18" text-anchor="end" class="font-mono">
          <tspan class="t-diff-val">{easy}</tspan><tspan class="t-diff-total"> / {easy_total}</tspan>
        </text>
      </g>

      <!-- Medium Row -->
      <g transform="translate(0, 36)">
        <rect width="292" height="28" rx="7" fill="{pill_bg}"/>
        <circle cx="16" cy="14" r="5" fill="{color_medium}"/>
        <text x="28" y="18" class="font-sans t-diff-name" fill="{color_medium}">Med.</text>
        <!-- Mini Progress Bar -->
        <rect x="74" y="11" width="100" height="6" rx="3" fill="{card_bg}"/>
        <rect x="74" y="11" width="{int(w_med_bar*100/140)}" height="6" rx="3" fill="{color_medium}"/>
        <text x="280" y="18" text-anchor="end" class="font-mono">
          <tspan class="t-diff-val">{medium}</tspan><tspan class="t-diff-total"> / {medium_total}</tspan>
        </text>
      </g>

      <!-- Hard Row -->
      <g transform="translate(0, 72)">
        <rect width="292" height="28" rx="7" fill="{pill_bg}"/>
        <circle cx="16" cy="14" r="5" fill="{color_hard}"/>
        <text x="28" y="18" class="font-sans t-diff-name" fill="{color_hard}">Hard</text>
        <!-- Mini Progress Bar -->
        <rect x="74" y="11" width="100" height="6" rx="3" fill="{card_bg}"/>
        <rect x="74" y="11" width="{int(w_hard_bar*100/140)}" height="6" rx="3" fill="{color_hard}"/>
        <text x="280" y="18" text-anchor="end" class="font-mono">
          <tspan class="t-diff-val">{hard}</tspan><tspan class="t-diff-total"> / {hard_total}</tspan>
        </text>
      </g>
    </g>
  </g>

  <!-- Divider -->
  <line x1="24" y1="214" x2="476" y2="214" stroke="{border_color}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Bottom Stats Metric Cards -->
  <g transform="translate(24, 226)">
    <!-- Metric 1: Total Solved -->
    <g transform="translate(0, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num" fill="{lc_amber}">{total_solved}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">TOTAL SOLVED</text>
    </g>

    <!-- Metric 2: Global Rank -->
    <g transform="translate(116, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num">{rank_short}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">GLOBAL RANK</text>
    </g>

    <!-- Metric 3: Acceptance Rate -->
    <g transform="translate(232, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num" fill="{color_easy}">{acceptance_rate}%</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">ACCEPTANCE</text>
    </g>

    <!-- Metric 4: Badges -->
    <g transform="translate(348, 0)">
      <rect width="104" height="52" rx="8" fill="{pill_bg}"/>
      <text x="52" y="24" text-anchor="middle" class="font-mono t-bottom-num" fill="{lc_amber}">🏅 {badges_count}</text>
      <text x="52" y="41" text-anchor="middle" class="font-sans t-bottom-lbl">BADGES</text>
    </g>
  </g>
</svg>
'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    stats = fetch_live_leetcode_stats(USERNAME)
    dark_svg = build_leetcode_card("dark", stats)
    light_svg = build_leetcode_card("light", stats)

    with open("assets/leetcode-card.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/leetcode-card-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/leetcode-card-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Generated assets/leetcode-card.svg and assets/leetcode-card-light.svg successfully!")

if __name__ == "__main__":
    main()
