# Requirements Engineering Matrix (REM) v1 — Lab 4

### REQ-001: NBQ Service (Next-Best-Question)
- **Stakeholder:** Transition Manager
- **Description:** Retornar a pergunta mais informativa com base no perfil, setor e respostas atuais.
- **Objective:** Minimizar o tempo de intake eliminando perguntas irrelevantes.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-1 + CSF-1
- **Preconditions:** Sessão de intake iniciada no Grupo 1; payload de perfil (`sector`, `solution`) disponível.
- **Postconditions:** Pergunta selecionada é marcada como "apresentada" na sessão; resposta é normalizada para scoring futuro.
- **Acceptance Criteria:**
  * Responder `200 OK` com `{ id, text, weight, why }`.
  * Se não houver mais perguntas, retornar `done: true`.
- **Validation Method:** Teste de API automático validando a presença de campos obrigatórios.
- **Variant Impact:** No

### REQ-002: Continuity Score Calculation
- **Stakeholder:** Transition Lead
- **Description:** Computar prontidão operacional (0-100) baseada em observabilidade, DR e acessos.
- **Objective:** Quantificar o risco de transição do serviço.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-1 + CSF-1
- **Preconditions:** Existência de respostas normalizadas exportadas pelo Grupo 1.
- **Postconditions:** Score gerado e associado a um `ScoringRun` persistido.
- **Acceptance Criteria:**
  * O score deve refletir penalizações por falta de evidências de DR (constraints).
  * Incluir a `policyVersion` na resposta.
- **Validation Method:** Comparação de resultados contra Golden Files de teste.
- **Variant Impact:** No

### REQ-003: Change Risk Assessment
- **Stakeholder:** Release Manager
- **Description:** Avaliar o risco de mudanças planeadas usando histórico de KPIs e payloads de mudança.
- **Objective:** Prever e mitigar falhas em mudanças de infraestrutura ou código.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-1 + CSF-2
- **Preconditions:** Dados históricos de incidentes e mudanças (Grupo 1) acessíveis via API.
- **Postconditions:** Recomendação de mitigação (guardrails) incluída se o risco exceder o threshold.
- **Acceptance Criteria:**
  * Retornar `risk0to100` e lista de `drivers`.
  * Identificar guardrails específicos como `REQUIRE_ROLLBACK`.
- **Validation Method:** Teste de integração com inputs de mudanças críticas conhecidas.
- **Variant Impact:** No

### REQ-004: Sizing Estimate FTE Bands
- **Stakeholder:** Service Manager
- **Description:** Estimar esforço de suporte (P10/P50/P90) a partir de volumetria e SLAs.
- **Objective:** Apoiar o dimensionamento de equipas e definição de preços.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-1 + CSF-1
- **Acceptance Criteria:**
  * Fornecer bandas de confiança realistas e listar pressupostos (assumptions).
  * Latência de cálculo $\le$ 800ms.
- **Validation Method:** Load testing com cenários de alta volumetria de tickets.
- **Variant Impact:** No

### REQ-006: Explain Endpoint (Explicabilidade)
- **Stakeholder:** Client Stakeholder / Auditor
- **Description:** Fornecer explicações humanas para qualquer score, ordenadas por contribuição absoluta.
- **Objective:** Cumprir o requisito de transparência da Variante 3.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-2 + CSF-2
- **Acceptance Criteria:**
  * Drivers devem mapear diretamente para features ou perguntas específicas.
  * Resposta deve incluir a metodologia aplicada.
- **Validation Method:** Inspecção manual de payloads de explicação para clareza terminológica.
- **Variant Impact:** **Yes**

### REQ-007: Policy Versioning & Registry
- **Stakeholder:** Architect / Auditor
- **Description:** Versionar políticas; expor a versão ativa e o histórico de alterações (changelog).
- **Objective:** Garantir que a lógica de negócio é imutável e auditável.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-3 + CSF-3
- **Acceptance Criteria:**
  * Cada nova política gera um snapshot imutável com checksum.
  * Respostas de scoring devem obrigatoriamente referenciar a versão ativa.
- **Validation Method:** Teste de integridade de checksum entre versões.
- **Variant Impact:** **Yes**

### REQ-010: Determinism & Replay Metadata
- **Stakeholder:** QA Engineer / Auditor
- **Description:** Persistir metadados da execução (`inputsHash`) para permitir reprodutibilidade total.
- **Objective:** Garantir que o motor é fiável e auditável sob a Variante 3.
- **Type:** **FR** | **Priority:** H
- **Objective + CSF:** OBJ-3 + CSF-3
- **Acceptance Criteria:**
  * Armazenar `ScoringRun` com hash do payload de entrada.
  * Resultados idênticos devem ser obtidos em replays do mesmo hash.
- **Validation Method:** Teste de Golden Records comparando saídas de execuções repetidas.
- **Variant Impact:** **Yes**

### NFR-001: Performance de Resposta Analítica
- **Stakeholder:** End User
- **Description:** O motor deve garantir tempos de resposta rápidos para não bloquear o utilizador.
- **Objective:** Manter a fluidez da interação Conversational Intake.
- **Type:** **NFR** | **Priority:** M
- **Objective + CSF:** OBJ-1 + CSF-1
- **Acceptance Criteria:**
  * p95 $\le$ 500ms para scoring e NBQ.
  * p95 $\le$ 800ms para sizing estimate.
- **Validation Method:** Testes de stress (Load Testing) a 50 RPS estáveis.
- **Variant Impact:** No