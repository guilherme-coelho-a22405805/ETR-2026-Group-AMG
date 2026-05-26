# Test-First Log — Lab 11

## Selected scope (max 3 requirements)

* REQ-010 (Variant 3 - Determinism & Replay Metadata)
    * AC used: O `inputsHash` calculado deve ignorar metadados não-analíticos garantindo que payloads com metadados diferentes produzem o mesmo hash final.
* REQ-006 (Variant 3 - Explain Endpoint)
    * AC used: A resposta deve retornar exatamente os 5 drivers ordenados por contribuição absoluta descendente.
* REQ-009 (Input Validation)
    * AC used: Rejeitar pedidos com campos obrigatórios em falta com erro MISSING_FIELDS.

## Tests written first (list)

* **T-01:** Valida se metadados diferentes (ex: `application_id`) alteram o hash calculado. Esperado: Hashes devem ser idênticos (maps to REQ-010 / AC-1).
* **T-02:** Valida rejeição de payload sem o campo `responses`. Esperado: Erro `MISSING_FIELDS` (maps to REQ-009 / AC-1).
* **T-03:** Valida ordenação do endpoint de explicação. Esperado: Retorna apenas 5 drivers e o maior impacto absoluto em primeiro lugar (maps to REQ-006 / AC-1).

## Results

* **Initial run:** (expected failures) 2 falhas. T-01 falhou porque o hash inicial estava a serializar o payload todo; T-03 falhou porque não cortava a lista aos primeiros 5 elementos.
* **After implementation:** (pass/fail summary) 3 Passed / 0 Failed.

## Implementation notes (minimal code to pass)

* **What modules/classes/functions were created:** Ficheiro de testes `tests/test_engine.py` utilizando `pytest`.
* **Key rules implemented:** Refatorização da função `compute_inputs_hash` em `ai_engine/scoring.py` para isolar apenas as features analíticas, garantindo o determinismo exigido pela Variante 3.

## BDD scenario

* **Feature:** bdd/features/lab11.feature
* **Scenario 1:** Determinism — identical features with different metadata produce the same hash.
* **Scenario 2:** Happy path — compute score and retrieve top 5 drivers.
* **Scenario 3:** Negative path — payload missing mandatory fields is rejected.

## AI usage

* **Tool:** Claude
* **Prompt summary:** "Gera os 3 testes unitários PyTest baseados na lógica de determinismo (hash sha-256) e top 5 drivers."
* **What was accepted:** A sintaxe de asserção `pytest.raises` e as fixtures mockadas.
* **What was rejected (feature drift):** Testes focados em UI ou rate limiting, pois fugiam do scope.
* **Why:** Para manter o foco nos requisitos analíticos da Variante 3.

## Lessons learned

* **What requirement/AC was ambiguous?** A definição de "Top 5" (REQ-006) não deixava claro o comportamento caso a política tivesse menos de 5 fatores avaliados na totalidade.
* **What test improved clarity?** O teste T-01 obrigou-nos a clarificar que o `application_id` e `timestamp` são metadados que não podem entrar na função de hash, protegendo a reprodutibilidade.
* **What would you change next?** No Lab 12, vamos adicionar testes para garantir