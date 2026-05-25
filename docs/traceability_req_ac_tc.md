## Traceability — REQ → AC → Test Cases / BDD (Lab 10)
| Requirement (REQ-###) | Acceptance Criteria (AC IDs or text refs) | Test Cases (TC-###) | BDD Scenario (Feature/Scenario) |
| ------ | ------ | ------ | ------ |
| **REQ-002** | AC-1, AC-2, AC-3 | TC-001, TC-003, TC-006 | Feature: lab9 / Scenario: Happy path; Alternative flow |
| **REQ-006** (Variant) | AC-Top 5 drivers (ordenação decrescente) | TC-002, TC-008 | Feature: lab9 / Scenario: Happy path; Determinism (tampering) |
| **REQ-009** | AC-Missing fields, invalid enums | TC-004, TC-005 | Feature: lab9 / Scenario: Negative path |
| **REQ-010** (Variant) | AC-Identical hashes para mesmos inputs | TC-007, TC-008, TC-009 | Feature: lab9 / Scenario: Determinism (identical features); Determinism (tampering) |
| **NFR-006** (Variant) | AC-100% output consistency | TC-009 | Feature: lab9 / Scenario: Determinism (identical features) |
| **NFR-008** (Variant) | AC-Labels legíveis | TC-002, TC-010 | Feature: lab9 / Scenario: Happy path |
| **REQ-007** (Variant) | AC-1, AC-2, AC-3 (SHA-256 Imutável) | TC-010 | |