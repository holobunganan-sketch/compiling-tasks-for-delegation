# Task Delegation Compiler Design

## Goal

Create a reusable Agent Skill that lets a capable reasoning model convert a user's request into a deterministic execution package for a less capable model.

## Core contract

The compiler model owns interpretation, planning, material decisions, risk classification, environment adaptation, exception design, and acceptance criteria. The executor model receives bounded steps with explicit inputs, actions, expected results, evidence requirements, and escalation exits.

## Decisions approved by the user

1. The skill must classify work as `SAFE_TO_DELEGATE`, `CONDITIONAL`, or `HIGH_MODEL_REQUIRED`.
2. The compiler must inspect live project/task context whenever that context can change the execution plan.
3. Executor discretion is strictly bounded. Uncovered branches, material choices, and unexpected states must stop and escalate.
4. Every verifiable step carries an evidence chain and the executor produces `EXECUTION_REPORT.md`.
5. The skill is domain-general: engineering, research, document, data, file, and operational knowledge work.
6. Output mode is adaptive: simple work uses one `EXECUTION_PLAN.md`; complex work uses a multi-file execution package.
7. Compilation has two layers: a platform-independent task contract and an environment-specific execution plan.

## Architecture

The skill uses progressive disclosure. `SKILL.md` contains the short mandatory workflow and routes the model to focused references. Templates define single-file and multi-file outputs. A Python validator catches mechanical package defects. Evaluation cases exercise delegation, ambiguity, evidence, and escalation behavior.

## Quality bar

A compiled package passes only when a less capable executor can determine every next action without inventing a material decision. Every step must be observable, bounded, and auditable. Any unsafe or undefined branch must terminate with a stop code and escalation payload.
