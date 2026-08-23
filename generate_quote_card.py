#!/usr/bin/env python3
"""
Professional Developer Wisdom & Philosophy Card Generator for Chandru M (@Chandru9842).
- Designed in the exact typography, color palette, and layout of GitHub Developer Stats (Ocean Theme).
- Uses 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, Roboto, sans-serif.
- Rotates daily through curated computer science and software architecture quotes.
- 100% compliant XML with dark/light mode support.
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
        "title": "Author of Refactoring & Enterprise Application Architecture",
        "topic": "Clean Code & Architecture"
    },
    {
        "quote": "Talk is cheap. Show me the code.",
        "author": "Linus Torvalds",
        "title": "Creator of Linux Kernel & Git Version Control",
        "topic": "Engineering Execution"
    },
    {
        "quote": "Simplicity is prerequisite for reliability.",
        "author": "Edsger W. Dijkstra",
        "title": "Turing Award Laureate & Computer Science Pioneer",
        "topic": "System Reliability"
    },
    {
        "quote": "The best way to predict the future is to invent it.",
        "author": "Alan Kay",
        "title": "Pioneer of Object-Oriented Programming & GUI",
        "topic": "Innovation & Systems"
    },
    {
        "quote": "First, solve the problem. Then, write the code.",
        "author": "John Johnson",
        "title": "Software Engineering Philosopher",
        "topic": "Problem Solving & DSA"
    },
    {
        "quote": "Premature optimization is the root of all evil in software engineering.",
        "author": "Donald Knuth",
        "title": "Author of The Art of Computer Programming",
        "topic": "Algorithmic Efficiency"
    },
    {
        "quote": "It is not enough for code to work. It must be clean, readable, and resilient to change.",
        "author": "Robert C. Martin",
        "title": "Author of Clean Code & Design Principles",
        "topic": "Software Craftsmanship"
    },
    {
        "quote": "Make it work, make it right, make it fast — in that exact order.",
        "author": "Kent Beck",
        "title": "Creator of Extreme Programming & Test-Driven Development",
        "topic": "Architecture & Quality"
    }
]

def get_daily_quote():
    day_of_year = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    idx = day_of_year % len(CURATED_QUOTES)
    return CURATED_QUOTES[idx]

def build_quote_svg(quote_data, theme="dark"):
    is_dark = (theme == "dark")
    
    # Exact Ocean theme colors matching Pic 2 (ghstats.dev)
    bg = "#040F1D" if is_dark else "#FFFFFF"
    card_bg = "#0B1E3B" if is_dark else "#F8FAFC"
    border = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(15, 23, 42, 0.12)"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#8BB9FE" if is_dark else "#475569"
    text_muted = "#5B7CA3" if is_dark else "#94A3B8"
    accent_cyan = "#00E8FF" if is_dark else "#0284C7"
    accent_emerald = "#10B981" if is_dark else "#059669"
    badge_bg = "rgba(0, 232, 255, 0.1)" if is_dark else "rgba(2, 132, 199, 0.1)"

    quote_str = quote_data["quote"]
    author_str = quote_data["author"]
    title_str = quote_data["title"]
    topic_str = quote_data["topic"]

    # Wrap quote text cleanly
    words = quote_str.split()
    lines = []
    curr_line = []
    max_len = 62
    for w in words:
        if sum(len(x) + 1 for x in curr_line) + len(w) <= max_len:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
    if curr_line:
        lines.append(" ".join(curr_line))

    # Format tspans
    line_tspans = []
    start_y = 86 if len(lines) <= 2 else 80
    line_height = 24
    for i, l in enumerate(lines):
        line_tspans.append(f'<tspan x="36" y="{start_y + (i * line_height)}" xml:space="preserve">{esc(l)}</tspan>')

    author_y = start_y + (len(lines) * line_height) + 16

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="790" height="195" viewBox="0 0 790 195" role="img" aria-label="Daily Developer Wisdom">
  <defs>
    <style>
      .font-sans {{ font-family: 'Segoe UI', Ubuntu, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Roboto, sans-serif; }}
      .font-mono {{ font-family: 'Consolas', 'Courier New', 'Fira Code', 'JetBrains Mono', monospace; }}
    </style>
    <linearGradient id="quoteCardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{card_bg}"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="790" height="195" rx="12" fill="url(#quoteCardBg)" stroke="{border}" stroke-width="1.2"/>

  <!-- Header Section (Matching Pic 2 Header) -->
  <g transform="translate(32, 22)">
    <circle cx="6" cy="11" r="4.5" fill="{accent_cyan}"/>
    <text x="18" y="15" class="font-sans" font-size="15px" font-weight="700" fill="{accent_cyan}">Daily Developer Wisdom</text>
    <text x="195" y="15" class="font-mono" font-size="11.5px" font-weight="600" fill="{text_secondary}">// {esc(topic_str)}</text>

    <!-- Daily Sync Badge -->
    <g transform="translate(618, 0)">
      <rect width="104" height="24" rx="6" fill="{badge_bg}" stroke="{accent_cyan}" stroke-width="0.8"/>
      <text x="52" y="16" class="font-mono" font-size="10px" font-weight="700" fill="{accent_cyan}" text-anchor="middle">DAILY SYNC</text>
    </g>
  </g>

  <!-- Divider -->
  <line x1="32" y1="56" x2="758" y2="56" stroke="{border}" stroke-width="1"/>

  <!-- Quote Body -->
  <text class="font-sans" font-size="14.5px" font-weight="600" fill="{text_primary}">
    {''.join(line_tspans)}
  </text>

  <!-- Author Attribution -->
  <g transform="translate(36, {author_y})">
    <text x="0" y="0" class="font-sans" font-size="13px" font-weight="700" fill="{accent_cyan}">— {esc(author_str)}</text>
    <text x="12" y="16" class="font-sans" font-size="11.5px" font-weight="500" fill="{text_secondary}">{esc(title_str)}</text>
  </g>

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

    print(f"Generated professional developer wisdom card ({quote['author']}) successfully!")

if __name__ == "__main__":
    main()
