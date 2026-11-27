# Portfolio release checklist

1. Read [AGENTS.md](AGENTS.md) and use a focused branch.
2. Regenerate graphics with `node scripts/generate_assets.mjs`; verify with `--check`.
3. Open a pull request and review the public diff for sensitive content.
4. Require passing asset, Mermaid, secret-scan and planner jobs before merging. This is a working agreement, not a claim that branch protection is configured.
5. Inspect the visual review artifact, including mobile graphics. Confirm the actual GitHub rendering when possible.
6. Update [CHANGELOG.md](CHANGELOG.md), merge the verified revision, and check the main-branch workflow.
7. Record residual issues and unverified claims. Never deploy to the private environment from this repository.

## Manual controls

Repository administrators should configure required status checks and review branch protection separately. Logo attribution is not blanket trademark clearance. Review third-party artwork rights before adding new logos.
