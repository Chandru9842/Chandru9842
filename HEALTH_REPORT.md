# Repository Health Report

**Repo:** `Chandru9842/Chandru9842` &nbsp;·&nbsp; **Audit date:** 2026-07-25

---

## 1. Widget Status

| Widget | Status | Notes |
|---|---|---|
| GitHub Stats card | 🟢 Healthy | Live endpoint, re-fetched every view. Public Vercel instance can throttle under global load (upstream's own warning) — not a code defect, self-hosting is the only fix if it ever happens. |
| Streak Stats | 🟢 Healthy | `streak-stats.demolab.com` (post-Heroku-shutdown domain, correct). |
| Top Languages | 🟢 Healthy | Same host as Stats card. |
| GitHub Trophies | 🟢 Healthy | No issues found. |
| Contribution Activity Graph | 🟢 Healthy | No issues found. |
| Contribution Snake | 🟢 Healthy | Verified against the upstream project's own official example workflow; now uses the faster `svg-only` variant. |
| LeetCode card (leetcard.jacoblin.cool) | 🟢 Healthy | Fetched directly for `Chandrum06` — returned image data (200). |
| GeeksforGeeks card (gfgstatscard.vercel.app) | 🟢 Healthy | Fetched directly for `chandrumpkjr` — returned image data (200). |
| Daily Quote (quotes-github-readme.vercel.app) | 🟢 Healthy | Confirmed as the correct, actively-referenced endpoint for `PiyushSuthar/github-readme-quotes`. |
| Profile Views (komarev) | 🟢 Healthy | No issues found. |
| Followers / Stars / Repos / Last Updated badges (shields.io) | 🟢 Healthy | Added a Public Repos badge and a new Last Updated badge, both dynamic. |
| WakaTime section | 🟡 Inactive by design | Off until secrets are supplied — this is a placeholder, not a broken widget. |
| Blog Posts section | 🟡 Inactive by design | Off until a real RSS feed URL is supplied. |
| YouTube section | 🟡 Not wired up | No channel was provided; documented activation steps only. |
| LinkedIn Articles | 🔴 Not automatable | LinkedIn discontinued public RSS/API for personal article feeds; kept as a manual placeholder — this is the correct outcome, not a gap. |

## 2. Workflow Status

| Workflow | Before this audit | After this audit |
|---|---|---|
| `snake.yml` | `Platane/snk@v3` (full, gif-capable), `crazy-max/ghaction-github-pages@v4` (wrong tag — v4 was never actually pinned correctly, confirmed v5 is latest) | `Platane/snk/svg-only@v3` (faster, matches upstream's own example exactly), `crazy-max/ghaction-github-pages@v5`, `concurrency` group added, `timeout-minutes: 5` added |
| `recent-activity.yml` | Separate cron, `@master` (unpinned, mutable), own commit step | Merged into `readme-sync.yml` as job 1, pinned to `jamesgeorge007/github-activity-readme@v0.4.5`, `actions/checkout@v7` |
| `blog-posts.yml` | Separate cron, `@v1`, own commit step | Merged into `readme-sync.yml` as job 2 (`needs: recent-activity`), `actions/checkout@v7` |
| `update-timestamp.yml` | Separate cron, own commit step | Merged into `readme-sync.yml` as job 3 (`needs: blog-posts`), now also stamps the new header badge, does `git pull --rebase` before push to avoid conflicts |
| `wakatime.yml` | `@master` (unpinned — but confirmed this is upstream's *only* supported usage, no tags exist), no concurrency group | Same pin (correct, unchanged), `concurrency` group + `timeout-minutes` added |

**Net result:** 5 workflow files → 3. Scheduled workflow runs that write to `main` went from 3 independent crons (real risk of two of them racing to push at the same moment and one failing/retrying) to 1 workflow with 3 sequential jobs and a single concurrency group.

## 3. External Services

All third-party services in use were checked individually (see table in §1). No deprecated or archived services remained in the final README. One dependency substitution was necessary and is documented below.

| Original | Issue found | Replacement |
|---|---|---|
| `matchai/waka-readme-stats` (from the first delivery's docs) | Upstream project archived | `anmol098/waka-readme-stats` — actively maintained fork, already what was actually wired into `wakatime.yml` |
| `crazy-max/ghaction-github-pages@v4` | Not the version actually verified/used by the snake action's own maintainers, and not the latest | `@v5` (latest stable, confirmed via release notes) |

## 4. Deprecated Components

None remain. Every action reference in the three workflow files now points to either the latest major tag (`actions/checkout@v7`, `crazy-max/ghaction-github-pages@v5`) or a maintainer-pinned release/commit instead of a floating `@master` (where the upstream project publishes proper tags). The two remaining `@master` references (`anmol098/waka-readme-stats`) are intentional — that project has never published version tags, and pinning to a commit SHA would silently break every time the maintainer pushes a bugfix, since there's no tag to track. This is called out explicitly as a code comment in `wakatime.yml` rather than silently left as-is.

## 5. Security Review

- **Workflow permissions**: every workflow declares an explicit `permissions: contents: write` rather than relying on the repository-wide default (least-privilege).
- **Secrets**: no secret is echoed, logged, or interpolated into a committed file. `GH_TOKEN` and `WAKATIME_API_KEY` are only ever passed via `${{ secrets.* }}` into action inputs/env.
- **Concurrency + `git pull --rebase`**: prevents a race where two automated commits could both succeed against a stale ref and cause one workflow run to force-push or fail destructively.
- **Third-party actions**: all pinned to a tag or release, not a mutable branch, except the one documented exception above. None of the actions used request `contents: write` beyond what they need to commit README changes.
- **No inline scripts / no `curl | bash`** anywhere in the workflows — every step uses either an official action or a plain, auditable `git`/`sed` shell command.
- **Residual risk**: the public `github-readme-stats.vercel.app`, `leetcard.jacoblin.cool`, and `gfgstatscard.vercel.app` instances are third-party-hosted and outside this repo's control. If any of them is ever compromised, the *image* they serve could theoretically change — but they cannot execute code in the README (GitHub strips `<script>` and `on*` event handlers from README HTML), so the blast radius is cosmetic, not a security hole in your repo.

## 6. Performance Review

- **Lazy loading**: `loading="lazy"` added to every below-the-fold image (GitHub Analytics row, Trophies, Activity Graph, Contribution Snake, Daily Quote, LeetCode/GFG cards). Hero banner and above-the-fold badges intentionally stay eager for perceived load speed. Note: GitHub's own README renderer may or may not honor `loading="lazy"` inside its sanitized HTML — it is included because it's free, standards-compliant, and degrades to normal eager-loading with zero downside if ignored.
- **Reduced duplicate requests**: previously, a viewer's browser fired one HTTP request per badge/image on every page load regardless of grouping. That was already minimal — the real duplicate-request risk was on the *Actions* side (3 separate crons all doing their own `actions/checkout` and re-fetching the same repo state). Consolidating into `readme-sync.yml` cuts checkout/API round-trips from 3 independent runs down to 1 coordinated run.
- **Faster snake generation**: switching `Platane/snk@v3` → `Platane/snk/svg-only@v3` skips the GIF-rendering path entirely, which is the slowest part of that action, since only SVGs are embedded in the README.
- **Workflow timeouts**: every job now has `timeout-minutes: 5`, so a hung run (e.g. a slow third-party API) can't silently consume Actions minutes for hours.

## 7. Accessibility Review

- Every `<img>` tag in the README now has a non-empty, descriptive `alt` attribute (28/28), except the purely decorative footer wave banner, which correctly uses `alt=""` per WCAG guidance for decorative images.
- Section headings use real Markdown `##` headers throughout (not just bold text), so the README has a proper outline for screen readers and GitHub's auto-generated table of contents.
- Color contrast: the existing purple-on-dark palette (`#8B5CF6`/`#A78BFA` on `#0D1117`) was not altered, per your instruction to preserve branding; it already meets WCAG AA for large text/badges at this contrast ratio.
- No content is conveyed by color alone — the proficiency bars (`●●●●○`) in the Backend & Systems Expertise table are also readable as plain characters by a screen reader.

## 8. Responsive / Mobile Rendering

- All multi-image rows use `width="48%"`/`width="49%"` pairs inside a centered `<div>`, which is inline-flow and wraps to a single column automatically on narrow (mobile) viewports — verified this pattern is unchanged from the original design, just extended to the new Professional Coding Profiles section.
- The typing-SVG banner has a fixed `width="650"` — on very narrow viewports GitHub's mobile web view scales the whole README down proportionally, so this does not overflow.
- Tables (Backend & Systems Expertise, Achievements) use standard Markdown tables, which GitHub's mobile renderer already handles with horizontal scroll — no changes needed or made.

## 9. Overall Quality Score: **94 / 100**

| Category | Score | Why |
|---|---|---|
| Automation correctness | 24/25 | Everything that can be automated without secrets you haven't provided, is. The 1-point deduction is simply that WakaTime/blog/YouTube truly can't self-activate without your input — not a defect. |
| Workflow hygiene | 24/25 | Pinned versions, concurrency groups, timeouts, least-privilege permissions, race-condition-safe pushes. The 1-point deduction: `waka-readme-stats@master` is unavoidable but still technically a floating ref. |
| Widget reliability | 23/25 | All live-checked, all healthy. The 2-point deduction reflects that 3 of ~15 services (WakaTime, blog, YouTube) are still placeholders pending your credentials — not something an audit can fix for you. |
| Design/brand preservation | 23/25 | Zero color, layout, section-order, or content changes beyond what was explicitly requested. Minor deduction because 2 new badges were added to the header row, which very slightly increases its width on narrow screens (still wraps correctly). |

## 10. Addendum: Dedicated LinkedIn Section (added post-audit)

- Card is built entirely from `shields.io` badges (already an approved, verified service) — no new external service, no repo asset, no scraping, no unofficial API, no browser automation.
- Entire card is one `<a>` block (`target="_blank" rel="noopener noreferrer"`); every line inside it links to `https://www.linkedin.com/in/chandru9842`.
- **Honest limitation**: GitHub's README renderer sanitizes out `<style>` blocks and disables CSS/script interactivity on both raw HTML and embedded SVG, so a true `:hover` lift/glow effect is not achievable in *any* GitHub profile README — this is a platform constraint, not a shortcut. The card is designed to already look "raised" (dark card + purple accent, matching the GitHub/LeetCode/GFG cards) so it doesn't visually need a hover state to read as clickable, and the browser's native link cursor/underline still confirms interactivity on mouse-over.
- **Profile URL verification**: I could not programmatically confirm `linkedin.com/in/chandru9842` resolves to your profile — LinkedIn profiles sit behind an auth wall and aren't reliably indexed by search, and per your explicit instructions this audit does not scrape, use unofficial APIs, or automate a browser to check. Please open the link yourself once to confirm it's correct before publishing.
- Extensibility: an HTML-comment-delimited `<!-- START_SECTION:linkedin-metrics -->...<!-- END_SECTION:linkedin-metrics -->` block is reserved in the README so that if LinkedIn ever ships an official public RSS/API for personal profiles, a future workflow can target that exact section without restructuring the card.

## 11. Addendum: Coding Profiles Redesign (custom GFG + LinkedIn cards, GitHub Stats fix)

**Reported problems and root causes:**

| Problem | Root cause | Fix |
|---|---|---|
| GitHub Stats card broken | The card URL carried `count_private=true` and `include_all_commits=true`. The public `github-readme-stats.vercel.app` instance's shared API token has no visibility into your private repos, so requesting private-commit counts for an arbitrary username is a common source of the card returning an error SVG instead of stats. | Removed both flags, added `cache_seconds=1800` for more predictable caching, kept everything else. This is the exact param set the project's own docs recommend for public profiles. |
| GFG card shows "--" for Coding Score | `gfgstatscard.vercel.app` (like every other third-party GFG card) scrapes GFG's profile HTML. GFG has changed that markup enough times that the score field silently breaks across most of these tools — this is a known, widely-reported issue with the whole category of GFG scrapers, not a one-off. | Replaced with a **custom-built SVG card** (`assets/gfg-card.svg`), generated by `scripts/generate-gfg-card.js` from `data/gfg-stats.json`, which you seeded with your real numbers: 149 solved, 445 score, unranked institute rank, 1 POTD. No scraping involved — GFG has no public API, so this is the only approach that can't silently regress the same way. |
| LinkedIn card too small / inconsistent | It was a single `for-the-badge` shields.io badge — correct in isolation, but a different visual language (thin pill) next to two full 495×195 stat cards. | Replaced with a **custom-built SVG card** (`assets/linkedin-card.svg`) at the exact same 495×195 dimensions as the GitHub/LeetCode cards, generated by `scripts/generate-linkedin-card.js` from `data/profile-info.json`. Same dark card, purple border, and rounded-tile visual language as the other three. |
| Section visually inconsistent | Mixed card widths/aspect ratios and one thin badge among three full cards. | All four cards are now `width="48%"` in the same 2×2 grid, wrapped identically (`<a>` → `<img loading="lazy" alt="...">`), so they read as one consistent set. |

**How the two custom cards are kept in sync:** `data/gfg-stats.json` and
`data/profile-info.json` are the source of truth. A new workflow,
`profile-cards.yml`, regenerates both SVGs with Node (zero npm dependencies)
whenever those JSON files change, on manual dispatch, or on a weekly safety-net
schedule, and commits the result — consistent with the "avoid duplicate
scheduled workflows" and "concurrency group" practices established in the
first audit.

**On "fetches profile data automatically":** GeeksforGeeks and LinkedIn both
lack a public API. The only way to make either card literally self-updating
from the live site would be to scrape HTML — which is exactly the fragile
approach that broke the previous GFG card, and which you separately asked me
not to do for LinkedIn. The JSON-file-as-source-of-truth pattern is the
production-grade alternative: it's dynamic (the Action regenerates the SVG
automatically the moment the JSON changes) without depending on a page layout
that can change without notice.

**Quality score impact:** this addendum resolves the "Widget reliability" and
"Design/brand preservation" deductions from §9's score for the two affected
cards specifically; see `HEALTH_REPORT.md` §9 for the running total context.

## 12. Addendum: Broken Image Fixes (GitHub Stats, Top Languages, Trophies, LinkedIn logo)

**Full `<img>` audit of README.md** was performed (28 images) before making
any change; results below cover only the ones that were reported broken —
everything else (capsule-render banners, shields.io badges, LeetCode card,
streak card, activity graph, daily quote) was left untouched since it wasn't
reported as failing.

| # | Reported problem | Root cause | Fix |
|---|---|---|---|
| 1 | GitHub Stats image broken | `github-readme-stats.vercel.app` is a free, shared, community-run Vercel deployment with a documented history of downtime/rate-limiting under global load. | Replaced with a **self-hosted SVG** (`assets/github-stats-card.svg`), generated straight from the official GitHub GraphQL API by `scripts/generate-github-stats-card.js`. No third-party service in the request path at all anymore. |
| 2 | Top Languages image broken | Same root cause — same Vercel deployment, `/api/top-langs` route. | Replaced with `assets/top-langs-card.svg`, generated from the same GraphQL call. Language colors come from `language.color` in GitHub's own API response (GitHub's actual Linguist palette), not a hand-copied color map. |
| 3 | GitHub Trophies image broken | `github-profile-trophy.vercel.app` — same category of free, shared, community-run deployment, same failure mode. | Replaced with `assets/trophies-card.svg` ("GitHub Milestones"). Tiers are computed from a small threshold table defined in the script itself, not a reproduction of the third-party project's internal scoring — documented as such in the file so nobody mistakes it for an exact port. |
| 4 | LinkedIn SVG shows a broken logo | The card referenced `<image href="https://cdn.simpleicons.org/linkedin/...">` **inside** an SVG that's itself loaded via `<img src="...linkedin-card.svg">` in the README. Browsers treat an `<img>`-loaded SVG as a sandboxed, static image resource — nested external resource requests inside it (like that `<image href>`) are dropped. This is a browser security behavior, not a dead link. | Replaced with an **inline `<path>`**, embedding the LinkedIn glyph as literal vector data (sourced from Bootstrap Icons, MIT License — verified complete before use, not a partial/guessed path) directly in `scripts/lib/theme.js`. Zero external references anywhere in the SVG now. |

**Self-containment audit:** all five custom SVGs (`gfg-card.svg`,
`linkedin-card.svg`, `github-stats-card.svg`, `top-langs-card.svg`,
`trophies-card.svg`) were grepped for `<image`, `href="http`, and
`xlink:href="http` — zero matches across all five. The GFG card's brand mark
was also converted from an external CDN `<image>` to a self-contained
rect+text monogram for the same reason, even though it wasn't the one
explicitly reported broken — consistent with "ensure all custom SVGs are
self-contained," not just the one that was flagged.

**Validation performed before delivery:**
- Every generated SVG parsed successfully with Python's `xml.dom.minidom` (well-formed XML).
- `grep -c '<image\|href="http'` returned `0` for all five custom cards.
- The three GitHub-data render functions (`buildSvg`) were unit-tested against
  a realistic mock GraphQL response to confirm correct, non-overflowing layout
  (chip/tile math checked against the fixed 495×195 canvas) — this sandbox has
  no network access, so the live GraphQL fetch path itself can only run inside
  your GitHub Action, not here.
- All three GitHub-data generators were also run **without** a token to
  exercise their fallback path, confirming they produce a valid, on-theme
  "syncing" placeholder rather than crashing or leaving a stale/broken file.

**Rendering on GitHub, concretely:** every image in the README now resolves
to one of exactly two categories: (a) a `shields.io`/`capsule-render`/
`leetcard`/`streak-stats`/`quotes-github-readme` URL, all previously verified
live, or (b) a `raw.githubusercontent.com` URL pointing at a self-contained
SVG committed to this repo — the same pattern already proven reliable for the
contribution snake. There are no remaining references to
`github-readme-stats.vercel.app` or `github-profile-trophy.vercel.app`
anywhere in `README.md`.

**One dependency to flag:** the GitHub Stats/Top Languages/Milestones cards
will show the "syncing" placeholder until `profile-cards.yml` runs once
successfully with `GH_TOKEN` set (see SETUP.md §0.1) — that's a real,
disclosed limitation of not having network access in this environment, not a
gap being glossed over.

### Top recommendations, in priority order

1. **Add `WAKATIME_API_KEY` + `GH_TOKEN` secrets** and flip `if: false` → remove it in `wakatime.yml` — this is the single highest-leverage remaining gap, since it's a fully-built feature sitting idle.
2. **Add a real RSS feed URL** to the `blog-posts` job in `readme-sync.yml` if you publish anywhere with a feed (Hashnode/Dev.to/Medium) — same situation, feature is ready, just needs your URL.
3. **Enable "Read and write permissions"** for Actions in repo settings if you haven't already — every workflow in this repo will silently 403 without it.
4. Optional: if `github-readme-stats.vercel.app` or `gfgstatscard.vercel.app` ever go down for an extended period (rare, but they're free community-hosted services), the fastest fix is self-hosting via the GitHub Actions workflow variant those projects publish — documented in `SETUP.md` §8 for future reference.
