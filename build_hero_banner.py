#!/usr/bin/env python3
"""
Pixel-Perfect Hero Banner & ASCII Art Generator for Chandru9842.
- Exact user-approved centered portrait sizing (54 cols x 34 rows, font-size 8.6px).
- Complete Developer Tools, AI Skills & Stack.
- Clean Education: B.E. CSE • SRM TRP Engineering College.
- Clickable links in SVG dock and README badges.
"""

import os
import io
import urllib.request
from PIL import Image, ImageEnhance, ImageOps

USERNAME = os.environ.get("GH_USERNAME", "Chandru9842")

def fetch_avatar_ascii(username=USERNAME, cols=54, rows=34):
    """
    Fetches avatar from GitHub and converts it to the exact
    user-approved centered ASCII portrait.
    """
    try:
        url = f"https://github.com/{username}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        img = Image.open(io.BytesIO(data)).convert("L")

        w, h = img.size
        # Precise crop to head and shoulders with balanced padding
        crop_box = (int(w * 0.08), int(h * 0.02), int(w * 0.92), int(h * 0.96))
        img_cropped = img.crop(crop_box)

        # High contrast and sharpness for defined facial lines
        img_cropped = ImageOps.autocontrast(img_cropped, cutoff=2)
        img_cropped = ImageEnhance.Contrast(img_cropped).enhance(1.65)
        img_cropped = ImageEnhance.Sharpness(img_cropped).enhance(2.2)

        # Resize to grid
        img_scaled = img_cropped.resize((cols, rows), Image.Resampling.LANCZOS)

        # Clean cyber ramp
        RAMP = "   ..::--==++**##%%@@@@"

        lines = []
        for y in range(rows):
            line = ""
            for x in range(cols):
                p = img_scaled.getpixel((x, y))
                idx = int(((255 - p) / 255.0) * (len(RAMP) - 1))
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

    raw_lines = fetch_avatar_ascii(USERNAME, cols=54, rows=34)

    # Format centered ASCII tspans with text-anchor="middle" at x="238"
    ascii_tspans = []
    y_start = 112
    line_h = 13.2
    for i, l in enumerate(raw_lines):
        l_esc = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y_pos = y_start + (i * line_h)
        ascii_tspans.append(f'<tspan x="238" y="{y_pos:.1f}" xml:space="preserve">{l_esc}</tspan>')

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

    <linearGradient id="laserSweep" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{laser_color}" stop-opacity="0"/>
      <stop offset="45%" stop-color="{laser_color}" stop-opacity="0.08"/>
      <stop offset="50%" stop-color="{laser_color}" stop-opacity="0.75"/>
      <stop offset="55%" stop-color="{laser_color}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{laser_color}" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="shimmerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="white" stop-opacity="0"/>
      <stop offset="50%" stop-color="white" stop-opacity="{0.12 if is_dark else 0.22}"/>
      <stop offset="100%" stop-color="white" stop-opacity="0"/>
    </linearGradient>

    <!-- Radial Background Lighting -->
    <radialGradient id="bgAmbient1" cx="20%" cy="15%" r="60%">
      <stop offset="0%" stop-color="{accent_1}" stop-opacity="{0.22 if is_dark else 0.12}"/>
      <stop offset="100%" stop-color="{bg_main}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="bgAmbient2" cx="80%" cy="85%" r="60%">
      <stop offset="0%" stop-color="{accent_2}" stop-opacity="{0.18 if is_dark else 0.10}"/>
      <stop offset="100%" stop-color="{bg_main}" stop-opacity="0"/>
    </radialGradient>

    <!-- Subtle Scanline Pattern -->
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.2" fill="{scan_color}" opacity="{0.04 if is_dark else 0.02}"/>
    </pattern>

    <!-- Reveal Mask for Left ASCII Portrait -->
    <mask id="asciiRevealMask">
      <rect x="18" y="55" width="440" height="0" fill="#FFFFFF">
        <animate attributeName="height" from="0" to="530" dur="2.0s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
      </rect>
    </mask>

    <!-- Sequential Clip Paths for Right Terminal Rows -->
    <clipPath id="cpHeader"><rect x="475" y="60" width="0" height="85"><animate attributeName="width" from="0" to="680" dur="0.5s" begin="0.4s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpPrompt"><rect x="475" y="145" width="0" height="42"><animate attributeName="width" from="0" to="680" dur="0.5s" begin="0.75s" fill="freeze"/></rect></clipPath>
    
    <clipPath id="cpRow1"><rect x="475" y="196" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.0s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpRow2"><rect x="475" y="218" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.15s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpRow3"><rect x="475" y="240" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.30s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpRow4"><rect x="475" y="262" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.45s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpRow5"><rect x="475" y="284" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.60s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpRow6"><rect x="475" y="306" width="0" height="22"><animate attributeName="width" from="0" to="680" dur="0.3s" begin="1.75s" fill="freeze"/></rect></clipPath>
    
    <clipPath id="cpSkills"><rect x="475" y="334" width="0" height="118"><animate attributeName="width" from="0" to="680" dur="0.5s" begin="1.95s" fill="freeze"/></rect></clipPath>
    <clipPath id="cpDock"><rect x="475" y="456" width="0" height="90"><animate attributeName="width" from="0" to="680" dur="0.5s" begin="2.25s" fill="freeze"/></rect></clipPath>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&amp;family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;display=swap');
      
      .font-mono {{ font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; }}
      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      
      .ascii-art {{ font-family: 'JetBrains Mono', 'Consolas', monospace; font-size: 8.6px; fill: url(#asciiGrad); letter-spacing: -0.15px; font-weight: 600; text-anchor: middle; }}
      .t-title {{ font-size: 26px; font-weight: 800; fill: url(#nameGrad); letter-spacing: -0.5px; }}
      .t-greeting {{ font-size: 13.5px; font-weight: 600; fill: {text_secondary}; letter-spacing: 0.3px; }}
      .t-prompt-usr {{ font-size: 12.5px; font-weight: 700; fill: {accent_2}; }}
      .t-prompt-cmd {{ font-size: 12.5px; font-weight: 600; fill: {text_primary}; }}
      .t-key {{ font-size: 11.5px; font-weight: 700; fill: {accent_2}; }}
      .t-val {{ font-size: 11.5px; font-weight: 500; fill: {text_primary}; }}
      .t-sep {{ font-size: 11.5px; fill: {text_muted}; opacity: 0.55; }}
      .t-dim {{ font-size: 10.5px; fill: {text_muted}; }}
      .pill-txt {{ font-size: 10.5px; font-weight: 600; fill: {pill_text}; }}
      .badge-lbl {{ font-size: 9.5px; font-weight: 700; fill: {accent_2}; letter-spacing: 1.3px; }}
      
      .social-link {{ cursor: pointer; text-decoration: none; }}
      .social-card {{ transition: transform 0.2s, stroke 0.2s; }}
      .social-card:hover {{ stroke: {accent_2}; }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="1180" height="610" rx="20" fill="{bg_main}"/>
  <rect width="1180" height="610" rx="20" fill="url(#bgAmbient1)"/>
  <rect width="1180" height="610" rx="20" fill="url(#bgAmbient2)"/>
  <rect width="1180" height="610" rx="20" fill="url(#scanlines)"/>

  <!-- Floating Ambient Particles -->
  <g opacity="{0.85 if is_dark else 0.4}">
    <circle cx="120" cy="110" r="1.8" fill="{accent_2}"><animate attributeName="opacity" values="0.2;1;0.2" dur="3.2s" repeatCount="indefinite"/></circle>
    <circle cx="280" cy="85" r="1.4" fill="{accent_1}"><animate attributeName="opacity" values="0.1;0.9;0.1" dur="4.1s" repeatCount="indefinite"/></circle>
    <circle cx="410" cy="140" r="1.6" fill="{accent_3}"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.8s" repeatCount="indefinite"/></circle>
    <circle cx="70" cy="450" r="1.5" fill="{accent_2}"><animate attributeName="opacity" values="0.2;0.8;0.2" dur="3.7s" repeatCount="indefinite"/></circle>
    <circle cx="390" cy="520" r="1.8" fill="{accent_1}"><animate attributeName="opacity" values="0.2;1;0.2" dur="4.5s" repeatCount="indefinite"/></circle>
    <circle cx="550" cy="100" r="1.4" fill="{accent_2}"><animate attributeName="opacity" values="0.1;0.85;0.1" dur="3.1s" repeatCount="indefinite"/></circle>
    <circle cx="820" cy="90" r="1.6" fill="{accent_3}"><animate attributeName="opacity" values="0.3;1;0.3" dur="3.9s" repeatCount="indefinite"/></circle>
    <circle cx="1110" cy="130" r="1.5" fill="{accent_2}"><animate attributeName="opacity" values="0.2;0.9;0.2" dur="2.9s" repeatCount="indefinite"/></circle>
    <circle cx="680" cy="540" r="1.7" fill="{accent_1}"><animate attributeName="opacity" values="0.2;1;0.2" dur="4.2s" repeatCount="indefinite"/></circle>
    <circle cx="1060" cy="510" r="1.6" fill="{accent_3}"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="3.5s" repeatCount="indefinite"/></circle>
  </g>

  <!-- Top macOS Glass Window Bar -->
  <g id="windowTitlebar">
    <rect x="14" y="12" width="1152" height="38" rx="12" fill="{titlebar_bg}" fill-opacity="{0.85 if is_dark else 0.92}" stroke="{panel_border}" stroke-width="1"/>
    <!-- Window Traffic Lights -->
    <circle cx="36" cy="31" r="5.5" fill="#EF4444"><animate attributeName="opacity" values="1;0.6;1" dur="4s" repeatCount="indefinite"/></circle>
    <circle cx="54" cy="31" r="5.5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.6;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
    <circle cx="72" cy="31" r="5.5" fill="#10B981"><animate attributeName="opacity" values="1;0.6;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
    
    <!-- Titlebar Header Text -->
    <text x="590" y="35.5" text-anchor="middle" class="font-mono t-dim" fill="{text_secondary}">chandru@production-node ~ % ./developer-profile.sh --status=ready</text>
    
    <!-- Status Beacon -->
    <g transform="translate(1040, 24)">
      <circle cx="8" cy="7" r="4" fill="{accent_3}">
        <animate attributeName="opacity" values="1;0.25;1" dur="1.2s" repeatCount="indefinite"/>
      </circle>
      <text x="18" y="11" class="font-mono badge-lbl" fill="{accent_3}">SYSTEM ONLINE</text>
    </g>
  </g>

  <!-- ==================== LEFT PANEL: CENTERED NATURAL BIOMETRIC ASCII PORTRAIT (~38%) ==================== -->
  <g id="leftSection" transform="translate(0, 0)">
    <!-- Floating ASCII Module -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3; 0 0" dur="6s" repeatCount="indefinite" easeMode="spline"/>
      
      <!-- Panel Border & Background -->
      <rect x="16" y="58" width="444" height="538" rx="16" fill="{panel_bg}" fill-opacity="{0.65 if is_dark else 0.75}" stroke="{panel_border}" stroke-width="1.2"/>
      <rect x="22" y="64" width="432" height="526" rx="12" fill="{panel_inner_bg}" fill-opacity="{0.45 if is_dark else 0.5}"/>

      <!-- HUD Top Bar -->
      <rect x="26" y="68" width="424" height="22" rx="6" fill="{titlebar_bg}" fill-opacity="0.6"/>
      <text x="36" y="83" class="font-mono badge-lbl">01 // FULL.BIOMETRIC.ASCII</text>
      <text x="438" y="83" text-anchor="end" class="font-mono t-dim">FPS: 60 • LIVE</text>

      <!-- Center-Aligned Face ASCII Render with Line-by-Line Reveal -->
      <g mask="url(#asciiRevealMask)">
        <text x="238" y="0" class="ascii-art">
{ascii_text_content}
        </text>
      </g>

      <!-- Animated Moving Laser Scanline Sweep -->
      <g mask="url(#asciiRevealMask)">
        <rect x="22" y="64" width="432" height="40" fill="url(#laserSweep)" style="mix-blend-mode: {'screen' if is_dark else 'multiply'}">
          <animateTransform attributeName="transform" type="translate" from="0 -40" to="0 530" dur="3.5s" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- HUD Tech Coordinate Overlay -->
      <rect x="26" y="560" width="424" height="24" rx="6" fill="{titlebar_bg}" fill-opacity="0.75"/>
      <text x="36" y="576" class="font-mono t-dim">LOC: 10.79°N, 78.70°E | ENCODE: UTF-8 | ID: CHANDRU9842</text>
      
      <!-- Corner Tech Reticle Accents -->
      <path d="M 28,74 L 28,68 L 34,68" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.8"/>
      <path d="M 442,74 L 442,68 L 436,68" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.8"/>
      <path d="M 28,582 L 28,588 L 34,588" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.8"/>
      <path d="M 442,582 L 442,588 L 436,588" stroke="{accent_2}" stroke-width="1.5" fill="none" opacity="0.8"/>
    </g>
  </g>

  <!-- ==================== RIGHT PANEL: TERMINAL & DEVELOPER ENVIRONMENT ==================== -->
  <g id="rightSection">
    <!-- Panel Container -->
    <rect x="470" y="58" width="696" height="538" rx="16" fill="{panel_bg}" fill-opacity="{0.65 if is_dark else 0.75}" stroke="{panel_border}" stroke-width="1.2"/>
    <rect x="476" y="64" width="684" height="526" rx="12" fill="{panel_inner_bg}" fill-opacity="{0.45 if is_dark else 0.5}"/>

    <!-- Terminal Sub Header Bar -->
    <rect x="480" y="68" width="676" height="22" rx="6" fill="{titlebar_bg}" fill-opacity="0.6"/>
    <text x="492" y="83" class="font-mono badge-lbl">02 // DEV.STATION.PROFILE</text>
    <text x="1144" y="83" text-anchor="end" class="font-mono t-dim">BRANCH: main [clean]</text>

    <!-- Block 1: Greeting & Name -->
    <g clip-path="url(#cpHeader)">
      <text x="492" y="106" class="font-mono t-greeting">Hi there 👋 Welcome to my workspace</text>
      <text x="492" y="134" class="font-sans t-title">I'm Chandru M</text>
    </g>

    <!-- Block 2: Terminal Interactive Prompt Box -->
    <g clip-path="url(#cpPrompt)">
      <rect x="490" y="146" width="656" height="32" rx="7" fill="{titlebar_bg}" fill-opacity="0.75" stroke="{panel_border}" stroke-width="1"/>
      <text x="504" y="167" class="font-mono">
        <tspan class="t-prompt-usr">chandru@cloud:~$ </tspan>
        <tspan class="t-prompt-cmd">Backend Engineer • Java / Spring Boot • Full Stack Systems</tspan>
      </text>
      <!-- Blinking Cursor -->
      <rect x="1000" y="155" width="7" height="14" fill="{accent_2}">
        <animate attributeName="opacity" values="1;0;1;0" dur="0.85s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- Divider 1 -->
    <line x1="490" y1="188" x2="1146" y2="188" stroke="{panel_border}" stroke-width="1" stroke-dasharray="4 4"/>

    <!-- Block 3: Sequential Spec Details (Clean non-overlapping rows, 22px step) -->
    <g clip-path="url(#cpRow1)">
      <text x="492" y="209" class="font-mono">
        <tspan class="t-key">📍 Location</tspan><tspan class="t-sep"> : .......... </tspan><tspan class="t-val">Tamil Nadu, India</tspan>
      </text>
    </g>

    <g clip-path="url(#cpRow2)">
      <text x="492" y="231" class="font-mono">
        <tspan class="t-key">🎓 Education</tspan><tspan class="t-sep"> : ......... </tspan><tspan class="t-val">B.E. CSE • SRM TRP Engineering College</tspan>
      </text>
    </g>

    <g clip-path="url(#cpRow3)">
      <text x="492" y="253" class="font-mono">
        <tspan class="t-key">⚡ Stack Pipeline</tspan><tspan class="t-sep"> : ..... </tspan><tspan class="t-val" font-weight="700" fill="{accent_3}">React → Node.js → Spring Boot → MySQL</tspan>
      </text>
    </g>

    <g clip-path="url(#cpRow4)">
      <text x="492" y="275" class="font-mono">
        <tspan class="t-key">🎯 Current Focus</tspan><tspan class="t-sep"> : ..... </tspan><tspan class="t-val">REST APIs • Microservices • Distributed Systems</tspan>
      </text>
    </g>

    <g clip-path="url(#cpRow5)">
      <text x="492" y="297" class="font-mono">
        <tspan class="t-key">🚀 Open For</tspan><tspan class="t-sep"> : .......... </tspan><tspan class="t-val">Software Engineering / Backend / Full-Stack Internships</tspan>
      </text>
    </g>

    <g clip-path="url(#cpRow6)">
      <text x="492" y="319" class="font-mono">
        <tspan class="t-key">📬 Contact Mail</tspan><tspan class="t-sep"> : ....... </tspan><tspan class="t-val">chandrumohan550@gmail.com</tspan>
      </text>
    </g>

    <!-- Divider 2 -->
    <line x1="490" y1="332" x2="1146" y2="332" stroke="{panel_border}" stroke-width="1" stroke-dasharray="4 4"/>

    <!-- ==================== SKILLS & COMPLETE TOOLCHAIN ==================== -->
    <g clip-path="url(#cpSkills)">
      <text x="492" y="349" class="font-mono badge-lbl">CORE TECHNOLOGIES, DEVELOPER TOOLS &amp; AI SKILLS</text>
      
      <!-- Row 1: Languages & Core Backend/Frontend Frameworks -->
      <g transform="translate(492, 358)">
        <g transform="translate(0, 0)"><rect width="66" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="33" y="16" text-anchor="middle" class="font-mono pill-txt">☕ Java</text></g>
        <g transform="translate(72, 0)"><rect width="104" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="52" y="16" text-anchor="middle" class="font-mono pill-txt">🍃 Spring Boot</text></g>
        <g transform="translate(182, 0)"><rect width="74" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="37" y="16" text-anchor="middle" class="font-mono pill-txt">⚛️ React</text></g>
        <g transform="translate(262, 0)"><rect width="84" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="42" y="16" text-anchor="middle" class="font-mono pill-txt">🟢 Node.js</text></g>
        <g transform="translate(352, 0)"><rect width="78" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="39" y="16" text-anchor="middle" class="font-mono pill-txt">🐬 MySQL</text></g>
        <g transform="translate(436, 0)"><rect width="80" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="40" y="16" text-anchor="middle" class="font-mono pill-txt">🐍 Python</text></g>
        <g transform="translate(522, 0)"><rect width="102" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="51" y="16" text-anchor="middle" class="font-mono pill-txt">⚡ JavaScript</text></g>
      </g>

      <!-- Row 2: DevOps, APIs & Architecture Tools -->
      <g transform="translate(492, 388)">
        <g transform="translate(0, 0)"><rect width="64" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="32" y="16" text-anchor="middle" class="font-mono pill-txt">🐙 Git</text></g>
        <g transform="translate(70, 0)"><rect width="82" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="41" y="16" text-anchor="middle" class="font-mono pill-txt">🐱 GitHub</text></g>
        <g transform="translate(158, 0)"><rect width="80" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="40" y="16" text-anchor="middle" class="font-mono pill-txt">🐳 Docker</text></g>
        <g transform="translate(244, 0)"><rect width="98" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="49" y="16" text-anchor="middle" class="font-mono pill-txt">🔌 REST APIs</text></g>
        <g transform="translate(348, 0)"><rect width="92" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="46" y="16" text-anchor="middle" class="font-mono pill-txt">🍃 MongoDB</text></g>
        <g transform="translate(446, 0)"><rect width="88" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="44" y="16" text-anchor="middle" class="font-mono pill-txt">☁️ AWS Cloud</text></g>
        <g transform="translate(540, 0)"><rect width="84" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="42" y="16" text-anchor="middle" class="font-mono pill-txt">🚀 Postman</text></g>
      </g>

      <!-- Row 3: Modern AI Toolchain, DSA & IDEs -->
      <g transform="translate(492, 418)">
        <g transform="translate(0, 0)"><rect width="138" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="69" y="16" text-anchor="middle" class="font-mono pill-txt">🤖 ChatGPT / OpenAI</text></g>
        <g transform="translate(144, 0)"><rect width="128" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="64" y="16" text-anchor="middle" class="font-mono pill-txt">✨ GitHub Copilot</text></g>
        <g transform="translate(278, 0)"><rect width="108" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="54" y="16" text-anchor="middle" class="font-mono pill-txt">⚡ Claude / Gemini</text></g>
        <g transform="translate(392, 0)"><rect width="86" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="43" y="16" text-anchor="middle" class="font-mono pill-txt">💻 VS Code</text></g>
        <g transform="translate(484, 0)"><rect width="140" height="24" rx="12" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/><text x="70" y="16" text-anchor="middle" class="font-mono pill-txt">🧠 DSA (250+ Solved)</text></g>
      </g>
    </g>

    <!-- ==================== BOTTOM SOCIAL & CONNECT DOCK (CLICKABLE LINKS) ==================== -->
    <g clip-path="url(#cpDock)">
      <rect x="490" y="460" width="656" height="58" rx="10" fill="{titlebar_bg}" fill-opacity="0.75" stroke="{panel_border}" stroke-width="1"/>
      
      <!-- Dock Item 1: GitHub (Clickable Link) -->
      <a xlink:href="https://github.com/Chandru9842" href="https://github.com/Chandru9842" target="_blank" class="social-link">
        <g transform="translate(502, 468)">
          <rect width="140" height="42" rx="7" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1" class="social-card"/>
          <text x="70" y="20" text-anchor="middle" class="font-mono badge-lbl">GITHUB ↗</text>
          <text x="70" y="34" text-anchor="middle" class="font-mono t-val">@Chandru9842</text>
        </g>
      </a>

      <!-- Dock Item 2: LinkedIn (Clickable Link) -->
      <a xlink:href="https://www.linkedin.com/in/chandru9842/" href="https://www.linkedin.com/in/chandru9842/" target="_blank" class="social-link">
        <g transform="translate(650, 468)">
          <rect width="150" height="42" rx="7" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1" class="social-card"/>
          <text x="75" y="20" text-anchor="middle" class="font-mono badge-lbl">LINKEDIN ↗</text>
          <text x="75" y="34" text-anchor="middle" class="font-mono t-val">in/chandru9842</text>
        </g>
      </a>

      <!-- Dock Item 3: LeetCode (Clickable Link) -->
      <a xlink:href="https://leetcode.com/u/Chandrum06/" href="https://leetcode.com/u/Chandrum06/" target="_blank" class="social-link">
        <g transform="translate(808, 468)">
          <rect width="150" height="42" rx="7" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1" class="social-card"/>
          <text x="75" y="20" text-anchor="middle" class="font-mono badge-lbl">LEETCODE ↗</text>
          <text x="75" y="34" text-anchor="middle" class="font-mono t-val">@Chandrum06</text>
        </g>
      </a>

      <!-- Dock Item 4: Email (Clickable Mailto Link) -->
      <a xlink:href="mailto:chandrumohan550@gmail.com" href="mailto:chandrumohan550@gmail.com" target="_blank" class="social-link">
        <g transform="translate(966, 468)">
          <rect width="168" height="42" rx="7" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1" class="social-card"/>
          <text x="84" y="20" text-anchor="middle" class="font-mono badge-lbl">EMAIL ✉</text>
          <text x="84" y="34" text-anchor="middle" class="font-mono t-val" font-size="11px">chandrumohan550</text>
        </g>
      </a>
    </g>

  </g>

  <!-- Global Glass Reflection Highlight Stripe -->
  <rect x="-300" y="0" width="200" height="610" fill="url(#shimmerGrad)" transform="skewX(-25)">
    <animateTransform attributeName="transform" type="translate" from="-400 0" to="1600 0" dur="6.5s" repeatCount="indefinite"/>
  </rect>

  <!-- Outer Shimmering Glowing Border -->
  <rect x="2" y="2" width="1176" height="606" rx="19" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.85">
    <animate attributeName="opacity" values="0.55;1;0.55" dur="3.5s" repeatCount="indefinite"/>
  </rect>
</svg>
'''
    return svg_content

def main():
    print(f"Generating pixel-perfect full face ASCII hero banner for {USERNAME}...")
    dark_svg = build_banner("dark")
    light_svg = build_banner("light")

    files_to_write = {
        "dark.svg": dark_svg,
        "light.svg": light_svg,
        "dark_mode.svg": dark_svg,
        "light_mode.svg": light_svg,
    }

    for fname, content in files_to_write.items():
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {fname} ({len(content)} bytes)")

if __name__ == "__main__":
    main()
