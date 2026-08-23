#!/usr/bin/env python3
"""
Ultra-Sleek Dynamic Developer Quote & Wisdom Matrix Generator for Chandru M (@Chandru9842).
- Automatically selects curated engineering and computer science quotes.
- Properly escapes all XML characters.
- Renders high-end glowing glassmorphism SVG quote cards with author badges and tags.
- Supports both dark and light modes.
"""

import os
import sys
import datetime
import xml.sax.saxutils as saxutils

OUTPUT_DARK = "assets/quote-card-dark.svg"
OUTPUT_LIGHT = "assets/quote-card-light.svg"
OUTPUT_MAIN = "assets/quote-card.svg"

def esc(text):
    return saxutils.escape(str(text))

CURATED_QUOTES = [
    {
        "quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
        "author": "Martin Fowler",
        "title": "Software Architecture & Refactoring Author",
        "tags": ["#Refactoring", "#CleanArchitecture", "#Maintainability"]
    },
    {
        "quote": "Talk is cheap. Show me the code.",
        "author": "Linus Torvalds",
        "title": "Creator of Linux & Git",
        "tags": ["#CleanCode", "#Execution", "#OpenSource"]
    },
    {
        "quote": "Simplicity is prerequisite for reliability.",
        "author": "Edsger W. Dijkstra",
        "title": "Turing Award Laureate & CS Pioneer",
        "tags": ["#Architecture", "#Reliability", "#DSA"]
    },
    {
        "quote": "The best way to predict the future is to invent it.",
        "author": "Alan Kay",
        "title": "Pioneer of OOP & Graphical UI",
        "tags": ["#Innovation", "#Systems", "#Vision"]
    },
    {
        "quote": "First, solve the problem. Then, write the code.",
        "author": "John Johnson",
        "title": "Software Engineering Philosopher",
        "tags": ["#ProblemSolving", "#Algorithms", "#Logic"]
    },
    {
        "quote": "Premature optimization is the root of all evil in software engineering.",
        "author": "Donald Knuth",
        "title": "Author of The Art of Computer Programming",
        "tags": ["#Optimization", "#Engineering", "#Algorithms"]
    },
    {
        "quote": "It is not enough for code to work. It must be clean, readable, and resilient to change.",
        "author": "Robert C. Martin",
        "title": "Author of Clean Code & SOLID Principles",
        "tags": ["#SOLID", "#Craftsmanship", "#CleanCode"]
    },
    {
        "quote": "Make it work, make it right, make it fast — in that exact order.",
        "author": "Kent Beck",
        "title": "Creator of Extreme Programming & TDD",
        "tags": ["#TDD", "#Agile", "#Performance"]
    }
]

def get_daily_quote():
    day_of_year = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    idx = day_of_year % len(CURATED_QUOTES)
    return CURATED_QUOTES[idx]

def build_quote_svg(quote_data, theme="dark"):
    is_dark = (theme == "dark")
    
    bg = "#0B1120" if is_dark else "#FFFFFF"
    card_bg = "#0F172A" if is_dark else "#F8FAFC"
    border = "rgba(56, 189, 248, 0.35)" if is_dark else "rgba(2, 132, 199, 0.25)"
    quote_text_color = "#F8FAFC" if is_dark else "#0F172A"
    author_color = "#38BDF8" if is_dark else "#0284C7"
    title_color = "#94A3B8" if is_dark else "#64748B"
    tag_bg = "#1E293B" if is_dark else "#E2E8F0"
    tag_text = "#E2E8F0" if is_dark else "#334155"
    accent_emerald = "#10B981" if is_dark else "#059669"
    quote_mark_color = "rgba(56, 189, 248, 0.12)" if is_dark else "rgba(2, 132, 199, 0.10)"

    quote_str = quote_data["quote"]
    author_str = quote_data["author"]
    title_str = quote_data["title"]
    tags = quote_data.get("tags", ["#Engineering", "#CleanCode"])

    # Wrap quote text cleanly
    words = quote_str.split()
    lines = []
    curr_line = []
    max_len = 56
    for w in words:
        if sum(len(x) + 1 for x in curr_line) + len(w) <= max_len:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
    if curr_line:
        lines.append(" ".join(curr_line))

    # Calculate y-positions for lines
    line_tspans = []
    start_y = 100 if len(lines) <= 2 else 92
    line_height = 28
    for i, l in enumerate(lines):
        line_tspans.append(f'<tspan x="42" y="{start_y + (i * line_height)}" xml:space="preserve">{esc(l)}</tspan>')

    # Build tag pills
    tag_pills = []
    tag_x = 42
    for t in tags:
        pill_w = len(t) * 7.5 + 16
        tag_pills.append(f"""
        <g transform="translate({tag_x}, 190)">
          <rect width="{pill_w:.1f}" height="24" rx="6" fill="{tag_bg}" stroke="{border}" stroke-width="0.8"/>
          <text x="{pill_w / 2:.1f}" y="16" class="font-mono" font-size="10.5px" font-weight="700" fill="{tag_text}" text-anchor="middle">{esc(t)}</text>
        </g>
        """)
        tag_x += pill_w + 10

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="790" height="236" viewBox="0 0 790 236" role="img" aria-label="Daily Developer Wisdom and Quote Card">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;700;800&amp;family=Plus+Jakarta+Sans:ital,wght@0,600;0,700;0,800;1,600;1,700&amp;display=swap');
      .font-sans {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
    <linearGradient id="quoteGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{card_bg}"/>
      <stop offset="100%" stop-color="{bg}"/>
    </linearGradient>
    <linearGradient id="glowLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#818CF8"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="790" height="236" rx="16" fill="url(#quoteGrad)" stroke="{border}" stroke-width="1.5"/>
  <rect x="0" y="0" width="790" height="3" fill="url(#glowLine)" rx="1.5"/>

  <!-- Giant Background Quote Glyph -->
  <text x="32" y="140" font-family="'Georgia', serif" font-size="160px" font-weight="900" fill="{quote_mark_color}">“</text>

  <!-- Header Telemetry -->
  <g transform="translate(32, 24)">
    <circle cx="8" cy="14" r="5" fill="{accent_emerald}">
      <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="22" y="19" class="font-sans" font-size="14.5px" font-weight="800" fill="{quote_text_color}">💬 DAILY DEVELOPER INSPIRATION</text>
    <text x="22" y="34" class="font-mono" font-size="10.5px" font-weight="600" fill="{title_color}">Engineering Philosophy // Wisdom Matrix</text>

    <!-- Daily Sync Badge -->
    <g transform="translate(615, 2)">
      <rect width="112" height="26" rx="7" fill="{accent_emerald}" fill-opacity="0.15" stroke="{accent_emerald}" stroke-width="1"/>
      <text x="56" y="17" class="font-mono" font-size="10px" font-weight="700" fill="{accent_emerald}" text-anchor="middle">DAILY SYNC</text>
    </g>
  </g>

  <!-- Quote Text -->
  <text class="font-sans" font-size="16.5px" font-style="italic" font-weight="700" fill="{quote_text_color}">
    {''.join(line_tspans)}
  </text>

  <!-- Author Info -->
  <g transform="translate(520, {start_y + (len(lines) * line_height) - 2})">
    <text x="238" y="0" class="font-sans" font-size="14px" font-weight="800" fill="{author_color}" text-anchor="end">— {esc(author_str)}</text>
    <text x="238" y="16" class="font-mono" font-size="10.5px" font-weight="600" fill="{title_color}" text-anchor="end">{esc(title_str)}</text>
  </g>

  <!-- Tag Pills -->
  {''.join(tag_pills)}

</svg>
'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    quote = get_daily_quote()

    dark_svg = build_quote_svg(quote, "dark")
    light_svg = build_quote_svg(quote, "light")

    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(OUTPUT_MAIN, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print(f"Generated ultra-sleek developer quote card ({quote['author']}) successfully!")

if __name__ == "__main__":
    main()
