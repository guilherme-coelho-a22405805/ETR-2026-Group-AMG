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