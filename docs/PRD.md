# CardGuard AI

CardGuard AI is a prototype for handling unrecognized credit card transactions using an AI-assisted workflow.

The product helps users understand a transaction, check relevant policies, decide what to do next, and start a dispute or account-protection workflow when needed.

The main product decision was to keep AI reasoning separate from authorization. The AI can understand the request, retrieve information, explain policies, and recommend an action, but it cannot independently perform sensitive account actions.

> **Reasoning is not authorization.**

All transactions and account actions used in this project are synthetic.

---

## Problem

When someone sees a transaction they do not recognize, resolving it can involve several steps:

- Finding the transaction
- Understanding the merchant or charge
- Checking the relevant policy
- Deciding whether to dispute it
- Protecting the account if fraud is suspected
- Escalating the case when needed

I wanted to understand how an AI agent could support this process without giving the model full control over account actions.

---

## Product Approach

The AI can:

- Understand the user's request
- Retrieve transaction information
- Retrieve relevant policies
- Explain the transaction
- Recommend next steps
- Guide the user through a dispute

Actions that affect the account are controlled by application logic and require approval where appropriate.

If the system cannot safely handle a request, it escalates the case instead of guessing.

---

## How It Works

```text
Customer
   |
   v
Customer UI
   |
   v
FastAPI
   |
   v
LangGraph Agent
   |
   +---- OpenAI
   +---- Policy Retrieval
   +---- Domain Tools
   |
   v
PostgreSQL
```

A typical request follows this flow:

```text
User Request
     |
     v
Safety Check
     |
     v
Intent Detection
     |
     v
Transaction / Policy Workflow
     |
     v
Recommendation
     |
     +---- Approval Required ----> User Approval
     |
     +---- Cannot Resolve -------> Escalation
     |
     v
Outcome
```

The LLM is not the authorization layer. It can recommend an action, but application logic determines whether the action is allowed.

---

## Example Workflow

A user says:

> "I don't recognize this transaction."

The system retrieves the transaction and determines what the user is trying to do.

If more information is available, it explains the transaction and retrieves the relevant policy.

If the user wants to dispute the transaction, the system guides them through the required steps.

If account protection is recommended, the system asks for explicit approval before continuing.

If the case cannot be handled safely, it is escalated.

---

## MVP Scope

The MVP includes:

- Transaction retrieval
- Intent routing
- Policy-grounded retrieval
- Synthetic dispute creation
- Approval before card lock
- PII protection
- Prompt-injection protection
- Human escalation
- Audit trail
- Customer interface
- Fraud Operations workflow
- Regression evaluations

The MVP does not use real financial accounts or process real financial transactions.

---

## Safety

The main controls are:

- Explicit approval for sensitive actions
- Restricted tool access
- PII redaction
- Prompt-injection protection
- Human escalation
- Audit logging
- Regression testing

The LLM is never used as the authorization layer.

---

## Success Metrics

### North Star Metric

**Safe Resolutions per 1,000 Eligible Agent Sessions**

### MVP Guardrails

| Metric | Target |
|---|---:|
| Unauthorized consequential actions | 0 |
| Actions without required approval | 0 |
| Critical MVP regression scenarios | 100% pass |

---

## Rollout

The product would be introduced gradually:

1. Prototype
2. Offline evaluation
3. Adversarial testing
4. Shadow mode
5. Specialist-assisted workflow
6. Limited pilot
7. Evidence-based autonomy expansion

Agent capabilities are expanded only when evaluation results support the change.

---

## Tech Stack

| Area | Tools |
|---|---|
| Frontend | Next.js |
| Backend | Python, FastAPI |
| Agent | LangGraph, OpenAI |
| Data | PostgreSQL |
| Retrieval | RAG |
| Observability | LangSmith |
| Analytics | PostHog |
| API Testing | Postman |
| Infrastructure | Docker |

---

## Documentation

| Document | Description |
|---|---|
| [Product Requirements Document](docs/PRD.md) | Problem, scope, requirements, users and metrics |
| [Agent Architecture](docs/AGENT_ARCHITECTURE.md) | System and agent workflow |
| [AI Product Strategy](docs/AI_PRODUCT_STRATEGY.md) | Product decisions and strategy |
| [Guardrails & HITL](docs/GUARDRAILS_HITL.md) | Approval and human-in-the-loop decisions |
| [Evaluations](docs/EVALS.md) | Evaluation approach |
| [RAG Strategy](docs/RAG_STRATEGY.md) | Retrieval approach |
| [Model Lifecycle](docs/MODEL_LIFECYCLE.md) | Model lifecycle |
| [Launch Risk](docs/LAUNCH_RISK.md) | Risks considered before release |
| [Observability](docs/LANGSMITH_OBSERVABILITY.md) | Monitoring and observability |

---

## My Role

I built CardGuard AI as an AI Product Management portfolio project.

My work included:

- Defining the product problem and MVP
- Writing the PRD
- Mapping user and agent workflows
- Defining product requirements
- Designing the approval and escalation logic
- Documenting the system architecture
- Defining product and safety metrics
- Creating the evaluation approach
- Planning the rollout strategy

The main principle I followed throughout the project was:

> **Use AI for reasoning. Keep sensitive actions behind clear product controls.**
