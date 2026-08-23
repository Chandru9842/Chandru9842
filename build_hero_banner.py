#!/usr/bin/env python3
"""
Pixel-Perfect Hero Banner & ASCII Art Generator for Chandru9842.
- Precise Passport-Proportion Centered ASCII Portrait calibrated to real avatar photograph.
- Complete Developer Tools, AI Skills & Stack.
- Clean Education: B.E. CSE • SRM TRP Engineering College.
- Clickable links in SVG dock and README badges.
"""

import os
import io
import urllib.request
import numpy as np
from PIL import Image, ImageFilter

USERNAME = os.environ.get("GH_USERNAME", "Chandru9842")

def fetch_avatar_ascii(username=USERNAME, cols=48, rows=34):
    """
    Fetches avatar from GitHub and converts it to an ultra-clean,
    centered passport portrait with natural human proportions.
    """
    try:
        url = f"https://github.com/{username}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        img = Image.open(io.BytesIO(data)).convert("RGB")

        # Resize with Lanczos
        img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
        arr = np.array(img_resized, dtype=np.float32)

        R = arr[:, :, 0]
        G = arr[:, :, 1]
        B = arr[:, :, 2]
        Lum = 0.299 * R + 0.587 * G + 0.114 * B

        img_gray = img_resized.convert("L")
        edges = np.array(img_gray.filter(ImageFilter.FIND_EDGES), dtype=np.float32)

        RAMP = " .:-=+*#%@"

        lines = []
        for y in range(rows):
            line = ""
            for x in range(cols):
                lum = Lum[y, x]
                r, g, b = R[y, x], G[y, x], B[y, x]
                edge = edges[y, x]
                
                # 1. Clear top lines
                if y < 2:
                    line += " "
                    continue
                    
                # 2. Clear outer left & right margins
                if y < 24 and (x < 6 or x > cols - 7):
                    line += " "
                    continue
                    
                # 3. Clean white background (high brightness & neutral white)
                if lum > 185 and abs(r - b) < 16 and edge < 22:
                    line += " "
                    continue
                if lum > 205:
                    line += " "
                    continue
                if (x < 3 or x > cols - 4) and lum > 175:
                    line += " "
                    continue

                # 4. Foreground: Darker = denser character + edge boost
                val = (255.0 - lum) / 255.0
                val = val + (edge / 255.0) * 0.25
                val = max(0.1, min(1.0, val))
                
                idx = int(val * (len(RAMP) - 1))
                line += RAMP[idx]
            lines.append(line)
        return lines
    except Exception as e:
        print(f"Warning: Avatar fetch fallback ({e})")
        return [" " * cols for _ in range(rows)]

def build_banner(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    
    if is_dark:
        bg_main = "#030712"
        panel_bg = "#0B1120"
        panel_inner_bg = "#0F172A"
        panel_border = "rgba(255, 255, 255, 0.08)"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        text_muted = "#64748B"
        text_highlight = "#38BDF8"
        accent_1 = "#7C3AED"  # Purple
        accent_2 = "#22D3EE"  # Cyan
        accent_3 = "#10B981"  # Emerald
        grad_stop_1 = "#22D3EE"
        grad_stop_2 = "#7C3AED"
        grad_stop_3 = "#10B981"
        pill_bg = "#1E293B"
        pill_border = "rgba(56, 189, 248, 0.28)"
        pill_text = "#E2E8F0"
        titlebar_bg = "#0B1120"
        scan_color = "#22D3EE"
        laser_color = "#38BDF8"
        ascii_color_1 = "#22D3EE"
        ascii_color_2 = "#818CF8"
        ascii_color_3 = "#C084FC"
    else:
        bg_main = "#FFFFFF"
        panel_bg = "#F8FAFC"
        panel_inner_bg = "#F1F5F9"
        panel_border = "rgba(15, 23, 42, 0.08)"
        text_primary = "#0F172A"
        text_secondary = "#334155"
        text_muted = "#64748B"
        text_highlight = "#0284C7"
        accent_1 = "#2563EB"  # Blue
        accent_2 = "#06B6D4"  # Cyan
        accent_3 = "#059669"  # Emerald
        grad_stop_1 = "#2563EB"
        grad_stop_2 = "#06B6D4"
        grad_stop_3 = "#059669"
        pill_bg = "#E2E8F0"
        pill_border = "rgba(2, 132, 199, 0.28)"
        pill_text = "#0F172A"
        titlebar_bg = "#F8FAFC"
        scan_color = "#06B6D4"
        laser_color = "#0284C7"
        ascii_color_1 = "#2563EB"
        ascii_color_2 = "#0284C7"
        ascii_color_3 = "#0D9488"

    raw_lines = fetch_avatar_ascii(USERNAME, cols=48, rows=34)

    # Format perfectly centered ASCII tspans with text-anchor="middle" at x="220" (exact center of 440px panel)
    ascii_tspans = []
    y_start = 76
    line_h = 11.2
    for i, l in enumerate(raw_lines):
        l_esc = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y_pos = y_start + (i * line_h)
        ascii_tspans.append(f'<tspan x="220" y="{y_pos:.1f}" xml:space="preserve">{l_esc}</tspan>')

    ascii_text_content = "\n".join(ascii_tspans)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-label="Chandru M - Premium GitHub Developer Banner">
  <defs>
    <!-- Dynamic Shifting Gradients -->
    <linearGradient id="heroGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{grad_stop_1}">
        <animate attributeName="stop-color" values="{grad_stop_1};{grad_stop_2};{grad_stop_3};{grad_stop_1}" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="{grad_stop_2}">
        <animate attributeName="stop-color" values="{grad_stop_2};{grad_stop_3};{grad_stop_1};{grad_stop_2}" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{grad_stop_3}">
        <animate attributeName="stop-color" values="{grad_stop_3};{grad_stop_1};{grad_stop_2};{grad_stop_3}" dur="10s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{ascii_color_1}">
        <animate attributeName="stop-color" values="{ascii_color_1};{ascii_color_2};{ascii_color_3};{ascii_color_1}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="{ascii_color_2}">
        <animate attributeName="stop-color" values="{ascii_color_2};{ascii_color_3};{ascii_color_1};{ascii_color_2}" dur="8s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{ascii_color_3}">
        <animate attributeName="stop-color" values="{ascii_color_3};{ascii_color_1};{ascii_color_2};{ascii_color_3}" dur="8s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>

    <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{grad_stop_1}"/>
      <stop offset="50%" stop-color="{grad_stop_2}"/>
      <stop offset="100%" stop-color="{grad_stop_3}"/>
    </linearGradient>

    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{accent_1}" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="{accent_2}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{accent_3}" stop-opacity="0.85"/>
    </linearGradient>

    <!-- Neon Glow Filter -->
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap');
      
      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; }}
      
      .cursor-blink {{
        animation: blink 1s step-end infinite;
      }}
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}

      .pulse-dot {{
        animation: pulseDot 2s ease-in-out infinite;
      }}
      @keyframes pulseDot {{
        0%, 100% {{ r: 3.5px; opacity: 1; }}
        50% {{ r: 5px; opacity: 0.6; }}
      }}

      .scanline {{
        animation: scanlineMove 6s linear infinite;
      }}
      @keyframes scanlineMove {{
        0% {{ transform: translateY(0px); opacity: 0.0; }}
        15% {{ opacity: 0.85; }}
        85% {{ opacity: 0.85; }}
        100% {{ transform: translateY(420px); opacity: 0.0; }}
      }}

      .badge-hover {{
        transition: transform 0.2s ease, opacity 0.2s ease;
        cursor: pointer;
      }}
      .badge-hover:hover {{
        transform: translateY(-2px);
        opacity: 0.95;
      }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="1180" height="610" rx="16" fill="{bg_main}"/>

  <!-- Outer Cyber Card -->
  <rect x="15" y="15" width="1150" height="580" rx="14" fill="{panel_bg}" stroke="url(#borderGrad)" stroke-width="1.8" filter="url(#softGlow)"/>

  <!-- macOS Style Window Titlebar -->
  <rect x="15" y="15" width="1150" height="38" rx="14" fill="{titlebar_bg}"/>
  <rect x="15" y="38" width="1150" height="15" fill="{titlebar_bg}"/>
  <line x1="15" y1="53" x2="1165" y2="53" stroke="{panel_border}" stroke-width="1"/>

  <!-- Window Controls -->
  <circle cx="38" cy="34" r="6" fill="#FF5F56"/>
  <circle cx="58" cy="34" r="6" fill="#FFBD2E"/>
  <circle cx="78" cy="34" r="6" fill="#27C93F"/>

  <!-- Titlebar Terminal Command -->
  <text x="590" y="38" text-anchor="middle" class="font-mono" font-size="11.5" font-weight="600" fill="{text_muted}">
    chandru@production-node ~ % ./developer-profile.sh --status=ready
  </text>

  <!-- Live Pulse Status Indicator -->
  <g transform="translate(1040, 26)">
    <circle cx="8" cy="8" r="3.5" fill="#10B981" class="pulse-dot"/>
    <text x="20" y="12" class="font-mono" font-size="10.5" font-weight="700" fill="#10B981" letter-spacing="0.5">SYSTEM ONLINE</text>
  </g>

  <!-- ======================================================== -->
  <!-- LEFT COLUMN: BIOMETRIC ASCII SCANNER                     -->
  <!-- ======================================================== -->
  <g transform="translate(35, 68)">
    <!-- Terminal Panel Frame -->
    <rect width="440" height="505" rx="10" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1.2"/>
    
    <!-- Top Bar -->
    <line x1="0" y1="32" x2="440" y2="32" stroke="{panel_border}" stroke-width="1"/>
    <text x="16" y="21" class="font-mono" font-size="10.5" font-weight="700" fill="{accent_2}" letter-spacing="0.8">01 // FULL.BIOMETRIC.ASCII</text>
    <text x="424" y="21" text-anchor="end" class="font-mono" font-size="9.5" font-weight="600" fill="{text_muted}">FPS: 60 • LIVE</text>

    <!-- Center HUD Corner Bracket Reticles -->
    <!-- Top-Left -->
    <path d="M 16 44 L 32 44 M 16 44 L 16 60" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.6"/>
    <!-- Top-Right -->
    <path d="M 424 44 L 408 44 M 424 44 L 424 60" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.6"/>
    <!-- Bottom-Left -->
    <path d="M 16 462 L 32 462 M 16 462 L 16 446" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.6"/>
    <!-- Bottom-Right -->
    <path d="M 424 462 L 408 462 M 424 462 L 424 446" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.6"/>

    <!-- Animated Cyber Scanline -->
    <g class="scanline">
      <line x1="16" y1="44" x2="424" y2="44" stroke="{laser_color}" stroke-width="1.8" filter="url(#neonGlow)"/>
      <rect x="16" y="20" width="408" height="24" fill="url(#heroGradient)" opacity="0.08"/>
    </g>

    <!-- Centered Clean Passport ASCII Portrait Output (48 cols x 34 rows, 8.8px font) -->
    <text class="font-mono" font-size="8.8px" font-weight="700" fill="url(#asciiGrad)" text-anchor="middle" letter-spacing="0.4px">
{ascii_text_content}
    </text>

    <!-- Bottom Telemetry HUD Info -->
    <line x1="0" y1="472" x2="440" y2="472" stroke="{panel_border}" stroke-width="1"/>
    <text x="16" y="491" class="font-mono" font-size="9" font-weight="600" fill="{text_muted}" letter-spacing="0.5">
      LOC: 10.79°N, 78.70°E | ENCODE: UTF-8 | ID: CHANDRU9842
    </text>
  </g>

  <!-- ======================================================== -->
  <!-- RIGHT COLUMN: DEVELOPER BIO & SYSTEM TELEMETRY           -->
  <!-- ======================================================== -->
  <g transform="translate(495, 68)">
    <!-- Main Right Container -->
    <rect width="650" height="505" rx="10" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1.2"/>
    
    <!-- Top Bar -->
    <line x1="0" y1="32" x2="650" y2="32" stroke="{panel_border}" stroke-width="1"/>
    <text x="18" y="21" class="font-mono" font-size="10.5" font-weight="700" fill="{accent_1}" letter-spacing="0.8">02 // DEV.STATION.PROFILE</text>
    <text x="632" y="21" text-anchor="end" class="font-mono" font-size="9.5" font-weight="600" fill="{text_muted}">BRANCH: main [clean]</text>

    <!-- Header Section -->
    <g transform="translate(20, 52)">
      <text x="0" y="0" class="font-sans" font-size="13" font-weight="600" fill="{text_secondary}">
        Hi there 👋 Welcome to my workspace
      </text>
      
      <!-- Primary Glowing Name -->
      <text x="0" y="28" class="font-sans" font-size="28" font-weight="800" fill="url(#nameGrad)" letter-spacing="-0.5px">
        I'm Chandru M
      </text>

      <!-- Terminal Command Shell Banner -->
      <g transform="translate(0, 42)">
        <rect width="610" height="34" rx="7" fill="{panel_bg}" stroke="{panel_border}" stroke-width="1"/>
        <text x="14" y="22" class="font-mono" font-size="11.5" font-weight="600" fill="{text_highlight}">
          chandru@cloud:~$ <tspan fill="{text_primary}">Backend Engineer • Java / Spring Boot • Full Stack Systems</tspan>
        </text>
      </g>
    </g>

    <!-- Telemetry Details Grid -->
    <g transform="translate(20, 150)">
      <line x1="0" y1="0" x2="610" y2="0" stroke="{panel_border}" stroke-width="1" stroke-dasharray="3 3"/>
      
      <!-- Row 1: Location -->
      <g transform="translate(0, 20)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">📍 Location</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-sans" font-size="11.5" font-weight="600" fill="{text_primary}">Tamil Nadu, India</text>
      </g>

      <!-- Row 2: Education -->
      <g transform="translate(0, 42)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">🎓 Education</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-sans" font-size="11.5" font-weight="600" fill="{text_primary}">B.E. CSE • SRM TRP Engineering College</text>
      </g>

      <!-- Row 3: Stack Pipeline -->
      <g transform="translate(0, 64)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">⚡ Stack Pipeline</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-sans" font-size="11.5" font-weight="600" fill="{text_primary}">React + Node.js ➔ Spring Boot + MySQL</text>
      </g>

      <!-- Row 4: Current Focus -->
      <g transform="translate(0, 86)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">🎯 Current Focus</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-sans" font-size="11.5" font-weight="600" fill="{text_primary}">REST APIs • Microservices • Distributed Systems</text>
      </g>

      <!-- Row 5: Open For -->
      <g transform="translate(0, 108)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">🚀 Open For</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-sans" font-size="11.5" font-weight="600" fill="{text_primary}">Software Engineering / Backend / Full-Stack Internships</text>
      </g>

      <!-- Row 6: Contact Mail -->
      <g transform="translate(0, 130)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="{accent_2}">📧 Contact Mail</text>
        <text x="125" y="0" class="font-mono" font-size="11" font-weight="600" fill="{text_muted}">: .........</text>
        <text x="160" y="0" class="font-mono" font-size="11" font-weight="700" fill="{text_highlight}">chandrumohan550@gmail.com</text>
      </g>

      <line x1="0" y1="146" x2="610" y2="146" stroke="{panel_border}" stroke-width="1" stroke-dasharray="3 3"/>
    </g>

    <!-- ======================================================== -->
    <!-- TECH STACK, TOOLS & AI SKILLS PILLS                      -->
    <!-- ======================================================== -->
    <g transform="translate(20, 316)">
      <text x="0" y="0" class="font-mono" font-size="9.5" font-weight="700" fill="{text_muted}" letter-spacing="0.8">
        CORE TECHNOLOGIES, DEVELOPER TOOLS &amp; AI SKILLS
      </text>

      <!-- Row 1: Core Technologies (Java, Spring Boot, React, Node.js, MySQL, Python, JavaScript) -->
      <g transform="translate(0, 12)">
        <!-- Java -->
        <g transform="translate(0, 0)">
          <rect width="64" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#EA2D2E"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Java</text>
        </g>

        <!-- Spring Boot -->
        <g transform="translate(70, 0)">
          <rect width="94" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#6DB33F"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Spring Boot</text>
        </g>

        <!-- React -->
        <g transform="translate(170, 0)">
          <rect width="70" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#61DAFB"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">React</text>
        </g>

        <!-- Node.js -->
        <g transform="translate(246, 0)">
          <rect width="76" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#5FA04E"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Node.js</text>
        </g>

        <!-- MySQL -->
        <g transform="translate(328, 0)">
          <rect width="68" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#4479A1"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">MySQL</text>
        </g>

        <!-- Python -->
        <g transform="translate(402, 0)">
          <rect width="72" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#3776AB"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Python</text>
        </g>

        <!-- JavaScript -->
        <g transform="translate(480, 0)">
          <rect width="90" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#F7DF1E"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">JavaScript</text>
        </g>
      </g>

      <!-- Row 2: Developer Tools (Git, GitHub, Docker, REST APIs, MongoDB, AWS Cloud, Postman) -->
      <g transform="translate(0, 40)">
        <!-- Git -->
        <g transform="translate(0, 0)">
          <rect width="52" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#F05032"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Git</text>
        </g>

        <!-- GitHub -->
        <g transform="translate(58, 0)">
          <rect width="70" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#A855F7"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">GitHub</text>
        </g>

        <!-- Docker -->
        <g transform="translate(134, 0)">
          <rect width="68" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#2496ED"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Docker</text>
        </g>

        <!-- REST APIs -->
        <g transform="translate(208, 0)">
          <rect width="82" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#009688"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">REST APIs</text>
        </g>

        <!-- MongoDB -->
        <g transform="translate(296, 0)">
          <rect width="76" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#47A248"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">MongoDB</text>
        </g>

        <!-- AWS Cloud -->
        <g transform="translate(378, 0)">
          <rect width="82" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#FF9900"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">AWS Cloud</text>
        </g>

        <!-- Postman -->
        <g transform="translate(466, 0)">
          <rect width="76" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#FF6C37"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Postman</text>
        </g>
      </g>

      <!-- Row 3: AI Skills & Problem Solving (ChatGPT/OpenAI, GitHub Copilot, Claude/Gemini, VS Code, DSA 250+ Solved) -->
      <g transform="translate(0, 68)">
        <!-- ChatGPT / OpenAI -->
        <g transform="translate(0, 0)">
          <rect width="124" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#10A37F"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">ChatGPT / OpenAI</text>
        </g>

        <!-- GitHub Copilot -->
        <g transform="translate(130, 0)">
          <rect width="112" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#8B5CF6"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">GitHub Copilot</text>
        </g>

        <!-- Claude / Gemini -->
        <g transform="translate(248, 0)">
          <rect width="114" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#D97706"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">Claude / Gemini</text>
        </g>

        <!-- VS Code -->
        <g transform="translate(368, 0)">
          <rect width="74" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#007ACC"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">VS Code</text>
        </g>

        <!-- DSA 250+ Solved -->
        <g transform="translate(448, 0)">
          <rect width="128" height="22" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <circle cx="11" cy="11" r="3" fill="#F59E0B"/>
          <text x="21" y="15" class="font-mono" font-size="9.5" font-weight="700" fill="{pill_text}">DSA (250+ Solved)</text>
        </g>
      </g>
    </g>

    <!-- Bottom Quick Launch Dock -->
    <g transform="translate(20, 436)">
      <line x1="0" y1="0" x2="610" y2="0" stroke="{panel_border}" stroke-width="1"/>
      
      <!-- GitHub Link -->
      <a href="https://github.com/Chandru9842" target="_blank" class="badge-hover">
        <g transform="translate(10, 12)">
          <rect width="130" height="28" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="65" y="18" text-anchor="middle" class="font-mono" font-size="9.5" font-weight="700" fill="{text_primary}">GITHUB ↗<tspan fill="{accent_2}"> @Chandru9842</tspan></text>
        </g>
      </a>

      <!-- LinkedIn Link -->
      <a href="https://www.linkedin.com/in/chandru9842/" target="_blank" class="badge-hover">
        <g transform="translate(155, 12)">
          <rect width="140" height="28" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="70" y="18" text-anchor="middle" class="font-mono" font-size="9.5" font-weight="700" fill="{text_primary}">LINKEDIN ↗<tspan fill="{accent_2}"> in/chandru9842</tspan></text>
        </g>
      </a>

      <!-- LeetCode Link -->
      <a href="https://leetcode.com/u/Chandrum06/" target="_blank" class="badge-hover">
        <g transform="translate(310, 12)">
          <rect width="135" height="28" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="67" y="18" text-anchor="middle" class="font-mono" font-size="9.5" font-weight="700" fill="{text_primary}">LEETCODE ↗<tspan fill="{accent_2}"> @Chandrum06</tspan></text>
        </g>
      </a>

      <!-- Email Link -->
      <a href="mailto:chandrumohan550@gmail.com" class="badge-hover">
        <g transform="translate(460, 12)">
          <rect width="140" height="28" rx="6" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="70" y="18" text-anchor="middle" class="font-mono" font-size="9.5" font-weight="700" fill="{text_primary}">EMAIL ✉<tspan fill="{accent_2}"> chandrumohan550</tspan></text>
        </g>
      </a>
    </g>
  </g>
</svg>
'''
    return svg_content

def main():
    print("Building Ultra-Clean Centered Passport Hero Banner SVGs...")
    dark_banner = build_banner("dark")
    light_banner = build_banner("light")

    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_banner)
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_banner)
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(dark_banner)
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(light_banner)

    print("Successfully built dark.svg, light.svg, dark_mode.svg, light_mode.svg!")

if __name__ == "__main__":
    main()
