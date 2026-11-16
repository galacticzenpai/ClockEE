# OmniRoute - Unified Multi-Provider AI Token Gateway & Fallback Router

## Skill Overview
`omniroute` is an open-source, OpenAI-compatible local AI gateway and smart multi-tier router. It connects hundreds of AI providers and free tiers (Google AI Studio / Gemini, Groq, Cerebras, Mistral, OpenRouter, GitHub Models, Ollama, DeepSeek) behind a single unified local endpoint (`http://localhost:20128/v1`).

Featured in Developer Showcase: Reel #4 (`https://www.instagram.com/p/De6ttI-zAba/` by `@tech.oak`).

---

## Key Capabilities
1. **Unified OpenAI-Compatible Endpoint**: Point any coding assistant, mesh agent, or Python client to `http://localhost:20128/v1` with `Authorization: Bearer <omniroute_key>`.
2. **Auto Fallback & Rate Limit Evasion**: When provider A hits HTTP 429 rate limit or quota exhaustion, OmniRoute automatically cascades and reroutes to provider B without throwing unhandled errors to the caller.
3. **Multi-Provider Pooling**: Aggregates free-tier monthly tokens across multiple accounts and providers into a steady pool of inference.
4. **Token & Cost Observability**: Tracks usage, latency, and failure rates per provider in a local SQLite database and dashboard.

---

## Directory Structure
- `integrations/omniroute/`
  - `SKILL.md`: Architecture reference and integration guide.
  - `omniroute_client.py`: Python client wrapper supporting streaming, failover routing, and health probes.
  - `providers_config.json`: Tier catalog and fallback cascade configuration.
  - `setup.sh` / `setup.bat`: Quick launch scripts.

---

## Usage Instructions

### 1. Launching OmniRoute via Global NPM
```bash
# Install globally
npm install -g omniroute

# Run headless or with dashboard
omniroute --port 20128
```

### 2. Using Python Helper Client (`omniroute_client.py`)
```python
from integrations.omniroute.omniroute_client import OmniRouteGateway

gateway = OmniRouteGateway(base_url="http://localhost:20128/v1", api_key="sk-omni-local")
response = gateway.chat_completion(
    model="router/fast-tier",
    messages=[{"role": "user", "content": "Explain ClockEE pomodoro algorithm"}]
)
print(response)
```

### 3. Local Fallback Simulation Mode
When the live npm OmniRoute daemon is not running, `OmniRouteGateway` operates in resilient local fallback mode, testing upstream endpoints directly or returning cached synthetic responses for offline testing.
