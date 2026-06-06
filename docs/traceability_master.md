# Traceability Master — Lab 14 (REQ → AC → Tests → Evidence)

**Team:** ETR-2026-Group-AMG (G3 — AI Engine)
**Variant:** Group 3 — Determinism + Explainability
**Slice:** Continuity Score (UC-02) + Explain (UC-05)
**Single source of truth:** este ficheiro consolida e substitui as matrizes parciais anteriores (`traceability_req_tc.md`, `traceability_req_bdd.md`, `traceability_req_ac_tc.md`, `traceability_uc_req.md`), que ficam como histórico por lab.

## Legenda
- **TC-###** — Test Case (especificação, `docs/test_cases.md`)
- **UT-##** — Unit test implementado (`tests/test_engine.py`)
- **Evidence** — onde está a prova de execução
- **OOS** — Out Of Scope (fora do slice escolhido; ver `docs/gap_analysis_lab14.md`)

## Matriz consolidada (todos os REQ + NFR)

| REQ-### | Tipo / Variant | AC reference | Test Case (TC/UT) | BDD Scenario (Feature / Scenario) | Evidence (where) | Notes |
|---|---|---|---|---|---|---|
| **REQ-002** | FR | AC-1 (0–100), AC-2 (policyVersion), AC-3 (uncertainty) | TC-001, TC-003, TC-006 / UT-08 | lab9, lab13 / Happy path; Alternative flow; Boundary | `docs/bdd_report.md`, `docs/unit_test_report.md` | Core scoring; clamp validado em TC-006 |
| **REQ-006** | FR · **Variant** | Top 5 drivers ordenados por contribuição absoluta desc | TC-002, TC-008 / **UT-03** | lab9, lab13 / Happy path; Determinism (tampering) | `docs/bdd_report.md`, `docs/unit_test_report.md` | **UT-03 reescrito no Lab 14** para chamar `explain_score()` real |
| **REQ-007** | FR · **Variant** | AC-1 (append-only), AC-2 (checksum SHA-256), AC-3 (DEPRECATED) | TC-010 / UT-07 | — | `docs/unit_test_report.md` | Sem cenário BDD dedicado (ver gap analysis G-2) |
| **REQ-009** | FR | Missing fields (E1), invalid enum, clamp | TC-001, TC-003, TC-004, TC-005, TC-006 / UT-02, UT-04, UT-05 | lab9, lab13 / Negative path | `docs/bdd_report.md`, `docs/unit_test_report.md` | Cobertura mais densa do conjunto |
| **REQ-010** | FR · **Variant** | Hashes idênticos p/ mesmos inputs; replay bloqueia adulteração | TC-007, TC-008, TC-009 / UT-01, UT-06 | lab9, lab11, lab13 / Determinism (identical features); tampering; Boundary | `docs/bdd_report.md`, `docs/unit_test_report.md` | Determinismo end-to-end |
| **NFR-006** | NFR · **Variant** | 100% coincidência de output em re-execução | TC-009 / UT-01 | lab9 / Determinism (identical features) | `docs/unit_test_report.md` | Verificada em re-run (hash + score) |
| **NFR-008** | NFR · **Variant** | Top 5 drivers com labels legíveis obrigatórios | TC-002, TC-010 / UT-03 | lab9, lab13 / Happy path (label não-vazio) | `docs/bdd_report.md`, `docs/unit_test_report.md` | Conflito "< 5 fatores" documentado (ver retrocompat. F-3) |
| **REQ-001** | FR | NBQ: 200 OK `{id,text,weight,why}` / `{done:true}` | — | — | OOS | NBQ fora do slice (ver gap G-1) |
| **REQ-003** | FR | `risk0to100` + drivers + guardrails | — | — | OOS | Change Risk fora do slice |
| **REQ-004** | FR | Bandas FTE P10/P50/P90 + assumptions | — | — | OOS | Sizing fora do slice |
| **REQ-005** | FR | Recomendações 90-dias (impacto/esforço) | — | — | OOS | Fora do slice |
| **REQ-008** | FR | Catálogo de features mapeado ao G1 | — | — | OOS | Fora do slice |
| **NFR-001** | NFR | p95 ≤ 500ms scoring/NBQ (server time) | TC-009 (proxy) | — | Parcial / OOS-medição | Performance não medida formalmente; Lighthouse (Lab 13) mediu front-end, não o motor |
| **NFR-002** | NFR | p95 ≤ 800ms sizing | — | — | OOS | Depende de REQ-004 (OOS) |
| **NFR-003** | NFR | 99.9% uptime, `/health` `/ready` | — | — | OOS | Sem endpoints REST no protótipo |
| **NFR-004** | NFR | Rate limiting 5 RPS | — | — | OOS | Explicitamente fora do scope (Lab 8) |
| **NFR-005** | NFR | Logs estruturados JSON | — | — | OOS | Fora do scope (Lab 8) |
| **NFR-007** | NFR | ≥ 70% cobertura módulos core | UT-01..08 (proxy) | — | `docs/unit_test_report.md` | Cobertura qualitativa; sem ferramenta de % formal |

## Cobertura do slice (resumo)

- **REQs do slice cobertos por testes:** REQ-002, REQ-006, REQ-007, REQ-009, REQ-010 (5/5) ✅
- **NFRs variant cobertos:** NFR-006, NFR-008 (2/2) ✅
- **Variant-driven cobertos:** REQ-006, REQ-007, REQ-010, NFR-006, NFR-008 (≥ 2 exigidos) ✅
- **NFRs incluídos na matriz:** ≥ 2 exigidos — incluídos NFR-006 e NFR-008 com testes, mais os restantes como contexto ✅
- **Total de linhas REQ/NFR na matriz:** 18 (≥ 10 exigidos) ✅

## Mudanças aplicadas nesta consolidação (Lab 14)
1. **UT-03** passou a referenciar a execução real de `explain_score()` (antes não chamava o motor — ver `docs/test_grooming_report.md`, ação 2).
2. Estado do BDD atualizado para refletir o suite completo após resolução do `AmbiguousStep` (3 features / 12 cenários / 94 steps — ver grooming ação 1).
3. REQs fora do slice marcados explicitamente como **OOS** com justificação cruzada em `docs/gap_analysis_lab14.md`.
