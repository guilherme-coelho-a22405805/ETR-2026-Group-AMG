# Traceability — Use Cases ↔ Requirements (Lab 6)

## Mapping (UC → REQ)
| Use Case | Linked Requirements (REQ-###) | Notes |
|---|---|---|
| UC-01 | REQ-001, REQ-009 | NBQ depende da validação de input correta. |
| UC-02 | REQ-002, REQ-009 | O cálculo exige dados normalizados. |
| UC-03 | REQ-003, REQ-009 | Avaliação de risco usa KPIs históricos do G1. |
| UC-04 | REQ-004, REQ-009 | Sizing exige volumetria válida. |
| UC-05 | REQ-006, REQ-007 | Explicabilidade ligada ao versionamento de políticas. |
| UC-06 | REQ-010, REQ-007 | Replay exige hash check e políticas imutáveis. |

## Gaps / Observations
- **Missing requirement candidate:** "O sistema deve permitir comparar dois ScoringRuns da mesma aplicação para detetar evolução de maturidade." (Revelado pela necessidade de fluxos alternativos de re-calculo).
- **Cobertura:** Todos os 10 requisitos funcionais estão mapeados em pelo menos um caso de uso.