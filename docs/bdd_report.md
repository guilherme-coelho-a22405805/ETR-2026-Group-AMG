# BDD Automation Report — Lab 13

## Tool used
- Framework: Behave 1.2.6
- Language/stack: Python 3.13
- Module under test: `ai_engine` (scoring, validator, explain, policy)

## How to run

```bash
# A partir da raiz do projecto:
behave bdd\ --include lab13
```

Para correr apenas os cenários do Lab 13 isolados:
```bash
behave bdd\features\lab13.feature
```

## Execution results

| # | Scenario | Result |
|---|---|---|
| 1 | Happy path — complete payload produces a valid score with top 5 drivers | ✅ PASSED |
| 2 | Negative path — payload missing responses field is rejected | ✅ PASSED |
| 3 | Alternative flow — partial responses trigger uncertainty flag | ✅ PASSED |
| 4 | Boundary — score of zero when all factors are 0.0 | ✅ PASSED |

- **Date:** 24-05-2026
- **Scenarios executed:** 4
- **Passed:** 4
- **Failed:** 0
- **Skipped:** 0

```
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
22 steps passed, 0 failed, 0 skipped
Took 0min 0.05s
```

## Notes

### What worked well
- Chamada directa às funções do `ai_engine` (sem HTTP) garante testes rápidos e estáveis.
- O `_build_stored_run` helper reutilizado dos labs anteriores simplificou os steps do explain.
- O cenário de boundary (score = 0) valida simultaneamente REQ-002 (clamp) e REQ-010 (determinismo).

### Falhas e resoluções
- Nenhuma falha na execução final. Durante o desenvolvimento foi necessário inicializar `context.storage` dentro do step `when the payload is scored` para cenários cujo Background não inclui `"the storage for ScoringRuns is empty"`.

### Next steps
- Adicionar cenário de boundary superior: todos os fatores a 1.0 → score = 100.
- Cobrir REQ-007 (política deprecated): submeter com `policyVersion=v0.9.0` e verificar `policyStatus = "deprecated"` na resposta do explain.
- Integrar com API HTTP (FastAPI/Django Ninja) quando o endpoint estiver estável.

---

## Update — Lab 14 (Test Grooming) — 07-06-2026

> Esta secção foi acrescentada na sprint de manutenção do Lab 14. O registo de execução
> original acima é mantido como histórico (24-05-2026, Behave 1.2.6). Durante o grooming
> re-executámos o suite num ambiente atualizado e detetámos duas situações que justificam
> esta nota. Ver detalhe completo em `docs/test_grooming_report.md` e
> `docs/test_retrocompatibility.md`.

### O que mudou desde o Lab 13

1. **Retrocompatibilidade de ferramenta (Behave ≥ 1.3) — `AmbiguousStep`.**
   O step `@then('the drivers are ordered by absolute contribution descending')` estava
   definido em **dois** módulos (`bdd/steps/steps.py` e `bdd/steps/steps_lab13.py`).
   Em Behave 1.2.6 isto passava; em Behave ≥ 1.3 o suite deixa de arrancar
   (`behave.step_registry.AmbiguousStep`). **Corrigido na causa-raiz** removendo a
   definição duplicada de `steps_lab13.py` e reutilizando a de `steps.py`.

2. **Contagem de steps corrigida.**
   O registo original indicava "22 steps" para o `lab13.feature` isolado. A contagem
   real e reprodutível é **30 steps** (4 cenários, incluindo os `And`/`Background`).
   O número correto passa a ser o desta secção.

### Re-execução após grooming (07-06-2026)

- **Stack:** Python 3.12 · Behave 1.3.3
- **Comandos:**
  - `python -m behave bdd/features/lab13.feature`
  - `python -m behave bdd`

| Suite | Features | Scenarios | Steps | Result |
|---|---|---|---|---|
| `lab13.feature` (isolado) | 1 | 4 | 30 | ✅ 0 failed |
| `bdd/` (completo: lab9 + lab11 + lab13) | 3 | 12 | 94 | ✅ 0 failed |

```
# lab13 isolado
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
30 steps passed, 0 failed, 0 skipped

# suite completo (bdd/)
3 features passed, 0 failed, 0 skipped
12 scenarios passed, 0 failed, 0 skipped
94 steps passed, 0 failed, 0 skipped
```

### Conclusão
Após a correção, o suite BDD corre **em qualquer versão recente do Behave** (deixou de
depender da versão 1.2.6). Os 4 cenários do Lab 13 mantêm-se a passar; a diferença face
ao registo original é apenas a contagem de steps (22 → 30) e a robustez à versão da
ferramenta. Nenhum comportamento de negócio foi alterado.
