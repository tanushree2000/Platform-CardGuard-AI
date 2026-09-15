CardGuard AI — Product Requirements Document

Author: Tanushree Poojary
Role: AI Product Manager
Status: MVP
Last Updated: September 2026

⸻

1. Overview

Problem

When customers see an unfamiliar card transaction, resolving it can involve multiple systems and decisions: transaction lookup, merchant identification, policy retrieval, dispute intake, account protection, and Fraud Operations escalation.

A traditional chatbot can explain information but cannot safely manage the complete workflow. On the other hand, allowing an LLM to independently take actions such as locking a card creates unacceptable risk.

Product Decision

CardGuard AI is a bounded AI agent that helps customers understand and resolve unfamiliar transactions while keeping consequential actions behind deterministic controls.

Reasoning is not authorization.

The AI can:

* Classify intent
* Retrieve information
* Summarize policies
* Explain transactions
* Recommend next steps

Deterministic product logic controls:

* Tool execution
* Account state
* User approvals
* Persistence
* Escalation

All MVP account data and actions are synthetic.

⸻

2. Goals

CardGuard AI should:

1. Help users understand unfamiliar transactions.
2. Provide policy-grounded explanations.
3. Guide users through dispute workflows.
4. Detect situations requiring account protection.
5. Require approval before consequential actions.
6. Escalate uncertain or high-risk cases.
7. Protect PII throughout the workflow.
8. Maintain an auditable record of agent activity.

Non-Goals

The MVP will not:

* Make autonomous financial decisions.
* Lock cards without explicit approval.
* Give the LLM unrestricted tool access.
* Process real financial transactions.
* Expand agent autonomy without evaluation evidence.

⸻

3. Personas

Cardholder

A customer who sees a transaction they do not recognize.

Needs

* Understand the transaction quickly.
* Know whether action is required.
* Receive clear next steps.
* Stay in control of account changes.

Fraud Operations Specialist

An internal specialist reviewing cases the AI cannot safely resolve.

Needs

* Understand why the case was escalated.
* Review relevant transaction context.
* See what the agent already attempted.
* Access an audit trail of actions and approvals.

⸻

4. User Scenarios

Scenario 1 — Customer recognizes the transaction

1. Customer selects an unfamiliar transaction.
2. CardGuard retrieves transaction context.
3. The agent explains available merchant and transaction information.
4. Customer recognizes the transaction.
5. Case is resolved without creating a dispute.

Scenario 2 — Customer wants to dispute

1. Customer does not recognize the transaction.
2. CardGuard retrieves the relevant policy.
3. Agent explains available resolution options.
4. Customer chooses to continue.
5. Required dispute information is collected.
6. A synthetic dispute is created.

Scenario 3 — Possible account compromise

1. Interaction indicates potential fraud.
2. Agent recommends protecting the account.
3. System requests explicit approval.
4. Customer confirms the action.
5. Deterministic product logic executes the synthetic card-lock workflow.

Scenario 4 — Agent cannot safely resolve

1. Agent encounters uncertainty or a restricted situation.
2. It stops the autonomous workflow.
3. Relevant context is captured.
4. Case is escalated to Fraud Operations.

⸻

5. Requirements

Priority	Requirement	Description
P0	Transaction Retrieval	Retrieve the correct transaction before providing transaction-specific guidance.
P0	Intent Routing	Route requests to the appropriate transaction, dispute, protection, or escalation workflow.
P0	Policy Retrieval	Ground policy-related answers in approved policy content.
P0	Approval Layer	Require explicit approval before consequential actions.
P0	PII Protection	Prevent sensitive information from being unnecessarily exposed to the model or logs.
P0	Escalation	Route uncertain or restricted cases to Fraud Operations.
P0	Audit Trail	Record important agent decisions, tool calls, approvals, and outcomes.
P0	Prompt-Injection Protection	Prevent untrusted instructions from bypassing system policies or tool controls.
P1	Fraud Ops Console	Give specialists context for escalated cases.
P1	Regression Evaluations	Test normal, failure, safety, and adversarial scenarios before releases.

⸻

6. System Architecture

┌─────────────────┐
│   Customer UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     FastAPI     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LangGraph Agent │
└────────┬────────┘
         │
         ├──────────────► OpenAI
         │
         ├──────────────► Policy Retrieval
         │
         ├──────────────► Domain Tools
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
└─────────────────┘

Agent Flow

User Request
     │
     ▼
Safety Check
     │
     ▼
Intent Classification
     │
     ▼
Domain Workflow
     │
     ▼
Action Required?
   /     \
 No       Yes
 │         │
 │         ▼
 │    Approval Required?
 │       /       \
 │     Yes        No
 │      │          │
 │      ▼          ▼
 │  User Approval  Execute Allowed Action
 │
 ▼
Outcome / Escalation

The LLM is never the authorization layer.

It may determine what action could be useful, but deterministic application logic determines whether the action is allowed.

⸻

7. Safety & Guardrails

Financial workflows require stronger controls than a standard conversational assistant.

Consequential Actions

Actions affecting account state require deterministic authorization.

For example:

Agent recommends card lock
          ↓
Product policy checks eligibility
          ↓
User receives confirmation request
          ↓
User explicitly approves
          ↓
Application executes action
          ↓
Action recorded in audit trail

PII

Sensitive information should be minimized or redacted before being sent to the model or stored in logs where appropriate.

Prompt Injection

User or retrieved content must not be able to override system policies, authorization rules, or tool permissions.

Human-in-the-Loop

When the agent cannot safely complete a workflow, escalation is preferred over guessing.

⸻

8. Success Metrics

North Star

Safe Resolutions per 1,000 Eligible Agent Sessions

This measures whether CardGuard successfully resolves customer problems while remaining inside defined safety boundaries.

Guardrail Metrics

Metric	MVP Target
Unauthorized consequential actions	0
Consequential actions without approval	0
Critical MVP regression scenarios	100% pass

These guardrails take priority over increasing agent autonomy.

⸻

9. Evaluation Strategy

The agent should be evaluated across:

* Successful transaction identification
* Unrecognized transaction flows
* Policy retrieval
* Dispute workflows
* Account-protection workflows
* Approval enforcement
* PII handling
* Prompt injection
* Tool misuse
* Escalation behavior
* Failure recovery

A release should not proceed when critical safety evaluations fail.

⸻

10. Release Strategy

CardGuard uses progressive rollout rather than immediately granting the agent broad autonomy.

Prototype
   ↓
Offline Evaluation
   ↓
Adversarial Evaluation
   ↓
Shadow Mode
   ↓
Specialist-Assisted
   ↓
Limited Pilot
   ↓
Evidence-Based Autonomy Expansion

Phase 1 — Prototype

Validate the complete workflow using synthetic data.

Phase 2 — Offline & Adversarial Evaluation

Test expected behavior, failure cases, prompt injection, and safety boundaries.

Phase 3 — Shadow Mode

Observe agent decisions without allowing consequential actions.

Phase 4 — Specialist-Assisted

Allow Fraud Operations specialists to review AI recommendations.

Phase 5 — Limited Pilot

Introduce bounded functionality to a controlled user group.

Phase 6 — Evidence-Based Expansion

Increase autonomy only when evaluation and operational evidence support the change.

⸻

11. Open Questions

* What conditions should automatically trigger escalation?
* What evidence should be required before increasing agent autonomy?
* Which additional account actions require explicit approval?
* What evaluation failures should block a release?
* What context should Fraud Operations receive during escalation?
* How long should audit records be retained?
* What additional adversarial scenarios should be tested?

These questions intentionally remain open until supported by sufficient product or evaluation evidence.

⸻

12. Key Product Principle

CardGuard AI is designed around bounded autonomy:

Use AI where reasoning creates value. Use deterministic systems where control matters.

The objective is not to maximize how many decisions the AI can make.

The objective is to maximize how many customer problems it can safely resolve.
