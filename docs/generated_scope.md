# Generated Scope — Lab 8

## Selected slice
- **Slice:** A — Intake session → capture answers (NBQ)
- **Short description:** O utilizador inicia uma sessão de intake para um serviço. O motor AI Engine sugere a próxima pergunta mais valiosa (Next-Best-Question) com base no perfil do serviço e nas respostas já dadas. O utilizador responde até o motor sinalizar `done: true`. Todas as respostas são registadas em memória associadas à sessão.

---

## Actors / roles
- **Primary actor:** G2 Interface
- **Secondary actor:** Transition Manager (utilizador humano que valida o processo)

---

## Use Cases implemented
- **UC-01:** Sugerir próxima pergunta (NBQ)

---

## Requirements implemented (max 10)
- **REQ-001** — NBQ Service: retornar a próxima pergunta mais informativa com base no perfil e respostas atuais
- **REQ-009** — Input Validation & Normalization: validar e normalizar tipos, enums e datas em formato UTC
- **NFR-001** — Performance: p95 ≤ 500ms para `/nbq/next`
- **NFR-005** — Logs Estruturados: logs em JSON com `requestId`, `latencyMs` e `status`

---

## Variant constraints implemented (min. 2)
- **Constraint 1 (REQ-007 / Variante 3):** Cada resposta da API inclui obrigatoriamente o campo `policyVersion`, referenciando a versão ativa da política de pesos NBQ.
- **Constraint 2 (REQ-010 / Variante 3):** Cada pedido gera e persiste (em memória) um `inputsHash` (SHA-256 sobre o payload de features efetivas), garantindo o determinismo — o mesmo payload com a mesma `policyVersion` produz sempre o mesmo resultado.

---

## Out of scope (explicit)
- Cálculo do Continuity Score (REQ-002) — será implementado noutra slice
- Change Risk Assessment (REQ-003)
- Sizing Estimate (REQ-004)
- Explain Endpoint (REQ-006)
- Persistência em base de dados (apenas in-memory/JSON local)
- Interface de utilizador (UI/frontend)
- Autenticação e autorização
- Rate limiting (NFR-004)