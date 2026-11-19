---
name: sloplint-ci
description: GitHub Actions Continuous Integration quality gate running Hallmark Anti-AI-Slop Linter on every push and pull request to guarantee 100/100 design certification.
---

# Automated GitHub Actions SlopLinter 100/100 Quality Gate

Reel: #31 (https://www.instagram.com/p/DfUe1XXx6Jw/)
Package: `integrations/sloplint_ci/`

## Capabilities
- Enforces automated design linter gate in GitHub Actions.
- Fails CI if score drops below 100.0 or any floor failure is detected.
- Generates JSON artifact reports on every build.
