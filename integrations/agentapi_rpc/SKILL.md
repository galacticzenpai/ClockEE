---
name: agentapi-rpc
description: Sub-5ms non-blocking inter-conversation RPC dispatcher powering ClockEE automated handoffs between all conversations.
---

# Sub-5ms Non-Blocking Inter-Conversation RPC Dispatcher

Reel: #30 (https://www.instagram.com/p/DfY3CZ_BkXd/)
Package: `integrations/agentapi_rpc/`

## Capabilities
- Wraps `agentapi.bat send-message` with non-blocking `subprocess.Popen`.
- Delivers handoff messages across conversation IDs in <5ms without stalling the caller.
- Includes queue fallback and retry buffer.
