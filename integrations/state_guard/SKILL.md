---
name: state-validator
description: Runtime client-side state mutation and corruption interceptor ensuring strict boundary checking on exam progress, active question index, and answer keys.
---

# Runtime Client-Side State Mutation & Corruption Interceptor

Reel: #28 (https://www.instagram.com/p/DfUPqjrt-H_/)
Package: `integrations/state_guard/`

## Capabilities
- Wraps exam state objects in ES6 Proxies with schema assertions.
- Rejects invalid mutations (e.g. negative question numbers, out-of-range option indices, NaN remaining seconds).
- Zero measurable latency (<1µs per mutation check).
