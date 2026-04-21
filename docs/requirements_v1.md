# Requirements v1 — Lab 3 (AI Engine)

## Functional Requirements (FR)

| ID | Epic | Requirement | Priority | Variant Impact |
|:--- |:--- |:--- |:--- |:--- |
| **REQ-001** | EPIC-1 | **NBQ Service**: Retornar a próxima pergunta mais informativa baseada no perfil e respostas atuais. | H | No |
| **REQ-002** | EPIC-2 | **Continuity Score**: Calcular a prontidão operacional (0-100) com breakdown de fatores. | H | No |
| **REQ-003** | EPIC-2 | **Change Risk**: Avaliar o risco de mudanças planeadas com drivers e guardrails. | H | No |
| **REQ-004** | EPIC-3 | **Sizing Estimate**: Estimar esforço em bandas P10/P50/P90 com pressupostos de impacto. | H | No |
| **REQ-005** | EPIC-2 | **90-day Recommendations**: Gerar ações prioritárias com prefill hints para o Grupo 2. | M | No |
| **REQ-006** | EPIC-2 | **Explain Endpoint**: [Variante] Fornecer explicações humanas para scores, ordenadas por contribuição. | H | **Yes** |
| **REQ-007** | EPIC-4 | **Policy Versioning**: Versionar políticas e garantir que cada resposta inclui a `policyVersion`. | H | **Yes** |
| **REQ-008** | EPIC-4 | **Feature Catalog**: Publicar o catálogo de features com mapeamento para o Grupo 1. | M | No |
| **REQ-009** | EPIC-1 | **Input Validation**: Validar e normalizar tipos, enums e datas em formato UTC. | H | No |
| **REQ-010** | EPIC-4 | **Determinism & Replay**: [Variante] Persistir `inputsHash` para garantir reprodutibilidade total. | H | **Yes** |

## Detailed Requirements (Top 6)

### REQ-001: NBQ Service (Next-Best-Question)
* **Description**: Retornar a próxima pergunta condicionada ao setor, solução e respostas atuais.
* **Objective**: Maximizar o ganho de informação por interação.
* **Acceptance Criteria**:
    * Retornar `200 OK` com `{ id, text, fields[], weight, why }`.
    * Retornar `{ done: true }` quando não houver mais perguntas aplicáveis.
* **Variant Impact**: No

### REQ-003: Change Risk Assessment
* **Description**: Avaliar o risco de uma mudança usando o payload da mudança e histórico de KPIs.
* **Objective**: Prevenir falhas em produção através de mitigação antecipada.
* **Acceptance Criteria**:
    * Se o risco exceder o threshold, incluir guardrails (ex: `ADD_CANARY`).
    * O resultado deve ser determinístico por versão de política.
* **Variant Impact**: No

### REQ-006: Explain Endpoint (Variante 3)
* **Description**: Fornecer explicações legíveis para qualquer score gerado.
* **Objective**: Garantir a transparência (explicabilidade) exigida pela Variante 3.
* **Acceptance Criteria**:
    * Listar drivers ordenados por contribuição absoluta.
    * Mapear drivers diretamente para as features ou perguntas de origem.
* **Variant Impact**: **Yes**

### REQ-007: Policy Versioning & Registry (Variante 3)
* **Description**: Gerir versões imutáveis de políticas de scoring e NBQ.
* **Objective**: Permitir auditoria e garantir que o comportamento do motor é previsível.
* **Acceptance Criteria**:
    * Toda a resposta da API deve incluir o campo `policyVersion`.
    * `GET /policy/version` deve listar o histórico completo com checksums.
* **Variant Impact**: **Yes**

### REQ-009: Input Validation & Normalization
* **Description**: Validar esquemas e normalizar dados recebidos dos Grupos 1 e 2.
* **Objective**: Garantir a integridade dos dados antes do processamento analítico.
* **Acceptance Criteria**:
    * Rejeitar pedidos com campos obrigatórios em falta com erro `MISSING_FIELDS`.
    * Normalizar datas para UTC e canonicalizar booleanos e enums.
* **Variant Impact**: No

### REQ-010: Determinism & Replay (Variante 3)
* **Description**: Garantir que o motor produz resultados idênticos para os mesmos inputs e política.
* **Objective**: Cumprir o requisito de reprodutibilidade da Variante 3.
* **Acceptance Criteria**:
    * Persistir um `ScoringRun` com o `inputsHash` de cada pedido.
    * Em caso de replay com o mesmo hash e versão, o output deve ser validado por comparação de hash.
* **Variant Impact**: **Yes**

## Non-Functional Requirements (NFR)

| ID | Type | Requirement | Measurable Metric | Variant? |
|:--- |:--- |:--- |:--- |:--- |
| **NFR-001** | Performance | Latência para Scoring/NBQ. | p95 $\le$ 500ms para `/nbq/next` e `/continuity-score`. | No |
| **NFR-002** | Performance | Latência para Sizing. | p95 $\le$ 800ms para `/sizing/estimate`. | No |
| **NFR-003** | Availability | Disponibilidade. | 99.9% de uptime mensal com endpoints de `/health` e `/ready`. | No |
| **NFR-004** | Security | Rate Limiting. | 5 RPS por utilizador com burst de 10 pedidos. | No |
| **NFR-005** | Observability | Logs Estruturados. | Logs em formato JSON incluindo `requestId`, `latencyMs` e `status`. | No |
| **NFR-006** | **[Variante]** | Determinismo. | 100% de coincidência de outputs para inputs idênticos e mesma versão. | **Yes** |
| **NFR-007** | Quality | Cobertura de Testes. | Mínimo de 70% de cobertura em módulos core de lógica. | No |
| **NFR-008** | **[Variante]** | Explicabilidade. | Cada score deve devolver obrigatoriamente os top 5 drivers com labels legíveis. | **Yes** |