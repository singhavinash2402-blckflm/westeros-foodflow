# Architecture Addendum — 2026-09-26

The authoritative layer architecture is now:

```text
Landing → Bronze → Silver → Gold
                         \
                          → BI / Analytics / ML

Control / Observability / Orchestration
```

Landing is source-faithful raw evidence. Bronze preserves source records and technical provenance. Silver owns canonicalization and business interpretation. Gold is business-facing analytical consumption. The Control Plane owns operational state.

Silver Decisions 6–22, Gold Decisions 23–33, and Control Plane/Orchestration Decisions 34–43 are locked.

This checkpoint supersedes any earlier ambiguity that treated SQL → Bronze as a direct canonicalization step or implied that Silver should simply append all source records.

3E must implement the locked contracts rather than redesign them.
