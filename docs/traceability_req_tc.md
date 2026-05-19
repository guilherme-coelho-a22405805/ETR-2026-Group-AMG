# Traceability — Requirements ↔ Test Cases (Lab 9)

**Slice:** Continuity Score + Explain (UC-02 + UC-05)
**Variant:** Group 3 — Determinism + Explainability

---

## Selected requirements 

| # | REQ ID | Type | Title | Variant impact |
|---|---|---|---|---|
| 1 | **REQ-002** | FR | Continuity Score (Readiness) | No |
| 2 | **REQ-006** | FR | Explain Endpoint (Human-readable drivers) | **Yes** |
| 3 | **REQ-009** | FR | Input Validation & Normalization | No |
| 4 | **REQ-010** | FR | Determinism & Replay Metadata | **Yes** |
| 5 | **NFR-006** | NFR | Output Consistency (Hash Match) | **Yes** |
| 6 | **NFR-008** | NFR | Top 5 Drivers Labeling | **Yes** |
| 7 | **REQ-007** | Other (governance) | Policy Versioning & Registry | **Yes** |
| 8 | **NFR-001** | Other (NFR perf.) | Latência Scoring/NBQ p95 ≤ 500ms | No |


---

## Mapping (REQ → TC)

| Requirement (REQ-###) | Test Cases (TC-###) | Coverage | Notes |
|---|---|---|---|
| **REQ-002** (FR) | TC-001, TC-003, TC-006 | Happy + Alt + Boundary | Core scoring logic |
| **REQ-006** (FR, Variant) | TC-002, TC-008 | Happy + Negative (E1) | Top 5 drivers + tampering block |
| **REQ-009** (FR) | TC-001, TC-003, TC-004, TC-005, TC-006 | Happy + Alt + 2 Negative + Boundary | Validação cobre múltiplos caminhos |
| **REQ-010** (FR, Variant) | TC-007, TC-008, TC-009 | Alt + Negative + Happy | Determinismo end-to-end |
| **NFR-006** (NFR, Variant) | TC-009 | Acceptance | 100% coincidência em re-execução |
| **NFR-008** (NFR, Variant) | TC-002, TC-010 | Happy + Unit | Top 5 drivers + labels legíveis |
| **REQ-007** (Other, Variant) | TC-010 | Unit | Imutabilidade + checksum único |
| **NFR-001** (Other, NFR) | TC-009 (proxy) | Acceptance | Verificação formal em Lab 10 |

---

