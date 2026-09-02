# AI PM Interview Guide

## 60-second story
I built CardGuard to prove more than prompt writing. It is a full-stack unfamiliar-transaction agent with customer and Fraud Ops products, LangGraph orchestration, PostgreSQL persistence, governed policy retrieval and approval-gated card controls. My key product decision was separating reasoning from authorization. I also built the eval dataset, guardrails, LangSmith-ready tracing, PostHog analytics, model lifecycle and staged rollout plan. All account data is synthetic.

## Why LangGraph?
Stateful inspectable orchestration with explicit branches and approval boundaries.

## Why LangSmith + PostHog?
LangSmith answers “is the agent behaving correctly?” PostHog answers “are users getting value?”

## Why no vector DB yet?
The corpus is too small to justify it.

## Biggest production risk?
Operational action outside policy, not awkward prose.
