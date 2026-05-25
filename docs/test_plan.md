# Test Plan — Lab 10
## 1) Scope
* **Slice covered:** Continuity Score + Explain (UC-02 + UC-05), Variante 3 (Determinismo e Explicabilidade).
* **Out of scope:** NBQ Service (REQ-001), Change Risk Assessment (REQ-003) e Sizing Estimate (REQ-004).

## 2) Test strategy (static + dynamic)
### Static testing (reviews)
* **What we review:** Requirements cruzados com Acceptance Criteria e Definition of Done.
* **Review checklist:** Ambiguidade de limites (boundaries), tratamento de exceções (falta de dados/adulteração) e clareza nos metadados que afetam o hash.

### Dynamic testing (planned execution)
| Level | What we test | Examples | Evidence |
| ------ | ------ | ------ | ------ |
| Unit | Lógica core e validação matemática | Clamp de valores (TC-006), Checksum SHA-256 único de políticas (TC-010) | planned unit tests (PyTest) |
| Integration | Integração de validação, scoring e replay | Garantia de que inputsHash de metadados diferentes é igual (TC-007) e bloqueio de adulteração (TC-008) | planned integration tests |
| System | Execução end-to-end do slice no AI Engine | Cálculo de score com policy_version e posterior pedido de explain | manual run notes / script logs |
| Acceptance (BDD) | Comportamento vs AC para persona (Transition Manager) | Teste ao determinismo e limite de Top 5 drivers | feature files (bdd/features/lab9.feature) |

## 3) TDD plan (at least 2 candidates)
* **Candidate 1 (rule/REQ):** REQ-010 (Determinism via inputsHash) .
* **Candidate 2 (rule/REQ):** REQ-006 (Top 5 drivers sorting) .
* **Why TDD is suitable:** A lógica matemática do Continuity Score e do cálculo de hash do determinismo têm inputs e outputs precisos. Testar primeiro o cálculo do hash forçará a ignorar metadados não-analíticos (como `application_id`), prevenindo regressões de determinismo .

## 4) BDD plan (what behaviors become scenarios)
* **Feature(s):** Continuity Score and Explainability for Application Intake.
* **Scenarios:** 
  - Happy path — compute score and retrieve top 5 drivers 
  - Negative path — payload missing mandatory fields is rejected 
  - Alternative flow — partial responses trigger uncertainty flag 
  - Determinism — identical features with different metadata produce the same hash 
  - Determinism — tampering with a stored payload blocks the explanation 
* **Links to REQs:** REQ-002, REQ-006, REQ-009, REQ-010 

## 5) Coverage goals
* **Happy path:** 100% de cobertura do processo de Intake com todos os fatores da `policyVersion` preenchidos 
* **Alternative flows:** Penalização por incerteza (`uncertainty_applied: true`) testada garantidamente .
* **Negative/error tests:** Campos obrigatórios em falta (`MISSING_FIELDS`), sector inválido e exceção crítica de `DeterminismError` da Variante 3.
* **Boundary tests:** Clamp matemático de inputs numéricos a 0.0 (mínimo) e 1.0 (máximo) 

## 6) NFR validation approach
* **NFR-006:** 100% de coincidência de outputs para inputs idênticos .
    * **How we verify:** Através de testes de integração (como o TC-009) que re-executam o fluxo e comparam assertivamente os hashes de saída com os hashes originais guardados .
* **NFR-008:** Cada score devolve obrigatoriamente os top 5 drivers com labels legíveis .
    * **How we verify:** Teste unitário e de BDD (TC-002 e TC-010) à rotina de extração dos labels a partir da política.

## 7) Evidence recording and responsibilities
* **Where results are stored:** Em `docs/unit_test_report.md` e `docs/test_first_log.md`.
* **Who maintains traceability:** Toda a equipa, com revisão do Test/QA Lead da semana.
* **How updates are tracked:** Via commits na branch principal do repositório GitHub.