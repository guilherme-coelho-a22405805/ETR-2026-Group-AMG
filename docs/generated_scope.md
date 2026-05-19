# Generated Scope — Lab 8

## Selected slice

- **Slice:** Combinação de **B (Evidence/Validation)** + **D (Export/Results)** adaptada ao nosso domínio AI Engine.
- **Nome interno:** *Continuity Score + Explain* (UC-02 → UC-05).
- **Descrição curta:**
  O Transition Manager submete um payload de intake com fatores de prontidão
  operacional. O motor valida e normaliza os inputs, calcula um Continuity Score
  (0–100) baseado na política ativa, persiste a execução com `inputsHash` para
  garantir determinismo, e permite consultar a explicação detalhada do score
  com os **Top 5 drivers** que mais contribuíram. A explicação só é fornecida
  se o check de integridade (replay do hash) passar — refletindo diretamente
  as constraints da Variante 3.

## Actors / roles

- **Primary actor:** Transition Manager (persona da Variante 3)
- **Secondary actor:** G2 Assistant (representado pela própria UI desktop neste protótipo)

## Use Cases implemented

- **UC-02 — Calcular Continuity Score**
  - Main flow (steps 1–5) totalmente implementado
  - Alternative flow A1 (campos opcionais em falta → `uncertainty_applied: true`)
  - Exception E1 (`MISSING_FIELDS`) implementada via `ValidationError`

- **UC-05 — Consultar explicação de score**
  - Main flow (steps 1–4) totalmente implementado
  - Exception E1 (Falha de Determinismo — Variante 3) implementada via `DeterminismError`
  - Aviso de política DEPRECATED (REQ-007 AC-3) implementado no resultado

## Requirements implemented (≤ 10)

| ID | Descrição (curta) | Onde está implementado |
|---|---|---|
| **REQ-002** | Continuity Score 0-100 com breakdown e `policyVersion` | `ai_engine/scoring.py::calculate_continuity_score` |
| **REQ-006** | Explain endpoint com Top 5 drivers (Variant) | `ai_engine/explain.py::explain_score` |
| **REQ-007** | Policy versioning com checksum SHA-256 (Variant) | `ai_engine/policy.py` (registry imutável) |
| **REQ-009** | Input validation + normalização (UTC, enums) | `ai_engine/validator.py::validate_and_normalize` |
| **REQ-010** | Determinism via `inputsHash` (Variant) | `ai_engine/scoring.py::compute_inputs_hash` + `replay_score` |
| **NFR-006** | 100% coincidência de outputs para inputs idênticos (Variant) | Verificado em `smoke_test.py` (determinism check) |
| **NFR-008** | Top 5 drivers com labels legíveis obrigatórios (Variant) | `ai_engine/explain.py` (limit=5 + labels da policy) |

Total: **7 requisitos** (dentro do limite de 10).

## Variant constraints implemented (≥ 2 obrigatórias)

1. **Determinismo algorítmico (REQ-010 + NFR-006):** O `inputsHash` é calculado
   apenas sobre as features analíticas (não os metadados como `application_id`
   ou `timestamp`), garantindo que dois payloads com features idênticas mas
   metadados diferentes produzem o mesmo hash e o mesmo score. O smoke test
   valida explicitamente este AC do REQ-010.

2. **Explicabilidade obrigatória (REQ-006 + NFR-008):** Cada explicação devolve
   **exatamente Top 5 drivers** (limit=5 por defeito) ordenados por contribuição
   absoluta descendente, com `label` legível para o Transition Manager
   (proveniente do snapshot da política).

3. **Integrity check no Explain (UC-05 E1):** A explicação só é entregue se o
   replay do cálculo produzir o mesmo `inputsHash` da execução original. Se for
   detetada adulteração, é lançado `DeterminismError` e a explicação é bloqueada
   — exatamente como descrito na exceção E1 do UC-05.

4. **Policy immutability + DEPRECATED warning (REQ-007):** O registo de
   políticas não permite delete (apenas marcar `inactive`/`deprecated`), e cada
   versão tem checksum SHA-256 único e estável.

## Out of scope (explicit)

- **NBQ Service (REQ-001), Change Risk (REQ-003), Sizing (REQ-004), 90-day
  Recommendations (REQ-005), Feature Catalog (REQ-008):** fora do slice escolhido.
- **Testes automatizados (PyTest):** serão criados no Lab 11 (test-first).
- **Endpoints REST reais:** este protótipo é desktop. As assinaturas dos métodos
  espelham os endpoints (`/continuity-score`, `/explain`) para permitir migração
  futura sem reescrever o motor.
- **Rate limiting (NFR-004) e logs estruturados (NFR-005):** fora do scope mínimo
  do Lab 8.
- **Autenticação / RBAC:** o protótipo assume um único utilizador local.
- **Performance benchmarks (NFR-001/NFR-002):** não mensurados neste lab.

## Traceability map (UC → REQ → ficheiro)

| UC step | REQ coberto | Ficheiro / função |
|---|---|---|
| UC-02 step 2 (validar schema) | REQ-009 | `validator.py::validate_and_normalize` |
| UC-02 step 3 (aplicar pesos) | REQ-002 | `scoring.py::calculate_continuity_score` |
| UC-02 step 4 (breakdown) | REQ-002 | breakdown computed in `calculate_continuity_score` |
| UC-02 step 5 (retornar + metadata) | REQ-002, REQ-007, REQ-010 | mesmo método (campo `policyVersion`, `inputsHash`) |
| UC-02 A1 (uncertainty) | REQ-002 AC-3 | `validator.py` retorna `uncertainty_applied` |
| UC-02 E1 (MISSING_FIELDS) | REQ-009 | `validator.py::ValidationError` |
| UC-05 step 2 (snapshot da policy) | REQ-007 | `policy.py::get_policy` |
| UC-05 step 3 (Top 5 drivers) | REQ-006, NFR-008 | `explain.py::explain_score` |
| UC-05 E1 (Falha determinismo) | REQ-010, NFR-006 | `explain.py::DeterminismError` |
