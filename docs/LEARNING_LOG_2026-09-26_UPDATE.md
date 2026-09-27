# 2026-09-26 Learning Log Update

## Architecture lesson from 3E

The first Bronze → Silver implementation exposed an important data-engineering distinction:

**preserving source records is not the same as defining a canonical business record.**

Bronze must preserve source evidence and provenance. Silver must interpret that evidence using explicit identity, deduplication, source-conflict, DQ, relationship, versioning, and late-arrival rules.

The observed `restaurants` provenance problem demonstrated why source metadata must not be casually mixed or overwritten during cross-source processing.

This led to an architecture review before continuing implementation.

## Current learning sequence

1. Understand the architecture manually.
2. Implement deterministic processing.
3. Validate correctness and idempotency.
4. Automate repetitive work.
5. Introduce AI-assisted automation.
6. Later introduce governed agentic workflows.

ADF and agentic automation are intentionally later learning stages; they are not being introduced to solve the current 3E problem prematurely.
