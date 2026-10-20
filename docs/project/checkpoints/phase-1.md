# westeros-foodflow Phase 1 Checkpoint — CSV / Medallion Foundation

**Status:** Completed  
**Source:** CSV-based westeros-foodflow foundation.

## Scope
- Established the initial CSV source and relationally meaningful restaurant/customer/order-style data foundations.
- Implemented the Medallion learning pattern:
  - Bronze — raw/ingested source representation.
  - Silver — cleaned, standardized, validated representation.
  - Gold — analytics-ready representation.
- Established ingestion metadata such as `_ingested_at` and `_ingestion_date`.
- Kept `_source_file` as ingestion/pipeline metadata for CSV ingestion.

## Architecture principle
The project should preserve raw source evidence in Bronze and apply business/data-quality transformations in Silver before producing Gold analytics.

## Later evolution
Phase 3 introduces a relational SQL source alongside the earlier CSV source. SQL ingestion uses SQL-specific metadata rather than relying on `_source_file`.

## Supersession
Phase 2 adds incremental CSV ingestion. Phase 3 adds the relational SQL source.
