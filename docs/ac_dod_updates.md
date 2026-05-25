# AC & DoD Updates — Lab 10
## Acceptance Criteria improvements (min. 3)

## Item 1 (Variant-driven)
* **Requirement:** REQ-010
* **Before:** "Given que dois payloads têm *features* idênticas, mas metadados não-analíticos diferentes..."
* **After:** "Given que dois payloads têm o mesmo dicionário de respostas (`responses`), o `inputsHash` calculado deve ignorar metadados não-analíticos (como `application_id` e timestamps), garantindo que ambos produzem o mesmo hash final."
* **Why changed:** O AC original era ambíguo quanto aos campos que eram metadados. Durante o Lab 8, descobrimos que serializar todo o payload quebrava o determinismo da Variante 3. Foi necessário explicitar que o hash é restrito ao dicionário de responses e policy_version .

## Item 2 (Variant-driven)
* **Requirement:** REQ-006
* **Before:** "A resposta deve retornar exatamente os 5 drivers com maior peso absoluto."
* **After:** "A resposta deve retornar os 5 drivers com maior peso absoluto. Se a política aplicável possuir menos de 5 fatores totais, o sistema retorna todos os fatores avaliados ordenados por peso absoluto, sem gerar erro."
* **Why changed:** Durante os testes em código, notou-se o conflito de tentar forçar "exatamente 5" caso a política tivesse apenas 4 fatores, o que daria erro em vez de ser transparente .

## Item 3
* **Requirement:** REQ-002
* **Before:** "A resposta deve incluir obrigatoriamente a `policyVersion` que originou o cálculo."
* **After:** "A resposta deve incluir obrigatoriamente a `policyVersion`"
* **Why changed:** Apenas a versão nominal não seria suficiente para fins de auditoria no caso de reconstrução de base de dados, garantindo assim que a versão associada corresponde à assinatura matemática inalterada .

## DoD updates (min. 2)
1. **Proposed DoD change:**
    * **Before:** Acceptance criteria exist  and are testable/verifiable.
    * **After:** Acceptance criteria exist, are testable/verifiable, and at least one AC covers limites matemáticos (boundary cases).
    * **Why:** Verificámos no Lab 9 (TC-006) a importância de garantir que o input de valores estivesse restrito através de `clamp` numérico a limites de [0.0, 1.0] para não gerar scores > 100.
2. **Proposed DoD change:**
    * **Before:** Validation method is defined (review/demo/test/measurement).
    * **After:** Validation method is defined and está cruzado explicitamente com pelo menos um Caso de Teste (TC-###) ou Cenário BDD aprovado.
    * **Why:** Facilita a geração da matriz de rastreabilidade, e garante que um requisito "Feito" é efetivamente provado de forma automatizada no CI/CD .