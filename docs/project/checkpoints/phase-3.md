# westeros-foodflow Phase 3 Checkpoint — Relational SQL

**Checkpoint ID:** `FOODFLOW-2026-09-26-PHASE3-3E-ARCHITECTURE-LOCKED`
**Date:** 2026-09-26
**Phase:** Phase 3 — Relational SQL
**Current implementation point:** **Stage 3E — Bronze → Silver**

## 1. Phase 3 status

| Stage | Status |
|---|---|
| 3A — SQL Foundation | ✅ Complete |
| 3B — Stage A dataset | ✅ Complete |
| 3C — JDBC connectivity | ✅ Complete |
| 3D — SQL → Landing → Bronze | ✅ Complete |
| 3E — Bronze → Silver | 🔴 Current / blocked |
| Architecture review | ✅ Complete / locked |

Do not repeat 3A–3D.

## 2. Why 3E was blocked

The first Bronze → Silver implementation exposed a source provenance/source-resolution problem in mixed-source Bronze data. In `restaurants`, SQL ingestion metadata could coexist with an older CSV `_source_file`, demonstrating metadata contamination/overwriting during processing.

The project deliberately paused implementation and revisited the architecture rather than applying a narrow Silver merge patch.

## 3. Authoritative architecture

```text
Landing → Bronze → Silver → Gold

Control / Observability / Orchestration
```

Landing is exact source evidence. Bronze preserves source records plus minimal technical provenance. Silver interprets and resolves evidence into canonical business state. Gold is analytical consumption. The Control Plane owns operational metadata.

## 4. Locked architecture decisions

- Silver S-06 through S-22
- Gold G-23 through G-33
- Control Plane / Orchestration C-34 through C-43

Full definitions are in `docs/DECISIONS.md` and the master checkpoint.

## 5. Silver table behavior

| Table | Silver behavior |
|---|---|
| `customers` | Current-state MERGE; optional history |
| `restaurants` | Current-state MERGE with evidence-based source conflict resolution; optional history |
| `menu_items` | Current-state MERGE; optional history |
| `delivery_partners` | Current-state MERGE; optional history |
| `orders` | Mutable transactional state; MERGE; status history separate |
| `order_items` | Transaction detail/relationship; controlled MERGE/upsert |
| `payments` | Mutable transactional state; MERGE |
| `order_status_history` | Event/history; append + replay dedup |
| `restaurant_reviews` | Review identity/chronology-aware |
| `delivery_partner_reviews` | Review identity/chronology-aware |

Invalid evidence is retained. Missing parents do not delete children. Late-arriving data is reprocessed when required. Silver processing must be idempotent.

## 6. Next implementation

The next task is to translate the locked Silver contract into executable processing for the existing 3D Bronze data.

```text
Existing Bronze
      ↓
canonical identity
      ↓
deduplication
      ↓
source conflict resolution
      ↓
business / relationship / schema DQ
      ↓
current-state or event semantics
      ↓
idempotent Silver writes
      ↓
lineage + observability
      ↓
Silver validation
```

If implementation evidence demonstrates a genuine architecture defect, stop and document it before changing a locked decision. Otherwise, do not redesign.

## 7. Future Phase 3 sequence

```text
3E Bronze → Silver
      ↓
3F deterministic ~5K
      ↓
3G AI-assisted ~15K
      ↓
3H ADF introduction
      ↓
3I ~250K orders
```

Learning sequence:

```text
Understand manually
→ deterministic automation
→ AI-assisted automation
→ governed agentic workflows
```

ADF-specific architecture is intentionally not locked yet.

## 8. Historical checkpoint

`FOODFLOW-2026-09-26-PHASE3-SQL-BRONZE-COMPLETE.md` remains in the repository as historical evidence of the completed 3D stage and the state before the 3E architecture review. It is superseded for current architecture by this checkpoint; it is not deleted.
