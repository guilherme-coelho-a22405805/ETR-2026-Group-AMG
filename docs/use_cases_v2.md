# Use Cases v2 — Lab 6

## UC-02 — Calcular Continuity Score
- **Primary actor:** G2 Assistant
- **Supporting actors:** Core System (G1)
- **Goal:** Obter um índice de prontidão (0-100) baseado em dados normalizados.
- **Preconditions:** Payload de respostas do intake disponível; Política de scoring ativa.
- **Trigger:** O G2 solicita o score via `POST /continuity-score`.
- **Postconditions (success):** Score devolvido com breakdown e `policyVersion`.
- **Postconditions (failure):** Sistema reporta erro de validação ou timeout.
- **Related requirements:** REQ-002, REQ-009

### Main flow (happy path)
1. O G2 envia o payload de respostas.
2. O Sistema valida o esquema do input (Normalização).
3. O Sistema aplica os pesos da `policyVersion` ativa.
4. O Sistema gera o breakdown de contribuições.
5. O Sistema retorna o score final e metadados.

### Alternative flows (min. 2)
A1. **Dados em falta:** Se campos não-obrigatórios faltarem, o sistema calcula o score com penalização por incerteza.
A2. **Re-calculo de sessão:** Se o ID da aplicação já tiver um score, o sistema atualiza o `ScoringRun` existente.

### Exceptions / errors (min. 2)
E1. **Erro de Validação (RE-G3-9):** Se faltarem campos obrigatórios, o sistema retorna `MISSING_FIELDS`.
E2. **Timeout do Core:** Se a ligação ao G1 falhar (> 3s), o sistema retorna erro de dependência.

---

## UC-05 — Consultar explicação de score (Explain)
- **Primary actor:** Transition Lead
- **Supporting actors:** N/A
- **Goal:** Visualizar a metodologia e os drivers que justificam o score.
- **Preconditions:** Existência de um `runId` válido e persistido.
- **Trigger:** O utilizador solicita a explicação detalhada.
- **Postconditions (success):** Exposição dos Top 5 drivers com labels legíveis.
- **Postconditions (failure):** Erro de "Execução não encontrada".
- **Related requirements:** REQ-006, REQ-010

### Main flow (happy path)
1. O Ator fornece o ID da execução.
2. O Sistema recupera o snapshot da política usada no momento do cálculo.
3. O Sistema identifica os 5 fatores de maior impacto absoluto.
4. O Sistema retorna a lista ordenada de drivers e a metodologia.

### Alternative flows (min. 2)
A1. **Exportação de Relatório:** O utilizador solicita o envio da explicação para formato PDF (via G2).
A2. **Visualização de Pesos Raw:** O utilizador (admin) solicita ver os pesos brutos por trás dos drivers.

### Exceptions / errors (min. 2)
E1. **Falha de Determinismo (Variante 3):** Se o `inputsHash` atual não coincidir com o original no replay, o sistema bloqueia a explicação e gera um alerta de auditoria.
E2. **Versão de Política Obsoleta:** Se a política original tiver sido arquivada sem snapshot, o sistema avisa que a explicação é limitada.

## Variant-driven notes
- O fluxo de exceção **E1 no UC-05** reflete diretamente a nossa **Variante 3**, garantindo que nenhum score é explicado se a integridade dos dados (Determinismo/Hash) estiver comprometida.