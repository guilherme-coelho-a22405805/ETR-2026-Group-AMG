# Acceptance Criteria — Lab 7

## REQ-001 — NBQ Service
- **AC-1:** Se o payload contiver um `sector` válido e existirem perguntas por responder, o sistema retorna `200 OK` e o ID da próxima pergunta.
- **AC-2:** Se todas as perguntas aplicáveis ao perfil já tiverem resposta, o sistema retorna `{ done: true }`.
- **AC-3:** Se o `sector` enviado não for reconhecido, o sistema rejeita o pedido com `400 Bad Request`.

## REQ-002 — Continuity Score Calculation
- **AC-1:** O score gerado deve ser um inteiro entre 0 e 100.
- **AC-2:** A resposta deve incluir obrigatoriamente a `policyVersion` que originou o cálculo.
- **AC-3:** Se faltarem campos não-obrigatórios, o cálculo processa-se mas adiciona uma flag `uncertainty_applied: true`.

## REQ-006 — Explain Endpoint (Given/When/Then)
**[Variant Impact: Yes]**
- **Given** que o utilizador autenticado solicita a explicação do score com o runID "X"
- **And** esse runID tem 10 drivers de impacto registados
- **When** o pedido for processado sem o query parameter "limit"
- **Then** a resposta deve retornar exatamente os 5 drivers com maior peso absoluto.
- **And** os drivers devem estar ordenados do maior para o menor impacto.

## REQ-007 — Policy Versioning & Registry
**[Variant Impact: Yes]**
- **AC-1:** Uma política guardada não pode ser apagada do registo (apenas marcada como inativa).
- **AC-2:** A criação de uma nova versão de política gera um checksum único `SHA-256`.
- **AC-3:** Se a versão de política requisitada for inativa, o sistema retorna a versão, mas com o aviso `DEPRECATED`.

## REQ-010 — Determinism & Replay Metadata (Given/When/Then)
**[Variant Impact: Yes]**
- **Given** que dois payloads são enviados para `/continuity-score`
- **And** os payloads têm *features* idênticas, mas metadados não-analíticos diferentes
- **When** o motor processar ambos os pedidos com a mesma `policyVersion`
- **Then** o sistema deve gerar exatamente o mesmo `inputsHash` para os dois payloads.
- **And** o score retornado deve ser matematicamente idêntico.

## NFR-001 — Performance de Resposta Analítica
- **AC-1:** Sob uma carga estabilizada de 50 pedidos por segundo, o p95 do Server Response Time não pode ultrapassar 500ms.
- **AC-2:** Sob carga normal, o sistema não pode retornar timeouts internos superiores a 1% dos pedidos.