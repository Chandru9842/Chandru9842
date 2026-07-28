// Shared design tokens for all custom-generated profile cards.
// Keeping this in one place means the GFG card, the LinkedIn card, the
// GitHub Stats/Top-Languages/Trophies cards, and any future card all stay
// pixel-consistent with each other and with the rest of the README.
module.exports = {
  width: 495,
  height: 220,
  radius: 14,
  bg: "#0D1117",
  bgAlt: "#161B22",
  border: "#8B5CF6",
  accent: "#8B5CF6",
  accentSoft: "#A78BFA",
  text: "#F8FAFC",
  textMuted: "#94A3B8",
  font: "'Segoe UI', Ubuntu, Sans-Serif",

  // Inline vector icon paths, embedded directly so cards never depend on an
  // external image/font request. No SVG loaded via <img> (which is how every
  // card in this README is embedded) can reliably fetch an external
  // <image href="..."> — browsers treat an <img>-loaded SVG as a static,
  // sandboxed image resource and drop nested external fetches, which is
  // exactly why the previous cdn.simpleicons.org-based logos rendered
  // broken. Everything below is self-contained vector path data instead.
  icons: {
    // LinkedIn "in" glyph, verbatim from Bootstrap Icons (MIT License),
    // https://icons.getbootstrap.com/icons/linkedin/ — viewBox 0 0 16 16.
    linkedin: {
      viewBox: "0 0 16 16",
      path: "M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z",
    },
  },

  /**
   * Renders a same-size, same-theme "pending sync" card. Used as a graceful
   * fallback by the GitHub Stats / Top Languages / Trophies generators when
   * GH_TOKEN isn't available (e.g. running locally without the secret) or
   * the GitHub API call fails, so the README always shows a self-contained,
   * on-brand SVG — never a broken image reference — until the next
   * successful Action run overwrites it with real data.
   */
  pendingCard(title, reason) {
    const w = this.width, h = this.height;
    const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(title)}: data sync pending">
  <title>${esc(title)} — sync pending</title>
  <rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="${this.radius}" fill="${this.bg}" stroke="${this.border}" stroke-width="1.4" stroke-dasharray="6 5"/>
  <text x="${w / 2}" y="${h / 2 - 8}" font-family="${this.font}" font-size="16" font-weight="700" fill="${this.accentSoft}" text-anchor="middle">${esc(title)}</text>
  <text x="${w / 2}" y="${h / 2 + 16}" font-family="${this.font}" font-size="12" fill="${this.textMuted}" text-anchor="middle">Syncing on next Action run &#8226; ${esc(reason)}</text>
</svg>
`;
  },
};
