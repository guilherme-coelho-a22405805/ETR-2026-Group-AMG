# Requirements Map — Lab 3

## EPIC-1 — Intake & Intelligent NBQ
* **REQ-001** — Geração de Next-Best-Question (NBQ)
* **REQ-006** — Validação de Evidência (Freshness)

## EPIC-2 — Scoring & Explainability
* **REQ-002** — Cálculo de Continuity Score
* **REQ-003** — **[Variante]** Explicabilidade via Top 5 Drivers
* **REQ-005** — Cálculo de Change Risk Assessment
* **REQ-007** — **[Variante]** Endpoint de Metodologia (/explain)
* **REQ-010** — **[Variante]** Execução Determinística

## EPIC-3 — Sizing & Estimation
* **REQ-004** — Estimativa de Sizing FTE (P10/P50/P90)

## EPIC-4 — Architecture & Quality (NFRs)
* **NFR-001** — Performance (Latency $\le$ 500ms)
* **NFR-003** — **[Variante]** Hash Check de Determinismo
* **NFR-004** — Statelessness
* **NFR-006** — **[Variante]** Human-readable Labels

***

### Variant Coverage Summary
* **Variant number:** Group 3 (Explicabilidade e Determinismo)
* **Variant-driven requirements:** REQ-003, REQ-007, REQ-010
* **Variant-driven NFRs:** NFR-003, NFR-006