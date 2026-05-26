# Unit Test Report — Lab 12

## Selected scope (max 3 requirements)

**REQ-010 (Determinism & Replay)**
    *  AC automated: Payloads com features idênticas mas metadados diferentes produzem o mesmo `inputsHash`. Bloqueia o replay em caso de hash alterado.
**REQ-006 (Explain Endpoint - Variant 3)**
    *  AC automated: A resposta deve listar os "Top 5" drivers ordenados por contribuição absoluta descendente.
**REQ-009 (Input Validation)**
    *  AC automated: Rejeitar pedidos com campos obrigatórios em falta (`MISSING_FIELDS`) ou enumerações inválidas (`INVALID_SECTOR`). Limites de valores (`clamp`) garantidos.

## Tests implemented (minimum 8)

| Test ID | Test name (Function) | REQ | AC | Type | Notes |
| ------ | ------ | ------ | ------ | ------ | ------ |
| UT-01 | `test_determinism_ignores_metadata` | REQ-010 | Hash consistency | Happy | Derivado do TC-007. Já implementado. |
| UT-02 | `test_missing_mandatory_fields_rejected` | REQ-009 | Missing fields E1 | Negative | Derivado do TC-004 . Já implementado. |
| UT-03 | `test_explain_returns_top_5_ordered` | REQ-006 | Top 5 sorting | Happy | Derivado do TC-002 . Já implementado. |
| UT-04 | `test_invalid_sector_rejected` | REQ-009 | Invalid enum | Negative | Derivado do TC-005. Rejeita setor fora da lista válida. |
| UT-05 | `test_boundary_clamp_min_max` | REQ-009 | Boundaries | Boundary | Derivado do TC-006. Força inputs a limites [0.0, 1.0]. |
| UT-06 | `test_explain_blocks_tampered_payload` | REQ-010 | Hash tampering | Negative | Derivado do TC-008. Levanta `DeterminismError` na adulteração. |
| UT-07 | `test_policy_checksum_uniqueness` | REQ-007 | SHA-256 stability | Happy | Derivado do TC-010. Garante imutabilidade matemática da política. |
| UT-08 | `test_missing_optional_trigger_uncertainty` | REQ-002 | Partial payload | Alt | Derivado do TC-003. Fatores opcionais ausentes ativam `uncertainty_applied. |

## Coverage checklist

Happy path tests: 3 (UT-01, UT-03, UT-07)
Negative/error tests: 3 (UT-02, UT-04, UT-06)
Boundary tests: 1 (UT-05)
Alternative flow tests: 1 (UT-08)

## Execution evidence

Date: 26-05-2026
Command used: `python -m pytest tests/test_engine.py`
Result summary:
  Tests run: 8
  Passed: 8
  Failed: 0
Notes: Todos os testes passaram, incluindo as validações rigorosas de determinismo e Top 5 associadas à variante 3