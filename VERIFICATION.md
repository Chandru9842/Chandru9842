# Verification Report

> This was the initial build-time verification. For the follow-up production
> audit (version pinning, workflow consolidation, quality score), see
> `HEALTH_REPORT.md`.

## Services checked and confirmed live (as of Jul 25, 2026)

| Service | Status | Notes |
|---|---|---|
| github-readme-stats.vercel.app | ✅ Active, maintained | Public instance can rate-limit under heavy global traffic (upstream project explicitly warns about this); self-hosting is available as a fallback but not required for normal use. |
| streak-stats.demolab.com | ✅ Active | This is the correct current host — the old `.herokuapp.com` URL was retired when Heroku ended its free tier; the README already used the right domain. |
| github-profile-trophy.vercel.app | ✅ Active, maintained | No change needed. |
| github-readme-activity-graph.vercel.app | ✅ Active, maintained | No change needed. |
| leetcard.jacoblin.cool | ✅ Active | Confirmed rendering for `Chandrum06`; includes contest rating via `ext=contest`. |
| gfgstatscard.vercel.app | ✅ Active | Confirmed working, renders username-based cards. Institute rank only appears if GfG itself exposes it on the public profile — this is upstream-dependent, not something the card controls. |
| komarev.com (profile views) | ✅ Active | No change needed. |
| shields.io (followers/stars/repos/badges) | ✅ Active | Added a dynamic "Public Repos" badge alongside existing Followers/Stars badges. |
| skillicons.dev | ✅ Active | No change needed. |
| capsule-render.vercel.app | ✅ Active | No change needed. |
| readme-typing-svg.demolab.com | ✅ Active | No change needed. |
| Platane/snk (contribution snake) | ✅ Active, widely used | Wired into `snake.yml`, publishing light + dark SVGs to the `output` branch, matching the `<picture>` tag already in the README. |
| gautamkrishnar/blog-post-workflow | ✅ Active, widely used | Added, but needs your RSS feed URL to activate (no feed was provided). |
| anmol098/waka-readme-stats | ✅ Active fork | The original `matchai/waka-readme-stats` project is archived; this actively maintained fork was substituted. Disabled by default until you connect WakaTime. |
| jamesgeorge007/github-activity-readme | ✅ Active, widely used | Added for the Recent Activity section. |
| LinkedIn public RSS/API | ❌ Discontinued | LinkedIn has not offered a public RSS feed or free API for personal article activity for several years. No reliable automated source exists — documented as a placeholder with a workaround instead of using a broken/fake widget. |

No deprecated or broken widgets were kept in the README.

## Automation features implemented

1. GitHub stats, streak, top-languages, trophies, activity graph — dark theme, purple accent (already live, unchanged design)
2. Contribution snake (light + dark) via scheduled Action → `output` branch
3. LeetCode stats card (auto-refreshing image, includes contest rating)
4. GeeksforGeeks stats card (auto-refreshing image)
5. Visitor counter (komarev, auto-incrementing)
6. Followers / Stars / Public Repos dynamic badges
7. Profile views dynamic badge
8. WakaTime section with markers, wired to a maintained Action (off by default, one flag to enable)
9. Recent GitHub activity section, refreshed every 6 hours
10. Blog posts section with markers, refreshed daily once a feed URL is added
11. YouTube and LinkedIn sections as clearly labeled placeholders with activation instructions (no channel/feed was supplied for either)
12. Daily developer quote, auto-refreshing image
13. "README last updated" timestamp, refreshed daily by a dedicated Action
14. Coding profile cards (LeetCode + GeeksforGeeks), clickable, responsive two-column layout — unchanged from original design

## What was intentionally *not* turned into a GitHub Action

Per the objective to avoid unnecessary complexity: stats/streak/trophy/activity-graph/quote/
LeetCode/GFG/followers/stars/repos/views badges are all **live image endpoints**, re-rendered
by their host every time the README is viewed. Wrapping these in a scheduled Action that
commits static copies into the README would add maintenance overhead and could make them
go *more* stale, not less — so they were left as-is, exactly as the original README already
had them.

## GitHub Sponsor badge

Not added. `Chandru9842` does not currently have GitHub Sponsors configured, and the
brief said to omit it in that case rather than show a broken/empty badge.

## Design/branding integrity check

- Colors (`#0D1117`, `#161B22`, `#8B5CF6`, `#A78BFA`, `#F8FAFC`, `#94A3B8`) — unchanged
- Section order, dividers, emoji headers, spacing — unchanged
- All existing sections, links, projects, and achievements — unchanged
- Markdown structure validated (balanced `<div>`/`<details>` tags, no broken image syntax)
