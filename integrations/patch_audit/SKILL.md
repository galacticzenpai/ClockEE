---
name: patch-audit
description: AST-aware git commit diff inspector and pre-commit guard protecting core files (cbt_master_bank.js, database schemas) from accidental deletions or hallucinated imports.
---

# AST-Aware Git Commit Diff Inspector for Hallucinated Files

Reel: #32 (https://www.instagram.com/p/DfZyG8ZyJwv/)
Package: `integrations/patch_audit/`

## Capabilities
- Inspects git staged diffs before commit.
- Enforces protection rules:
  - Blocks deletion or mass truncation of core question banks (`cbt_master_bank.js`).
  - Detects unresolved merge conflicts or phantom syntax.
  - Sub-millisecond verification (<1ms).
