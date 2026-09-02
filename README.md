# CardGuard AI
## Production-Style Credit-Card Fraud Resolution Agent

**Built by Tanushree Poojary | AI Product Management Portfolio**

CardGuard is a full-stack agentic product for unfamiliar credit-card transactions. It includes a customer web app, Fraud Operations console, FastAPI backend, PostgreSQL persistence, LangGraph orchestration, optional OpenAI reasoning, governed policy retrieval, human approval gates, LangSmith-ready tracing, PostHog analytics, automated evals, Postman APIs, Jira backlog and Docker deployment.

**Core principle:** the model may reason, retrieve, summarize and recommend. Deterministic product policy controls consequential actions.

## Demo flow
Customer selects an unfamiliar transaction → agent identifies it → retrieves fraud policy → creates a synthetic dispute case → recommends card lock → explicit approval required → synthetic card state changes only after approval → case appears in Fraud Operations.

## Stack
- Next.js + React + TypeScript
- FastAPI + Python
- PostgreSQL
- LangGraph
- OpenAI Responses API
- LangSmith-ready tracing
- PostHog analytics
- Pytest + agent evals
- Postman
- Jira-ready CSV
- Docker + GitHub Actions

## Run
```bash
cp .env.example .env
docker compose up --build
```

Open:
- Customer: http://localhost:3000/customer
- Fraud Ops: http://localhost:3000/ops
- API docs: http://localhost:8000/docs

No OpenAI key is required for the demo workflow; a deterministic safe classifier is used as fallback.

## Truthfulness
All users, cards, transactions, policies and account actions are synthetic. This is not connected to a bank or card network and does not claim real production outcomes or regulatory certification.
