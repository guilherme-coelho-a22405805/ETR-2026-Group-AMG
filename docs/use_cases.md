# Use Cases — Lab 5

## UC-01 — Sugerir próxima pergunta (NBQ)
- **Primary actor:** G2 Interface
- **Supporting actors:** N/A
- **Goal:** Fornecer à interface a pergunta que mais reduz a incerteza do processo de intake.
- **Preconditions:** Sessão de intake ativa; perfil do serviço (setor/solução) definido.
- **Trigger:** A interface (G2) envia o estado atual das respostas e solicita a próxima ação.
- **Postconditions (success):** Uma pergunta válida (ou sinal de "done") é retornada com o seu peso e justificação.
- **Postconditions (failure):** Sistema retorna erro de validação se os inputs forem incompatíveis com a política.
- **Related requirements:** REQ-001, REQ-009

### Main flow (happy path)
1. O G2 envia o payload de respostas atuais.
2. O motor valida a `policyVersion` ativa.
3. O sistema calcula o ganho de informação para todas as perguntas aplicáveis.
4. O sistema seleciona a pergunta com maior peso.
5. O sistema retorna o ID da pergunta, o texto e o campo `why` (justificação).

### Alternative flows
A1. **Nenhuma pergunta aplicável:** O sistema deteta que todos os requisitos de informação foram satisfeitos e retorna `{ done: true }`.

### Exceptions / errors
E1. **Policy Version Inválida:** O sistema retorna erro `VALIDATION_ERROR` se a política solicitada não existir no registo.

---

## UC-05 — Consultar explicação de score (Explain)
- **Primary actor:** Transition Manager
- **Supporting actors:** G1 Core (fonte de dados)
- **Goal:** Compreender os fatores (drivers) que determinaram um Continuity Score ou Change Risk.
- **Preconditions:** Um `ScoringRun` foi executado previamente; o utilizador tem acesso ao relatório.
- **Trigger:** O Transition Manager clica em "Ver detalhes/Porquê?" na interface.
- **Postconditions (success):** Sistema apresenta os Top 5 drivers ordenados por contribuição absoluta.
- **Postconditions (failure):** Mensagem de erro se o ID da execução não for encontrado.
- **Related requirements:** REQ-003, REQ-006, NFR-008

### Main flow (happy path)
1. O Transition Manager solicita a explicação de um score específico.
2. O sistema recupera os metadados e inputs do `ScoringRun`.
3. O sistema identifica os 5 fatores (respostas ou KPIs) com maior impacto (positivo ou negativo).
4. O sistema gera labels legíveis (human-readable) para cada driver.
5. O sistema apresenta o breakdown detalhado e a metodologia utilizada.

### Alternative flows
A1. **Menos de 5 drivers disponíveis:** O sistema apresenta todos os fatores disponíveis sem preencher com dados fictícios.

### Exceptions / errors
E1. **Dados de Origem Inacessíveis:** Se o link para a evidência original no G1 estiver quebrado, o sistema sinaliza o driver mas alerta para a falha na rastreabilidade.