# Agent Architecture
Next.js → FastAPI → LangGraph → OpenAI / policy retrieval / domain tools → PostgreSQL.

LangGraph state: safety → intent → domain workflow → approval/escalation → outcome.

The LLM is never the authorization layer.
