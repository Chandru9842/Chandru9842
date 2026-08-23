#!/usr/bin/env python3
"""
Dynamic Hero Banner & ASCII Art Generator for Chandru9842.
Fetches the user's latest GitHub profile photo and converts it
into a full, high-contrast, centered ASCII portrait inside a
premium animated SVG banner.
"""

import os
import io
import urllib.request
from PIL import Image, ImageEnhance, ImageOps

USERNAME = os.environ.get("GH_USERNAME", "Chandru9842")

def fetch_avatar_ascii(username=USERNAME, cols=62, rows=47):
    """
    Fetches the live avatar from GitHub and converts the full face
    into sharp, high-contrast ASCII art.
    """
    try:
        url = f"https://github.com/{username}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=10).read()
        img = Image.open(io.BytesIO(data)).convert("L")

        # Square center crop to keep full head & face proportion
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))

        # Enhance contrast and sharpness for defined facial lines
        img = ImageOps.autocontrast(img, cutoff=1.5)
        img = ImageEnhance.Contrast(img).enhance(1.45)
        img = ImageEnhance.Sharpness(img).enhance(1.5)

        # Scale to match character aspect ratio (height is ~1.8x width in mono fonts)
        img = img.resize((cols, rows), Image.Resampling.LANCZOS)

        # High-contrast cyber ASCII ramp
        RAMP = "  ..::--==++**##%%@@"

        lines = []
        for y in range(rows):
            line = ""
            for x in range(cols):
                pixel = img.getpixel((x, y))
                # Darker facial features -> denser characters
                idx = int(((255 - pixel) / 255.0) * (len(RAMP) - 1))
                line += RAMP[idx]
            lines.append(line)
        return lines
    except Exception as e:
        print(f"Warning: Could not fetch live avatar ({e}), using fallback art.")
        return ["  ...:::---===+++***###%%%@@@  " for _ in range(rows)]

def build_banner(theme_mode="dark"):
    is_dark = (theme_mode == "dark")
    
    # Visual Theme Palette
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
        pill_border = "rgba(56, 189, 248, 0.3)"
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
        pill_border = "rgba(2, 132, 199, 0.3)"
        pill_text = "#0F172A"
        titlebar_bg = "#F8FAFC"
        scan_color = "#06B6D4"
        laser_color = "#0284C7"
        ascii_color_1 = "#2563EB"
        ascii_color_2 = "#0284C7"
        ascii_color_3 = "#0D9488"

    raw_lines = fetch_avatar_ascii(USERNAME, cols=62, rows=47)

    # Format ASCII tspans with exact coordinate spacing
    ascii_tspans = []
    y_start = 104
    line_h = 9.8
    for i, l in enumerate(raw_lines):
        l_esc = l.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y_pos = y_start + (i * line_h)
        ascii_tspans.append(f'<tspan x="28" y="{y_pos:.1f}" xml:space="preserve">{l_esc}</tspan>')

    ascii_text_content = "\n".join(ascii_tspans)

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-label="Chandru M - Premium GitHub Developer Banner">
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
      <stop offset="50%" stop-color="white" stop-opacity="{0.12 if is_dark else 0.25}"/>
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

    <!-- Reveal Mask for ASCII Line-by-Line Unfold -->
    <mask id="asciiRevealMask">
      <rect x="20" y="55" width="440" height="0" fill="#FFFFFF">
        <animate attributeName="height" from="0" to="530" dur="2.2s" begin="0.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
      </rect>
    </mask>

    <!-- Terminal Sequential Reveal Clip Paths -->
    <clipPath id="cHeader"><rect x="475" y="65" width="0" height="60"><animate attributeName="width" from="0" to="680" dur="0.6s" begin="0.5s" fill="freeze"/></rect></clipPath>
    <clipPath id="cRole"><rect x="475" y="125" width="0" height="42"><animate attributeName="width" from="0" to="680" dur="0.6s" begin="0.9s" fill="freeze"/></rect></clipPath>
    <clipPath id="cSep1"><rect x="475" y="170" width="0" height="15"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="1.1s" fill="freeze"/></rect></clipPath>
    <clipPath id="cInfo1"><rect x="475" y="188" width="0" height="26"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="1.3s" fill="freeze"/></rect></clipPath>
    <clipPath id="cInfo2"><rect x="475" y="214" width="0" height="26"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="1.5s" fill="freeze"/></rect></clipPath>
    <clipPath id="cInfo3"><rect x="475" y="240" width="0" height="26"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="1.7s" fill="freeze"/></rect></clipPath>
    <clipPath id="cInfo4"><rect x="475" y="266" width="0" height="26"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="1.9s" fill="freeze"/></rect></clipPath>
    <clipPath id="cInfo5"><rect x="475" y="292" width="0" height="26"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="2.1s" fill="freeze"/></rect></clipPath>
    <clipPath id="cSep2"><rect x="475" y="322" width="0" height="15"><animate attributeName="width" from="0" to="680" dur="0.4s" begin="2.3s" fill="freeze"/></rect></clipPath>
    <clipPath id="cSkills"><rect x="475" y="340" width="0" height="120"><animate attributeName="width" from="0" to="680" dur="0.6s" begin="2.5s" fill="freeze"/></rect></clipPath>
    <clipPath id="cLinks"><rect x="475" y="470" width="0" height="110"><animate attributeName="width" from="0" to="680" dur="0.6s" begin="2.8s" fill="freeze"/></rect></clipPath>

    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&amp;family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;display=swap');
      
      .font-mono {{ font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; }}
      .font-sans {{ font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      
      .ascii-art {{ font-family: 'JetBrains Mono', 'Consolas', monospace; font-size: 6.9px; fill: url(#asciiGrad); letter-spacing: -0.15px; font-weight: 500; }}
      .t-title {{ font-size: 26px; font-weight: 800; fill: url(#nameGrad); letter-spacing: -0.5px; }}
      .t-greeting {{ font-size: 14px; font-weight: 600; fill: {text_secondary}; letter-spacing: 0.5px; }}
      .t-role {{ font-size: 15px; font-weight: 700; fill: {text_highlight}; }}
      .t-key {{ font-size: 12.5px; font-weight: 700; fill: {accent_2}; }}
      .t-val {{ font-size: 12.5px; font-weight: 500; fill: {text_primary}; }}
      .t-sep {{ font-size: 12px; fill: {text_muted}; opacity: 0.45; }}
      .t-dim {{ font-size: 11px; fill: {text_muted}; }}
      .pill-txt {{ font-size: 11.5px; font-weight: 600; fill: {pill_text}; }}
      .badge-lbl {{ font-size: 10px; font-weight: 700; fill: {accent_2}; letter-spacing: 1.5px; }}
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

  <!-- ==================== LEFT PANEL: FULL BIOMETRIC ASCII PORTRAIT (~38%) ==================== -->
  <g id="leftSection" transform="translate(0, 0)">
    <!-- Floating ASCII Module -->
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0; 0 -3.5; 0 0" dur="7s" repeatCount="indefinite" easeMode="spline"/>
      
      <!-- Panel Border & Background -->
      <rect x="16" y="58" width="444" height="538" rx="16" fill="{panel_bg}" fill-opacity="{0.65 if is_dark else 0.75}" stroke="{panel_border}" stroke-width="1.2"/>
      <rect x="22" y="64" width="432" height="526" rx="12" fill="{panel_inner_bg}" fill-opacity="{0.45 if is_dark else 0.5}"/>

      <!-- HUD Top Bar -->
      <rect x="26" y="68" width="424" height="22" rx="6" fill="{titlebar_bg}" fill-opacity="0.6"/>
      <text x="36" y="83" class="font-mono badge-lbl">01 // FULL.BIOMETRIC.ASCII</text>
      <text x="438" y="83" text-anchor="end" class="font-mono t-dim">FPS: 60 • LIVE</text>

      <!-- Full Face ASCII Render with Line-by-Line Reveal -->
      <g mask="url(#asciiRevealMask)">
        <text x="28" y="0" class="ascii-art">
{ascii_text_content}
        </text>
      </g>

      <!-- Animated Moving Laser Scanline Sweep -->
      <g mask="url(#asciiRevealMask)">
        <rect x="22" y="64" width="432" height="40" fill="url(#laserSweep)" style="mix-blend-mode: {'screen' if is_dark else 'multiply'}">
          <animateTransform attributeName="transform" type="translate" from="0 -40" to="0 530" dur="3.6s" repeatCount="indefinite"/>
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

    <!-- Content Row 1: Greeting & Name (Delayed Reveal) -->
    <g clip-path="url(#cHeader)">
      <text x="492" y="112" class="font-mono t-greeting">Hi there 👋 Welcome to my workspace</text>
      <text x="492" y="146" class="font-sans t-title">I'm Chandru M</text>
    </g>

    <!-- Content Row 2: Dynamic Cycling Typewriter Role (SMIL Multi-phrase Typewriter) -->
    <g clip-path="url(#cRole)">
      <rect x="492" y="156" width="652" height="30" rx="6" fill="{titlebar_bg}" fill-opacity="0.6" stroke="{panel_border}" stroke-width="1"/>
      <text x="504" y="176" class="font-mono t-role">
        <tspan fill="{accent_1}">❯ </tspan>
        <!-- Phase 1: Backend Engineer -->
        <tspan>
          <animate attributeName="display" values="inline;inline;none;none;none" keyTimes="0;0.24;0.25;0.99;1" dur="14s" repeatCount="indefinite"/>
          Backend Engineer (Java &amp; Spring Boot)
        </tspan>
        <!-- Phase 2: Full-Stack Systems Developer -->
        <tspan>
          <animate attributeName="display" values="none;none;inline;inline;none" keyTimes="0;0.25;0.26;0.49;1" dur="14s" repeatCount="indefinite"/>
          Full-Stack Systems Developer (React + Node)
        </tspan>
        <!-- Phase 3: Scalable Cloud & REST Architecture -->
        <tspan>
          <animate attributeName="display" values="none;none;inline;inline;none" keyTimes="0;0.50;0.51;0.74;1" dur="14s" repeatCount="indefinite"/>
          REST API Designer &amp; Database Architect
        </tspan>
        <!-- Phase 4: Distributed Systems & Microservices -->
        <tspan>
          <animate attributeName="display" values="none;none;inline;inline;inline" keyTimes="0;0.75;0.76;0.99;1" dur="14s" repeatCount="indefinite"/>
          Building Scalable, Production-Ready Systems
        </tspan>
      </text>
      <!-- Blinking Typewriter Cursor -->
      <rect x="880" y="164" width="8" height="14" fill="{accent_2}">
        <animate attributeName="opacity" values="1;0;1;0" dur="0.8s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- Divider Line 1 -->
    <g clip-path="url(#cSep1)">
      <text x="492" y="200" class="font-mono t-sep">────────────────────────────────────────────────────────────────────────</text>
    </g>

    <!-- Specifications / Sequential Details -->
    <g clip-path="url(#cInfo1)">
      <text x="492" y="218" class="font-mono">
        <tspan class="t-key">📍 Location</tspan><tspan class="t-sep"> : .......... </tspan><tspan class="t-val">Tamil Nadu, India</tspan>
      </text>
    </g>
    <g clip-path="url(#cInfo2)">
      <text x="492" y="242" class="font-mono">
        <tspan class="t-key">🎓 Education</tspan><tspan class="t-sep"> : ......... </tspan><tspan class="t-val">B.E. Computer Science • SRM TRP (Expected 2027)</tspan>
      </text>
    </g>
    <g clip-path="url(#cInfo3)">
      <text x="492" y="266" class="font-mono">
        <tspan class="t-key">⚡ Stack Pipeline</tspan><tspan class="t-sep"> : ..... </tspan><tspan class="t-val" font-weight="700" fill="{accent_3}">React → Spring Boot → MySQL</tspan>
      </text>
    </g>
    <g clip-path="url(#cInfo4)">
      <text x="492" y="290" class="font-mono">
        <tspan class="t-key">🎯 Current Focus</tspan><tspan class="t-sep"> : ..... </tspan><tspan class="t-val">REST APIs • Microservices • Distributed Systems</tspan>
      </text>
    </g>
    <g clip-path="url(#cInfo5)">
      <text x="492" y="314" class="font-mono">
        <tspan class="t-key">🚀 Open To</tspan><tspan class="t-sep"> : ........... </tspan><tspan class="t-val">Software Engineering / Backend / Full-Stack Internships</tspan>
      </text>
    </g>

    <!-- Divider Line 2 -->
    <g clip-path="url(#cSep2)">
      <text x="492" y="335" class="font-mono t-sep">────────────────────────────────────────────────────────────────────────</text>
    </g>

    <!-- ==================== SKILLS GLOWING PILLS ==================== -->
    <g clip-path="url(#cSkills)">
      <text x="492" y="355" class="font-mono badge-lbl">CORE TECHNOLOGIES &amp; TOOLCHAIN</text>
      
      <!-- Pills Row 1 -->
      <g transform="translate(492, 368)">
        <!-- Java -->
        <g transform="translate(0, 0)">
          <rect width="68" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="34" y="17.5" text-anchor="middle" class="font-mono pill-txt">☕ Java</text>
        </g>
        <!-- Spring Boot -->
        <g transform="translate(76, 0)">
          <rect width="112" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="56" y="17.5" text-anchor="middle" class="font-mono pill-txt">🍃 Spring Boot</text>
        </g>
        <!-- React -->
        <g transform="translate(196, 0)">
          <rect width="78" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="39" y="17.5" text-anchor="middle" class="font-mono pill-txt">⚛️ React</text>
        </g>
        <!-- Node.js -->
        <g transform="translate(282, 0)">
          <rect width="88" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="44" y="17.5" text-anchor="middle" class="font-mono pill-txt">🟢 Node.js</text>
        </g>
        <!-- MySQL -->
        <g transform="translate(378, 0)">
          <rect width="80" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="40" y="17.5" text-anchor="middle" class="font-mono pill-txt">🐬 MySQL</text>
        </g>
        <!-- Docker -->
        <g transform="translate(466, 0)">
          <rect width="84" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="42" y="17.5" text-anchor="middle" class="font-mono pill-txt">🐳 Docker</text>
        </g>
        <!-- Git -->
        <g transform="translate(558, 0)">
          <rect width="66" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="33" y="17.5" text-anchor="middle" class="font-mono pill-txt">🐙 Git</text>
        </g>
      </g>

      <!-- Pills Row 2 -->
      <g transform="translate(492, 402)">
        <!-- REST APIs -->
        <g transform="translate(0, 0)">
          <rect width="102" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="51" y="17.5" text-anchor="middle" class="font-mono pill-txt">🔌 REST APIs</text>
        </g>
        <!-- JavaScript -->
        <g transform="translate(110, 0)">
          <rect width="108" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="54" y="17.5" text-anchor="middle" class="font-mono pill-txt">⚡ JavaScript</text>
        </g>
        <!-- Python -->
        <g transform="translate(226, 0)">
          <rect width="86" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="43" y="17.5" text-anchor="middle" class="font-mono pill-txt">🐍 Python</text>
        </g>
        <!-- AWS Cloud -->
        <g transform="translate(320, 0)">
          <rect width="70" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="35" y="17.5" text-anchor="middle" class="font-mono pill-txt">☁️ AWS</text>
        </g>
        <!-- DSA / Problem Solving -->
        <g transform="translate(398, 0)">
          <rect width="142" height="26" rx="13" fill="{pill_bg}" stroke="{pill_border}" stroke-width="1"/>
          <text x="71" y="17.5" text-anchor="middle" class="font-mono pill-txt">🧠 DSA (250+ Solved)</text>
        </g>
      </g>
    </g>

    <!-- ==================== BOTTOM SOCIAL & CONNECT DOCK ==================== -->
    <g clip-path="url(#cLinks)">
      <rect x="492" y="445" width="652" height="74" rx="12" fill="{titlebar_bg}" fill-opacity="0.75" stroke="{panel_border}" stroke-width="1"/>
      
      <!-- Dock Item: GitHub -->
      <g transform="translate(506, 457)">
        <rect width="140" height="50" rx="8" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1"/>
        <text x="70" y="24" text-anchor="middle" class="font-mono badge-lbl">GITHUB</text>
        <text x="70" y="40" text-anchor="middle" class="font-mono t-val">@Chandru9842</text>
      </g>

      <!-- Dock Item: LinkedIn -->
      <g transform="translate(654, 457)">
        <rect width="150" height="50" rx="8" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1"/>
        <text x="75" y="24" text-anchor="middle" class="font-mono badge-lbl">LINKEDIN</text>
        <text x="75" y="40" text-anchor="middle" class="font-mono t-val">in/chandru9842</text>
      </g>

      <!-- Dock Item: LeetCode -->
      <g transform="translate(812, 457)">
        <rect width="150" height="50" rx="8" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1"/>
        <text x="75" y="24" text-anchor="middle" class="font-mono badge-lbl">LEETCODE</text>
        <text x="75" y="40" text-anchor="middle" class="font-mono t-val">@Chandrum06</text>
      </g>

      <!-- Dock Item: Email -->
      <g transform="translate(970, 457)">
        <rect width="162" height="50" rx="8" fill="{panel_inner_bg}" stroke="{panel_border}" stroke-width="1"/>
        <text x="81" y="24" text-anchor="middle" class="font-mono badge-lbl">EMAIL</text>
        <text x="81" y="40" text-anchor="middle" class="font-mono t-val" font-size="11.5px">chandrumohan550</text>
      </g>
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
    print(f"Generating full face ASCII hero banner for {USERNAME}...")
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
