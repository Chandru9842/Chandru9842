#!/usr/bin/env node
/**
 * Fetches the raw data needed for the GitHub Stats, Top Languages, and
 * Trophies cards in a single GraphQL request (one API round trip instead of
 * three), using the official GitHub GraphQL API — no third-party service.
 *
 * WHY THIS EXISTS: github-readme-stats.vercel.app and github-profile-trophy.
 * vercel.app are free, shared, community-hosted Vercel deployments. They
 * have a well-documented history of going down or rate-limiting under
 * global load, which is what broke the GitHub Stats / Top Languages /
 * Trophies cards in this README. Rather than swap in another third-party
 * mirror with the same failure mode, these three cards are now generated
 * from GitHub's own API and committed as static SVGs, exactly like the GFG
 * and LinkedIn cards already are.
 *
 * REQUIRES: a GH_TOKEN (or GITHUB_TOKEN) env var with at least `repo` +
 * `read:user` scope — the same secret already documented in SETUP.md for
 * the "recent activity" and WakaTime jobs. The default Actions GITHUB_TOKEN
 * cannot read a user's contributionsCollection, so a real PAT is required.
 */
const USERNAME = process.env.GITHUB_STATS_USERNAME || "Chandru9842";
const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;

const QUERY = `
  query ($login: String!) {
    user(login: $login) {
      login
      followers { totalCount }
      repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
        totalCount
        nodes {
          stargazerCount
          forkCount
          languages(first: 8, orderBy: { field: SIZE, direction: DESC }) {
            edges {
              size
              node { name color }
            }
          }
        }
      }
      contributionsCollection {
        totalCommitContributions
        totalIssueContributions
        totalPullRequestContributions
        totalPullRequestReviewContributions
        contributionCalendar { totalContributions }
      }
    }
  }
`;

async function fetchGitHubData(username = USERNAME) {
  if (!TOKEN) {
    throw new Error(
      "Missing GH_TOKEN/GITHUB_TOKEN env var. Set GH_TOKEN as a repo secret with repo + read:user scope."
    );
  }

  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      "Content-Type": "application/json",
      "User-Agent": `${username}-profile-card-generator`,
    },
    body: JSON.stringify({ query: QUERY, variables: { login: username } }),
  });

  if (!res.ok) {
    throw new Error(`GitHub GraphQL request failed: ${res.status} ${res.statusText}`);
  }

  const json = await res.json();
  if (json.errors) {
    throw new Error(`GitHub GraphQL errors: ${JSON.stringify(json.errors)}`);
  }

  return normalize(json.data.user);
}

function normalize(user) {
  const repos = user.repositories.nodes;

  const totalStars = repos.reduce((sum, r) => sum + r.stargazerCount, 0);
  const totalForks = repos.reduce((sum, r) => sum + r.forkCount, 0);

  const langTotals = new Map();
  for (const repo of repos) {
    for (const edge of repo.languages.edges) {
      const key = edge.node.name;
      const prev = langTotals.get(key) || { size: 0, color: edge.node.color };
      prev.size += edge.size;
      langTotals.set(key, prev);
    }
  }
  const totalLangSize = [...langTotals.values()].reduce((s, l) => s + l.size, 0) || 1;
  const topLanguages = [...langTotals.entries()]
    .map(([name, { size, color }]) => ({
      name,
      color: color || "#8B5CF6",
      percent: (size / totalLangSize) * 100,
    }))
    .sort((a, b) => b.percent - a.percent)
    .slice(0, 5);

  const cc = user.contributionsCollection;

  return {
    login: user.login,
    followers: user.followers.totalCount,
    publicRepos: user.repositories.totalCount,
    totalStars,
    totalForks,
    commitsPastYear: cc.totalCommitContributions,
    issuesPastYear: cc.totalIssueContributions,
    prsPastYear: cc.totalPullRequestContributions,
    reviewsPastYear: cc.totalPullRequestReviewContributions,
    contributionsPastYear: cc.contributionCalendar.totalContributions,
    topLanguages,
  };
}

module.exports = { fetchGitHubData, USERNAME };
