# Requirements v1 — Lab 3 (AI Engine)

## Functional Requirements (FR)

| ID | Epic | Requirement | Priority | Variant Impact |
|:--- |:--- |:--- |:--- |:--- |
| **REQ-001** | EPIC-1 | O sistema deve gerar a próxima pergunta (NBQ) para reduzir a incerteza do intake. | H | No |
| **REQ-002** | EPIC-2 | O motor deve calcular o Continuity Score (0-100) com base nos dados de infraestrutura. | H | No |
| **REQ-003** | EPIC-2 | **[Variante]** O sistema deve fornecer os "Top 5 drivers" que justificam cada score gerado. | H | **Yes** |
| **REQ-004** | EPIC-3 | O motor deve estimar o esforço de equipa em bandas P10, P50 e P90. | H | No |
| **REQ-005** | EPIC-2 | O sistema deve calcular o risco de mudanças (Change Risk) com base no histórico. | M | No |
| **REQ-006** | EPIC-4 | O motor deve validar a "frescura" (freshness) dos links de evidência fornecidos. | M | No |
| **REQ-007** | EPIC-2 | **[Variante]** O sistema deve expor um endpoint para explicar a metodologia de cálculo. | L | **Yes** |

## Detailed Requirements (Top 6)

### REQ-001: Geração de Next-Best-Question (NBQ)
* **Description:** O motor deve analisar o estado atual das respostas e selecionar a pergunta que, estatisticamente, mais contribui para fechar o gap de incerteza do score final.
* **Objective:** Minimizar o tempo do utilizador no processo de intake.
* **Acceptance Criteria:**
    * O endpoint `/nbq/next` deve retornar apenas uma pergunta por pedido.
    * A pergunta retornada deve incluir o peso (weight) e a justificação (why).
* **Variant Impact:** No

### REQ-002: Cálculo de Continuity Score
* **Description:** Processar as respostas normalizadas para gerar um índice de prontidão operacional (0 a 100).
* **Objective:** Fornecer uma métrica clara sobre o risco de assumir o suporte de uma aplicação.
* **Acceptance Criteria:**
    * O cálculo deve considerar as áreas de Observabilidade, DR/BCP, Acessos e Runbooks.
    * O score deve ser atualizado instantaneamente após a submissão de novos dados.
* **Variant Impact:** No

### REQ-003: Explicabilidade via "Top 5 Drivers"
* **Description:** Para cada cálculo de score, o motor deve identificar e listar os 5 fatores (respostas ou falta delas) que mais impactaram o resultado final.
* **Objective:** Garantir que o Transition Manager compreende e pode remediar os pontos fracos detetados.
* **Acceptance Criteria:**
    * Devem ser listados 5 itens (ou todos, se o total de inputs for inferior a 5).
    * Cada driver deve incluir o nome da feature e a sua contribuição percentual.
* **Variant Impact:** **Yes**

### REQ-004: Estimativa de Sizing (P10/P50/P90)
* **Description:** Calcular a necessidade de equipa (FTEs) com base em volumetria de tickets e SLAs de suporte.
* **Objective:** Evitar o sub-dimensionamento ou sobre-dimensionamento da equipa na fase comercial.
* **Acceptance Criteria:**
    * O output deve apresentar três bandas: Otimista (P10), Provável (P50) e Conservadora (P90).
    * O cálculo deve incluir pressupostos sobre automação esperada.
* **Variant Impact:** No

### REQ-006: Validação de Evidência (Freshness)
* **Description:** Verificar se as evidências fornecidas (ex: links para testes de DR) foram atualizadas nos últimos 12 meses.
* **Objective:** Garantir que o score reflete o estado atual e não dados obsoletos.
* **Acceptance Criteria:**
    * O sistema deve sinalizar evidências com mais de 365 dias como "stale".
    * Evidências obsoletas devem ter um peso negativo no Continuity Score.
* **Variant Impact:** No

### REQ-010: Execução Determinística da Política
* **Description:** Garantir que, para a mesma versão de política e os mesmos inputs, o motor gera sempre o mesmo output.
* **Objective:** Permitir a auditabilidade e reprodutibilidade dos resultados para compliance.
* **Acceptance Criteria:**
    * O sistema deve realizar um "hash check" entre execuções com o mesmo payload.
* **Variant Impact:** **Yes**

## Non-Functional Requirements (NFR)

| ID | Type | Requirement | Measurable Metric | Variant? |
|:--- |:--- |:--- |:--- |:--- |
| **NFR-001** | Performance | Latência reduzida para scoring. | $\le$ 500ms para 95% dos pedidos sob carga normal. | No |
| **NFR-002** | Availability | Disponibilidade do serviço. | 99.9% de uptime mensal. | No |
| **NFR-003** | **[Variante]** | Reprodutibilidade. | 100% de coincidência de hash para inputs idênticos na mesma versão. | **Yes** |
| **NFR-004** | Architecture | Statelessness. | 0 persistência de dados de sessão em base de dados local. | No |
| **NFR-005** | Observability | Rastreabilidade de erros. | Todos os logs devem incluir um `requestId` único. | No |
| **NFR-006** | **[Variante]** | Transparência. | Cada driver retornado deve ter um label legível (human-readable). | **Yes** |