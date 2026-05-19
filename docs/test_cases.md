# Test Cases — Lab 9

**Slice:** Continuity Score + Explain (UC-02 + UC-05)
**Variant:** Group 3 — Determinism + Explainability

---

## TC-001 — Calcular Continuity Score com payload completo

- **Type:** Functional
- **Priority:** H
- **Related requirements:** REQ-002, REQ-009
- **Coverage:** Happy path
- **Preconditions:**
  - Storage local inicializado e acessível em `data/scoring_runs.json`.
- **Test data:**
  
  ```json
  {
    "application_id": "APP-TC001",
    "sector": "healthcare",
    "responses": {
      "documentation_completeness": 0.8,
      "monitoring_coverage": 0.6,
      "dr_bcp_readiness": 0.7,
      "access_management": 0.9,
      "integrations_mapped": 0.5,
      "support_model_defined": 0.85
    }
  }
  ```

- **Steps:**
  1. Submeter o payload acima ao motor (`calculate_continuity_score` via UI ou função).
  2. Capturar o resultado (score + metadados).
  3. Verificar que existe um registo persistido com o runId retornado.
- **Expected results:**
  - Resposta inclui `score` do tipo inteiro entre 0 e 100.
  - Resposta inclui o campo `policyVersion: "v1.0.0"`.
  - Resposta inclui `inputsHash` não vazio (string de 64 caracteres hex).
  - `uncertainty_applied = false` (todos os fatores fornecidos).
  - Registo guardado em `scoring_runs.json` com o mesmo runId.

---

## TC-002 — Explicar score com Top 5 drivers ordenados (Variant)

- **Type:** Functional
- **Priority:** H
- **Related requirements:** REQ-006, NFR-008
- **Coverage:** Happy path + Variant
- **Preconditions:**
  - Existe um `ScoringRun` persistido com 6 drivers no breakdown (resultado de TC-001).
- **Test data:**
  - `runId` válido obtido em TC-001.
- **Steps:**
  1. Invocar o endpoint Explain (`explain_score(stored_run, limit=5)`).
  2. Inspecionar a lista `drivers` retornada.
- **Expected results:**
  - Retorna **exatamente 5** elementos na lista `drivers`.
  - A lista está ordenada **por contribuição absoluta descendente** (`abs(drivers[i].contribution) >= abs(drivers[i+1].contribution)`).
  - Cada driver tem `label` legível em português (vindo dos labels da policy ativa).
  - Resposta inclui `methodology` (string descritiva) e `integrity.deterministic = true`.

---

## TC-003 — Calcular score com campos opcionais em falta

- **Type:** System
- **Priority:** M
- **Related requirements:** REQ-002, REQ-009
- **Coverage:** Alternative flow (UC-02 A1)
- **Preconditions:**
  - Política `v1.0.0` ativa.
- **Test data:**

  ```json
  {
    "application_id": "APP-TC003",
    "sector": "bfsi",
    "responses": {
      "documentation_completeness": 0.9,
      "monitoring_coverage": 0.8
    }
  }
  ```

- **Steps:**
  1. Submeter o payload com apenas 2 dos 6 fatores preenchidos.
  2. Capturar o resultado.
- **Expected results:**
  - O cálculo **completa-se com sucesso** (não rejeita).
  - `uncertainty_applied = true`.
  - `missingOptionalFields` contém os 4 fatores em falta.
  - Score gerado é inferior ao de TC-001 (penalização por incerteza — fatores em falta contam como 0).

---

## TC-004 — Erro de validação: campos obrigatórios em falta (E1)

- **Type:** Unit
- **Priority:** H
- **Related requirements:** REQ-009
- **Coverage:** Negative / error (UC-02 E1)
- **Preconditions:** Nenhuma.
- **Test data:**
  
  ```json
  { "sector": "retail" }
  ```

- **Steps:**
  1. Invocar `validate_and_normalize` com o payload acima (sem `application_id` nem `responses`).
- **Expected results:**
  - Levanta `ValidationError`.
  - `error.code == "MISSING_FIELDS"`.
  - `error.fields` contém `"application_id"` e `"responses"`.
  - Nenhuma execução é persistida.

---

## TC-005 — Erro de validação: sector inválido

- **Type:** Unit
- **Priority:** H
- **Related requirements:** REQ-009
- **Coverage:** Negative / error
- **Preconditions:** Nenhuma.
- **Test data:**
  
  ```json
  {
    "application_id": "APP-TC005",
    "sector": "manufacturing",
    "responses": { "documentation_completeness": 0.5 }
  }
  ```

- **Steps:**
  1. Invocar `validate_and_normalize` com sector fora do enum permitido.
- **Expected results:**
  - Levanta `ValidationError`.
  - `error.code == "INVALID_SECTOR"`.
  - `error.fields == ["sector"]`.
  - Mensagem indica os sectores válidos (`healthcare`, `bfsi`, `retail`, `other`).

---

## TC-006 — Boundary: valores extremos 0.0 e 1.0 em todos os fatores

- **Type:** Integration
- **Priority:** M
- **Related requirements:** REQ-002, REQ-009
- **Coverage:** Boundary
- **Preconditions:** Política `v1.0.0` ativa.
- **Test data:**
  - **Payload A (mínimo):** todos os 6 fatores = `0.0`
  - **Payload B (máximo):** todos os 6 fatores = `1.0`
  - **Payload C (clamp):** um fator com `1.5` (acima do limite) e outro com `-0.2` (abaixo).
- **Steps:**
  1. Calcular score para Payload A.
  2. Calcular score para Payload B.
  3. Calcular score para Payload C.
- **Expected results:**
  - **Payload A:** `score == 0`.
  - **Payload B:** `score == 100`.
  - **Payload C:** validator faz clamp para `[0.0, 1.0]` antes do cálculo; score válido entre 0 e 100; nenhum erro levantado.

---

## TC-007 — Determinismo: payloads com mesmas features e metadados diferentes (Variant)

- **Type:** Integration
- **Priority:** H
- **Related requirements:** REQ-010, NFR-006
- **Coverage:** Alternative flow + Variant (REQ-010 AC)
- **Preconditions:** Política `v1.0.0` ativa.
- **Test data:**
  - **Payload X:** `application_id="APP-X"`, sector=`healthcare`, responses idênticas a TC-001.
  - **Payload Y:** `application_id="APP-Y"` (METADADO DIFERENTE), sector=`healthcare`, responses idênticas a TC-001.
- **Steps:**
  1. Calcular score para Payload X → guardar `inputsHash_X` e `score_X`.
  2. Calcular score para Payload Y → guardar `inputsHash_Y` e `score_Y`.
  3. Comparar hashes e scores.
- **Expected results:**
  - `inputsHash_X == inputsHash_Y` (metadados não-analíticos NÃO afetam o hash).
  - `score_X == score_Y`.
  - Ambos os registos foram persistidos com `runId` diferentes (cada execução é única) mas o mesmo `inputsHash`.

---

## TC-008 — Explain bloqueia quando payload foi adulterado (UC-05 E1, Variant)

- **Type:** Integration
- **Priority:** H
- **Related requirements:** REQ-010, REQ-006
- **Coverage:** Negative / error (UC-05 E1)
- **Preconditions:**
  - Existe um `ScoringRun` persistido (output de TC-001).
- **Test data:**
  - Clone do `ScoringRun` de TC-001 onde se altera manualmente `responses.documentation_completeness` de `0.8` para `0.99` **sem** recalcular o `inputsHash`.
- **Steps:**
  1. Carregar o registo original.
  2. Adulterar o `responses` no clone.
  3. Invocar `explain_score(tampered_run)`.
- **Expected results:**
  - Levanta `DeterminismError`.
  - `error.original_hash` ≠ `error.replay_hash`.
  - Nenhuma explicação é retornada (a chamada bloqueia antes de calcular drivers).

---

## TC-009 — Determinismo perfeito em re-execução (NFR-006)

- **Type:** Acceptance
- **Priority:** H
- **Related requirements:** NFR-006, REQ-010
- **Coverage:** Variant + NFR verification
- **Preconditions:** Política `v1.0.0` ativa.
- **Test data:**
  - Mesmo payload de TC-001.
- **Steps:**
  1. Executar `calculate_continuity_score` com o payload → `result_1`.
  2. Executar **novamente** `calculate_continuity_score` com o **mesmo payload** → `result_2`.
  3. Comparar `score`, `inputsHash`, `breakdown` e `policyVersion`.
- **Expected results:**
  - `result_1.score == result_2.score` (100% coincidência exigida pelo NFR-006).
  - `result_1.inputsHash == result_2.inputsHash`.
  - `result_1.breakdown == result_2.breakdown` (mesmas contribuições por fator).
  - Apenas o `runId` e `computedAt` diferem (são metadados, não output analítico).

---

## TC-010 — Policy Registry: imutabilidade e checksum único (Variant)

- **Type:** Unit
- **Priority:** M
- **Related requirements:** REQ-007, NFR-008
- **Coverage:** Variant + NFR verification (labels)
- **Preconditions:** Módulo `policy.py` carregado.
- **Test data:** Versões `v1.0.0` (active) e `v0.9.0` (deprecated) definidas no registo.
- **Steps:**
  1. Chamar `list_policies()`.
  2. Capturar o checksum SHA-256 de `v1.0.0`.
  3. Chamar `policy_checksum("v1.0.0")` novamente.
  4. Tentar obter uma versão inexistente: `get_policy("v9.9.9")`.
  5. Verificar que `v1.0.0` tem labels legíveis para todos os fatores.
- **Expected results:**
  - `list_policies()` devolve **ambas** as versões (a deprecated **não foi apagada** — REQ-007 AC-1).
  - Checksum de `v1.0.0` é uma string SHA-256 de 64 caracteres hex.
  - Chamar `policy_checksum("v1.0.0")` duas vezes devolve **exatamente o mesmo valor** (REQ-007 AC-2).
  - `get_policy("v9.9.9")` levanta `ValueError`.
  - Todos os 6 fatores têm `label` não vazio em português (suporta NFR-008).

