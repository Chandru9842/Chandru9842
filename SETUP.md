# Setup Instructions

This repo is your GitHub profile repo: **Chandru9842/Chandru9842**. Everything below assumes
the files are committed to the `main` branch of that repo.

## 1. Folder structure to commit

```
Chandru9842/
├── README.md
├── SETUP.md
├── VERIFICATION.md
├── HEALTH_REPORT.md
├── data/
│   ├── gfg-stats.json        # source of truth for the GFG card (hand-updated)
│   └── profile-info.json     # source of truth for the LinkedIn card
├── scripts/
│   ├── lib/
│   │   ├── theme.js               # shared colors/sizing + inline icon paths for all cards
│   │   └── fetch-github-data.js   # single GraphQL call feeding the 3 GitHub-data cards
│   ├── generate-gfg-card.js         # data/gfg-stats.json -> assets/gfg-card.svg
│   ├── generate-linkedin-card.js    # data/profile-info.json -> assets/linkedin-card.svg
│   ├── generate-github-stats-card.js  # GitHub API -> assets/github-stats-card.svg
│   ├── generate-top-langs-card.js     # GitHub API -> assets/top-langs-card.svg
│   └── generate-trophies-card.js      # GitHub API -> assets/trophies-card.svg
├── assets/
│   ├── gfg-card.svg              # generated — do not hand-edit
│   ├── linkedin-card.svg         # generated — do not hand-edit
│   ├── github-stats-card.svg     # generated — do not hand-edit
│   ├── top-langs-card.svg        # generated — do not hand-edit
│   └── trophies-card.svg         # generated — do not hand-edit
└── .github/
    └── workflows/
        ├── snake.yml           # contribution snake -> output branch
        ├── readme-sync.yml     # recent activity + blog posts + timestamp (chained, 1 concurrency group)
        ├── profile-cards.yml   # regenerates all 5 custom cards (GFG/LinkedIn from data/, GitHub Stats/Top Langs/Trophies from the GitHub API)
        └── wakatime.yml        # optional, disabled until secrets are added
```

> `recent-activity.yml`, `blog-posts.yml`, and `update-timestamp.yml` from the
> previous delivery have been merged into a single `readme-sync.yml` with three
> sequential jobs. This removes the risk of two workflows racing to `git push`
> to `main` at the same time (a real failure mode with 3 independent
> README-committing crons), and cuts the number of separate scheduled runs
> from 3 to 1.

## 0. Updating your GeeksforGeeks / LinkedIn card content

Both cards under **Professional Coding Profiles** are custom-generated SVGs,
not third-party scrapers — see `HEALTH_REPORT.md` §11 for why.

- **GFG numbers changed?** Edit `data/gfg-stats.json` (problems solved, coding
  score, institute rank, POTD solved), commit, and push. The `profile-cards.yml`
  workflow regenerates `assets/gfg-card.svg` automatically.
- **Headline/name changed?** Edit `data/profile-info.json` the same way to
  regenerate `assets/linkedin-card.svg`.
- **Test locally first** (optional): `node scripts/generate-gfg-card.js && node scripts/generate-linkedin-card.js`
  — both scripts have zero npm dependencies, just Node's built-in `fs`.

## 0.1 GitHub Stats / Top Languages / Milestones — now self-hosted

These three used to be `<img>` tags pointing at `github-readme-stats.vercel.app`
and `github-profile-trophy.vercel.app`. Both are free, shared, community-run
Vercel deployments, and both started rendering broken (a well-documented
failure mode for that whole category of service, not specific to this repo).
They're now generated straight from the official GitHub GraphQL API and
committed as static SVGs under `assets/`, refreshed daily by `profile-cards.yml`.

- **Requires the `GH_TOKEN` secret** (already documented in §3 below) with
  `repo` + `read:user` scope — the default Actions `GITHUB_TOKEN` can't read
  a user's `contributionsCollection`.
- **No token yet / API call fails?** Each script falls back to a same-size,
  same-theme "syncing" placeholder instead of leaving a broken image — see
  `scripts/lib/theme.js`'s `pendingCard()` helper. It self-heals the next
  time the workflow runs successfully.
- **Test locally** (needs `GH_TOKEN` in your shell env):
  `GH_TOKEN=ghp_xxx node scripts/generate-github-stats-card.js`

## 2. Repository settings (one-time)

1. **Settings → Actions → General → Workflow permissions** → select
   **"Read and write permissions"**. Several workflows commit back to the repo
   and will fail with a 403 otherwise.
2. **Settings → Actions → General** → confirm Actions are enabled for this repository.

## 3. Secrets to add (Settings → Secrets and variables → Actions → New repository secret)

| Secret name | Required by | How to get it |
|---|---|---|
| `GH_TOKEN` | `wakatime.yml`, the `recent-activity` job in `readme-sync.yml`, and the GitHub Stats/Top Languages/Milestones jobs in `profile-cards.yml` | Create a classic Personal Access Token at github.com/settings/tokens with `repo` + `user` scopes. The default `GITHUB_TOKEN` GitHub provides to Actions cannot read your cross-repo commit/PR/issue history or `contributionsCollection`, so these jobs need a real PAT. Without it, the three GitHub-data cards fall back to a "syncing" placeholder instead of a broken image. |
| `WAKATIME_API_KEY` | `wakatime.yml` | Sign up at wakatime.com → install the editor plugin → copy the key from wakatime.com/settings/api-key |

`snake.yml` and the `blog-posts` / `stamp-timestamp` jobs in `readme-sync.yml`
only need the built-in `GITHUB_TOKEN`, which Actions provides automatically —
no setup required beyond the "Read and write permissions" step above.

## 4. Turn on WakaTime (optional)

The WakaTime section is disabled by default (`if: false` guard in `wakatime.yml`)
because most people haven't installed the plugin yet. Once you have:

1. Added `WAKATIME_API_KEY` and `GH_TOKEN` as secrets (step 3)
2. Confirmed **Display coding activity publicly** is checked in your WakaTime privacy settings

remove the `if: false` line in `.github/workflows/wakatime.yml` and re-run the workflow
(Actions tab → Refresh WakaTime Stats → Run workflow).

## 5. Turn on the blog feed (optional)

Open `.github/workflows/readme-sync.yml`, find the `blog-posts` job, and replace
`REPLACE_WITH_YOUR_RSS_FEED_URL` with your feed (Hashnode, Dev.to, Medium, or Substack
all expose a public RSS/Atom URL). Multiple feeds can be comma-separated. Until this
is set, the README shows a placeholder.

## 6. YouTube (optional, not yet wired up)

No workflow is included for this by default since no channel was provided. To add it:
1. Get a YouTube Data API v3 key from Google Cloud Console.
2. Add `YOUTUBE_API_KEY` and `YOUTUBE_CHANNEL_ID` as repo secrets.
3. Add a job using an action such as `Varun0157/youtube-latest-video` (or write a small
   script step calling the YouTube Data API) that writes into a new
   `<!--START_SECTION:youtube--> ... <!--END_SECTION:youtube-->` block in the README.

## 7. LinkedIn articles

LinkedIn does not currently offer a public RSS or free API for a personal profile's
articles, so this can't be automated reliably. The README placeholder recommends
publishing on a platform with an open feed and cross-posting to LinkedIn instead.

## 8. Things that need **no** setup at all

These already auto-update on every page view, with no GitHub Action, secret, or token:

- Profile Views (komarev.com)
- Followers / Stars / Public Repos (shields.io dynamic badges + GitHub API)
- GitHub Stats, Streak Stats, Top Languages (github-readme-stats.vercel.app, streak-stats.demolab.com)
- GitHub Trophies (github-profile-trophy.vercel.app)
- Contribution Activity Graph (github-readme-activity-graph.vercel.app)
- LeetCode card (leetcard.jacoblin.cool)
- GeeksforGeeks card (gfgstatscard.vercel.app)
- Daily Developer Quote (quotes-github-readme.vercel.app)

These are all image URLs re-rendered live by their host on every request — committing
a GitHub Action to "refresh" them would be redundant and was intentionally left out.

## 9. GitHub Sponsor badge

Omitted — no GitHub Sponsors account is currently configured for `Chandru9842`. Add one
at github.com/sponsors and I can drop a badge in on request.
