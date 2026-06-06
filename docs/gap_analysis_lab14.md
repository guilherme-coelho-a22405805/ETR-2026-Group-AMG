# Gap Analysis — Lab 14

**Team:** ETR-2026-Group-AMG (G3 — AI Engine) · **Variant 3** · Slice: Continuity Score + Explain
**Base:** `docs/traceability_master.md`

Esta análise cruza todos os REQ/NFR contra os testes (TC/UT) e cenários BDD existentes, classifica cada lacuna e define uma ação.

---

## 1) REQs com NENHUMA cobertura de teste (sem TC e sem cenário)

| ID | Lacuna | Ação |
|---|---|---|
| **REQ-001** (NBQ Service) | Fora do slice; sem TC nem cenário | **Out-of-scope** — NBQ não pertence ao slice Continuity+Explain (ver `docs/generated_scope.md`). Não testar neste projeto. |
| **REQ-003** (Change Risk) | Fora do slice | **Out-of-scope** — justificado em `generated_scope.md`. |
| **REQ-004** (Sizing FTE) | Fora do slice | **Out-of-scope**. |
| **REQ-005** (90-day Recommendations) | Fora do slice | **Out-of-scope**. |
| **REQ-008** (Feature Catalog) | Fora do slice | **Out-of-scope**. |
| **NFR-002/003/004/005** | Dependem de funcionalidades OOS ou de infra REST inexistente no protótipo | **Out-of-scope** — coerente com os limites declarados no Lab 8. |

> Todos os REQs do **slice escolhido** (REQ-002, 006, 007, 009, 010) têm pelo menos um teste **e** (exceto REQ-007) pelo menos um cenário BDD.

---

## 2) Testes / cenários SEM ligação a REQ

Revisão de `tests/test_engine.py` (UT-01..08) e dos feature files: **não há testes órfãos**. Todos os UT mapeiam para um REQ (ver matriz mestre). Todos os cenários BDD têm `# REQ links` no respetivo `.feature`.

| Item | Estado | Ação |
|---|---|---|
| UT-01..08 | Todos ligados a REQ-002/006/007/009/010 | OK — nenhuma ação |
| lab9 / lab11 / lab13 scenarios | Todos com REQ links em comentário | OK — nenhuma ação |

**Observação (menor):** `bdd/features/lab11.feature` e `bdd/features/lab9.feature` cobrem comportamento muito sobreposto ao de `lab13.feature` (são iterações dos mesmos REQ ao longo dos labs). Não é um teste órfão, mas é **duplicação histórica** — tratada como ponto de grooming, não como gap (ver `docs/test_grooming_report.md`).

---

## 3) Itens de AC NÃO cobertos por teste

| REQ / AC | Lacuna | Ação |
|---|---|---|
| **REQ-007 / AC-3** (aviso `DEPRECATED` quando política inativa) | O campo `policyStatus` existe em `explain_score`, mas nenhum TC/UT exercita o caminho com `v0.9.0` (deprecated) | **Ação registada (não corrigida neste lab):** adicionar UT futuro que faça explain de um run com `policyVersion=v0.9.0` e asserte `policyStatus == "deprecated"`. Já estava previsto como *next step* em `docs/bdd_report.md`. Mantido fora do âmbito do grooming desta sprint para não introduzir novo teste sem revisão de AC. |
| **NFR-008 / "obrigatoriamente top 5"** vs política com < 5 fatores | AC exige sempre 5, mas o código devolve `[:limit]` (pode dar < 5). Nenhum teste cobre política com < 5 fatores porque `v1.0.0`/`v0.9.0` têm sempre 6 | **AC precisa de reescrita** (já proposta em `docs/ac_dod_updates.md`, Item 2). Documentado como ponto frágil em `docs/test_retrocompatibility.md` (F-3). Sem teste novo até a AC ser formalmente atualizada. |
| **NFR-001 / p95 ≤ 500ms** | Sem medição formal de performance | **Out-of-scope de medição** neste protótipo. O Lighthouse (Lab 13) mediu o carregamento do front-end Streamlit, que **não** corresponde ao "server response time interno" do NFR-001. Distinção registada na matriz e em `requirements_validation.md`. |

---

## 4) Ações concluídas nesta sprint (Lab 14)

1. **Consolidada** a rastreabilidade num único ficheiro (`docs/traceability_master.md`), substituindo 4 matrizes parciais como source-of-truth.
2. **Resolvido o gap de fiabilidade do UT-03:** o teste passou a chamar `explain_score()` do motor real (antes re-implementava a ordenação numa lista local e não testava o código de produção). Ver grooming ação 2.
3. **Resolvido o bloqueio de execução do suite BDD:** removida a definição duplicada do step de ordenação que causava `AmbiguousStep`. Ver grooming ação 1.
4. **Classificados** todos os REQ/NFR fora do slice como OOS com justificação cruzada, fechando a leitura "REQ sem teste".
5. **Registadas** (sem corrigir código) as 2 lacunas de AC que exigem decisão de requisitos antes de virar teste (REQ-007 AC-3 e NFR-008 < 5 fatores).
