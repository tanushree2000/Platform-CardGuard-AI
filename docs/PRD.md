CardGuard AI

Product Requirements Document

Author: Tanushree Poojary
Role: AI Product Manager
Status: MVP
Product: AI-Powered Transaction Identification & Dispute Support Platform

⸻

1. Change History

Version	Change	Owner
v1.0	Defined product problem, MVP scope and safety model	Tanushree Poojary
v1.1	Added agent architecture, guardrails and evaluation requirements	Tanushree Poojary
v1.2	Added rollout strategy and success metrics	Tanushree Poojary

⸻

2. Overview

Problem

Customers sometimes see transactions on their card that they do not recognize. Resolving these cases can involve several separate steps: identifying the transaction, explaining relevant policies, determining whether a dispute is appropriate, protecting the account and escalating suspicious activity to Fraud Operations.

A traditional chatbot can explain information but cannot manage the complete workflow. At the same time, allowing an AI agent to independently perform consequential actions such as locking a card creates unacceptable risk.

Product

CardGuard AI is a bounded AI agent designed to help customers identify and resolve unfamiliar card transactions while keeping consequential actions under deterministic product controls.

The core product principle is:

Reasoning is not authorization.

The AI can classify intent, retrieve information, summarize, explain and recommend actions. Product policy controls approvals, account state, tool execution, persistence and escalation.

All MVP account data and actions are synthetic.

⸻

3. Objectives

CardGuard AI should:

* Help users understand unfamiliar transactions.
* Retrieve relevant policy information before recommending next steps.
* Guide users through dispute workflows.
* Escalate suspicious or uncertain cases appropriately.
* Require explicit approval before consequential account actions.
* Protect sensitive information throughout the workflow.
* Maintain an auditable record of agent actions and decisions.

⸻

4. Success Metrics

North Star Metric

Safe Resolutions per 1,000 Eligible Agent Sessions

This measures whether the agent successfully helps users while operating within defined safety boundaries.

Supporting Metrics

Metric	Target
Unauthorized consequential actions	0
MVP regression scenarios passing	100%
PII protection	No exposed sensitive information
Consequential actions without approval	0

The primary hard guardrail is zero unauthorized consequential actions.

⸻

5. Personas

Primary — Cardholder

A customer who notices a transaction they do not immediately recognize and wants to understand what happened and determine what to do next.

Needs: Fast explanation, clear next steps, account safety and confidence before taking action.

Secondary — Fraud Operations Specialist

An internal specialist responsible for reviewing cases that require human judgment or additional investigation.

Needs: Clear context, escalation information and an auditable history of the AI interaction.

⸻

6. User Scenarios

Scenario 1 — Transaction identified

A customer asks about an unfamiliar transaction.

CardGuard retrieves the transaction, provides relevant context and helps the customer recognize it.

Outcome: No unnecessary dispute is created.

Scenario 2 — Customer wants to dispute

The customer still does not recognize the transaction.

CardGuard retrieves the appropriate policy, explains the dispute process and collects the information required to create a synthetic dispute.

Outcome: The customer receives a clear guided resolution path.

Scenario 3 — Potential account compromise

The interaction suggests that the customer’s card may be compromised.

CardGuard recommends account protection. A card lock cannot occur automatically.

Outcome: The system asks for explicit customer approval before the action proceeds.

Scenario 4 — Agent cannot safely resolve

The available information is insufficient or the case requires human judgment.

Outcome: CardGuard escalates the case rather than attempting to resolve it autonomously.

⸻

7. User Stories / Features / Requirements

P0 — Transaction Retrieval

As a cardholder, I want the system to retrieve the relevant transaction so that I can understand what the charge represents.

Requirement: The agent must identify the correct transaction before providing transaction-specific guidance.

⸻

P0 — Intent Routing

As a cardholder, I want the system to understand whether I am asking for an explanation, dispute or account-protection action.

Requirement: Requests must be routed to the appropriate domain workflow.

⸻

P0 — Governed Policy Retrieval

As a cardholder, I want answers based on applicable policies rather than unsupported AI-generated information.

Requirement: Policy-related responses must use approved policy retrieval.

⸻

P0 — Explicit Approval

As a cardholder, I want control over actions that affect my account.

Requirement: Consequential actions such as card locking require explicit approval before execution.

The LLM must never serve as the authorization layer.

⸻

P0 — Human Escalation

As a customer, I want uncertain or high-risk situations reviewed by the appropriate specialist.

Requirement: The system must support escalation when the agent cannot safely complete the workflow.

⸻

P0 — PII Protection

As a customer, I expect sensitive financial information to remain protected.

Requirement: Personally identifiable information must be redacted where required before model processing or logging.

⸻

P0 — Audit Trail

As a Fraud Operations specialist, I need visibility into what the agent did so that cases can be reviewed.

Requirement: Important agent decisions, tool calls, approvals and outcomes must be auditable.

⸻

P1 — Fraud Operations Console

Provide specialists with an internal interface for reviewing escalated cases and relevant interaction context.

⸻

P1 — Regression Evaluation

Maintain evaluation scenarios covering normal workflows, unsafe requests and adversarial behavior.

A release should not proceed if critical safety scenarios fail.

⸻

8. System Design

High-Level Architecture

Customer UI → FastAPI → LangGraph Agent → OpenAI / Policy Retrieval / Domain Tools → PostgreSQL

Agent Workflow

Safety Check → Intent Classification → Domain Workflow → Approval or Escalation → Outcome

The architecture intentionally separates AI reasoning from authorization.

The LLM determines what information may be relevant and what action could be appropriate.

Deterministic application logic determines whether that action is permitted.

⸻

9. Designs

The MVP contains two primary interfaces:

Customer UI

Supports transaction identification, explanations, dispute guidance, approvals and escalation.

Fraud Operations Console

Supports internal review of escalated cases and agent interaction history.

Detailed interface designs can evolve independently as long as the safety and approval requirements remain unchanged.

⸻

10. Features Out

The following are intentionally outside the MVP:

Fully autonomous financial actions
The agent will not independently perform consequential account actions.

Unrestricted tool access
The model will only interact with approved domain tools.

Automatic expansion of AI authority
Additional autonomy must be supported by evaluation evidence before release.

Production financial transactions
The MVP uses synthetic account data and synthetic account actions.

⸻

11. Release Plan

Phase 1 — Prototype

Validate the end-to-end workflow using synthetic data.

Phase 2 — Offline & Adversarial Evaluation

Test expected workflows, failure cases, prompt injection and safety boundaries.

Phase 3 — Shadow Mode

Evaluate agent behavior without allowing it to control consequential account actions.

Phase 4 — Specialist-Assisted

Allow Fraud Operations specialists to review AI recommendations.

Phase 5 — Limited Pilot

Release bounded capabilities to a controlled user population.

Phase 6 — Evidence-Based Autonomy

Expand capabilities only when evaluation and operational evidence demonstrate that doing so is safe.

⸻

12. Open Issues

* What confidence or evidence should trigger automatic escalation?
* Which additional account actions should require explicit approval?
* What evaluation threshold should block a release?
* What information should Fraud Operations receive during escalation?
* How long should agent decision and audit records be retained?
* Which additional adversarial scenarios should be included before pilot launch?

These remain open until supported by sufficient product, technical or evaluation evidence.

⸻

13. Q&A

Why not build a normal chatbot?

Transaction resolution involves workflows and actions, not only answering questions. A chatbot can explain information but cannot effectively coordinate the full resolution process.

Why not allow the AI to act autonomously?

The system operates in a financial context where incorrect consequential actions can create significant customer risk.

Therefore:

Reasoning is not authorization.

What happens when the agent is uncertain?

It escalates rather than guessing.

How will additional autonomy be introduced?

Only after evaluation and operational evidence show that the capability can operate within the defined safety requirements.

⸻

14. Other Considerations

Security

Prompt injection, inappropriate tool use and PII exposure must be evaluated before release.

Observability

Agent workflows should provide enough visibility to understand failures, tool calls, escalations and outcomes.

Product Principle

CardGuard AI is designed around bounded autonomy:

Use AI where reasoning creates value. Use deterministic systems where control matters.
