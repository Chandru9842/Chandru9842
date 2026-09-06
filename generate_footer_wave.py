#!/usr/bin/env python3
"""
Generates modern, vibrant, theme-adaptive Footer Wave SVGs for Chandru M (@Chandru9842).
- Replaces broken/grey capsule-render.vercel.app with high-performance, self-hosted SVGs.
- Dark theme: Multi-layered Electric Cyan & Deep Ocean wave with luminous glow.
- Light theme: Vibrant Azure / Ocean Cyan wave that blends seamlessly with light GitHub UI.
"""

import os

OUTPUT_DARK = "assets/footer-wave-dark.svg"
OUTPUT_LIGHT = "assets/footer-wave-light.svg"
OUTPUT_MAIN = "assets/footer-wave.svg"

def build_footer_wave(theme="dark"):
    is_dark = (theme == "dark")

    if is_dark:
        # Dark Theme: Electric Cyan to Deep Navy glow
        grad1_start = "#00E8FF"
        grad1_mid = "#0284C7"
        grad1_end = "#00558A"
        grad1_op = "0.22"

        grad2_start = "#0284C7"
        grad2_mid = "#00E8FF"
        grad2_end = "#38BDF8"
        grad2_op = "0.45"

        grad3_start = "#040F1D"
        grad3_mid = "#0B2545"
        grad3_end = "#0077B6"
        crest_color = "#00E8FF"
        crest_op = "0.9"
    else:
        # Light Theme: Crisp Ocean Blue to Electric Cyan (vibrant & clean on white background)
        grad1_start = "#BAE6FD"
        grad1_mid = "#7DD3FC"
        grad1_end = "#38BDF8"
        grad1_op = "0.35"

        grad2_start = "#38BDF8"
        grad2_mid = "#00E8FF"
        grad2_end = "#0284C7"
        grad2_op = "0.55"

        grad3_start = "#0284C7"
        grad3_mid = "#00B4D8"
        grad3_end = "#00E8FF"
        crest_color = "#0284C7"
        crest_op = "0.8"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none" width="100%" height="110" role="img" aria-label="Profile Footer Wave Decorator">
  <defs>
    <linearGradient id="waveGrad1_{theme}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{grad1_start}" />
      <stop offset="50%" stop-color="{grad1_mid}" />
      <stop offset="100%" stop-color="{grad1_end}" />
    </linearGradient>

    <linearGradient id="waveGrad2_{theme}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{grad2_start}" />
      <stop offset="50%" stop-color="{grad2_mid}" />
      <stop offset="100%" stop-color="{grad2_end}" />
    </linearGradient>

    <linearGradient id="waveGrad3_{theme}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{grad3_start}" />
      <stop offset="50%" stop-color="{grad3_mid}" />
      <stop offset="100%" stop-color="{grad3_end}" />
    </linearGradient>
  </defs>

  <!-- Wave Layer 1 (Deepest Background Wave) -->
  <path d="M0,42 C180,85 360,15 540,52 C720,88 920,22 1080,58 C1140,70 1180,50 1200,46 L1200,120 L0,120 Z"
        fill="url(#waveGrad1_{theme})"
        opacity="{grad1_op}" />

  <!-- Wave Layer 2 (Middle Rhythm Wave) -->
  <path d="M0,58 C220,18 440,80 660,42 C880,5 1040,72 1200,56 L1200,120 L0,120 Z"
        fill="url(#waveGrad2_{theme})"
        opacity="{grad2_op}" />

  <!-- Wave Layer 3 (Foreground Wave) -->
  <path d="M0,74 C280,108 560,38 840,78 C980,96 1120,66 1200,68 L1200,120 L0,120 Z"
        fill="url(#waveGrad3_{theme})" />

  <!-- Wave Crest Line (Vibrant Top Stroke Highlight) -->
  <path d="M0,74 C280,108 560,38 840,78 C980,96 1120,66 1200,68"
        fill="none"
        stroke="{crest_color}"
        stroke-width="1.8"
        stroke-opacity="{crest_op}" />
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    dark_svg = build_footer_wave("dark")
    light_svg = build_footer_wave("light")

    with open(OUTPUT_DARK, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(OUTPUT_LIGHT, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(OUTPUT_MAIN, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print(f"Generated {OUTPUT_DARK}, {OUTPUT_LIGHT}, and {OUTPUT_MAIN} successfully!")

if __name__ == "__main__":
    main()
