# Traceability — Requirements ↔ BDD Scenarios (Lab 13)

## Selected requirements (min. 2)
- REQ-002 — Continuity Score computation (range 0–100, policyVersion, uncertainty flag)
- REQ-006 — Explainability: top 5 drivers ordered by absolute contribution
- REQ-009 — Input validation: mandatory fields rejection with error codes
- REQ-010 — Determinism: identical inputs always produce the same inputsHash

## Mapping (REQ → Scenario)

| Requirement | Scenario name | Feature file | Notes |
|---|---|---|---|
| REQ-002, REQ-006 | Happy path — complete payload produces a valid score with top 5 drivers | bdd/features/lab13.feature | Validates score range, policyVersion, inputsHash, uncertainty_applied=false, 5 ordered drivers with labels |
| REQ-009 | Negative path — payload missing responses field is rejected | bdd/features/lab13.feature | Validates MISSING_FIELDS error code and field list |
| REQ-002 AC-3 | Alternative flow — partial responses trigger uncertainty flag | bdd/features/lab13.feature | Only 2/6 factors provided → uncertainty_applied=true, 4 missing optional fields |
| REQ-010 | Boundary — score of zero when all factors are 0.0 | bdd/features/lab13.feature | All weights × 0.0 = score 0; also validates hash determinism across two identical runs |