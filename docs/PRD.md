CardGuard AI

CardGuard AI is a prototype for handling unrecognized credit card transactions using an AI-assisted workflow.

The product helps a user understand a transaction, check relevant policies, decide what to do next, and start a dispute or account-protection workflow when needed.

The main product decision was to keep AI reasoning separate from authorization. The AI can understand the request, retrieve information, explain policies, and recommend an action, but it cannot independently perform sensitive account actions.

All transactions and account actions used in this project are synthetic.

Problem

When someone sees a transaction they do not recognize, resolving it can involve several steps:

* Finding the transaction
* Understanding the merchant or charge
* Checking the relevant policy
* Deciding whether to dispute it
* Protecting the account if fraud is suspected
* Escalating the case when needed

I wanted to see how an AI agent could support this process without giving the model full control over account actions.

Product Approach

CardGuard follows one main rule:

Reasoning is not authorization.

The AI can:

* Understand the user’s request
* Retrieve transaction information
* Retrieve relevant policies
* Explain the transaction
* Recommend next steps
* Guide the user through a dispute

Actions that affect the account are controlled by application logic and require approval where appropriate.

If the system cannot safely handle a request, it escalates the case instead of guessing.

How It Works

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

A typical request follows this flow:

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

Example

A user says:

I don’t recognize this transaction.

The system retrieves the transaction and determines what the user is trying to do.

If more information is available, it explains the transaction and relevant policy.

If the user wants to dispute the transaction, the system guides them through the required steps.

If account protection is recommended, the system asks for explicit approval before continuing.

If the case cannot be handled safely, it is escalated.

MVP Scope

The MVP includes:

* Transaction retrieval
* Intent routing
* Policy-grounded retrieval
* Synthetic dispute creation
* Approval before card lock
* PII protection
* Prompt-injection protection
* Human escalation
* Audit trail
* Customer interface
* Fraud Operations workflow
* Regression evaluations

The MVP does not use real financial accounts or process real financial transactions.

Safety

Safety is part of the product requirements, not a separate feature.

The main controls include:

* Explicit approval for sensitive actions
* Restricted tool access
* PII redaction
* Prompt-injection protection
* Human escalation
* Audit logging
* Regression testing

The LLM is not used as the authorization layer.

Success Metrics

The North Star metric for the product is:

Safe Resolutions per 1,000 Eligible Agent Sessions

The main MVP guardrail is:

Unauthorized consequential actions: 0

Critical MVP regression scenarios should also maintain a 100% pass rate before release.

Rollout

The product would be introduced gradually:

1. Prototype
2. Offline evaluation
3. Adversarial testing
4. Shadow mode
5. Specialist-assisted workflow
6. Limited pilot
7. Expand autonomy based on evaluation results

The idea is to increase what the agent can do only when there is enough evidence that the workflow is safe.

Tech Stack

* Python
* FastAPI
* Next.js
* LangGraph
* OpenAI
* PostgreSQL
* RAG
* LangSmith
* PostHog
* Docker
* Postman

Documentation

The repository includes the product and technical documentation I created while working through the project.

Document	What it covers
Product Requirements Document	Problem, scope, requirements, users and metrics
Agent Architecture	System and agent workflow
AI Product Strategy	Product decisions and strategy
Guardrails & HITL	Approval and human-in-the-loop decisions
Evaluations	Evaluation approach
RAG Strategy	Retrieval approach
Model Lifecycle	Model lifecycle
Launch Risk	Risks considered before release
Observability	Monitoring and observability

My Role

I built this as an AI Product Management portfolio project.

My work included defining the problem, writing the PRD, mapping the user and agent workflows, defining requirements and guardrails, documenting the system architecture, defining product metrics, and creating the evaluation and rollout approach.

The main product principle I followed throughout the project was:

Use AI for reasoning. Keep sensitive actions behind clear product controls.
