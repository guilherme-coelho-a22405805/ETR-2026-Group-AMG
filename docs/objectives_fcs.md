# Objectives & Critical Success Factors (CSFs) — Lab 4

## Variant
- **Variant number:** Group 3
- **Persona:** Transition Manager (Responsável técnico pela validação de serviços)
- **Key constraint focus:** Determinismo algorítmico e explicabilidade (Top 5 drivers)

---

## Objectives (3)

### OBJ-1 — Otimizar a eficiência do processo de recolha de dados (Intake)
- **Description:** Reduzir o tempo e esforço necessários para completar a descoberta de um serviço através de interações inteligentes.
- **Stakeholders impacted:** Transition Manager, Client IT Team.
- **Success signal:** Conclusão do questionário com o número mínimo de perguntas necessárias para atingir confiança no score.
- **Variant-driven:** No

### OBJ-2 — Garantir a transparência e auditabilidade das decisões da IA
- **Description:** Assegurar que cada métrica gerada pelo motor pode ser explicada e rastreada até à sua origem.
- **Stakeholders impacted:** Client Stakeholders, Audit Team.
- **Success signal:** Redução de pedidos de suporte manual para explicar resultados de "Continuity" ou "Risk".
- **Variant-driven:** **Yes**

### OBJ-3 — Assegurar a reprodutibilidade absoluta dos resultados analíticos
- **Description:** Garantir que o sistema produz resultados idênticos para os mesmos inputs, independentemente do ambiente ou momento da execução.
- **Stakeholders impacted:** DevTeam, QA, Compliance Officers.
- **Success signal:** 100% de correspondência de hash em testes de replay para a mesma versão de política.
- **Variant-driven:** **Yes**

---

## Critical Success Factors (3)

### CSF-1 — Eficácia da Política de NBQ (Next-Best-Question)
- **Linked objective:** OBJ-1
- **Definition:** O algoritmo deve selecionar a pergunta que mais reduz a incerteza estatística do projeto.
- **Evidence:** Diminuição da margem de erro do score após cada resposta da NBQ.
- **Variant-driven:** No
- **Linked requirements (3):**
  * REQ-001 (NBQ Service)
  * REQ-009 (Input Validation)
  * NFR-001 (Performance NBQ)

### CSF-2 — Clareza na Exposição de Drivers de Score
- **Linked objective:** OBJ-2
- **Definition:** O motor deve identificar e rotular corretamente os "Top 5 drivers" para cada execução de scoring.
- **Evidence:** Presença do campo `breakdown` legível em todas as respostas de scoring.
- **Variant-driven:** **Yes**
- **Linked requirements (3):**
  * REQ-003 (Change Risk Drivers)
  * REQ-006 (Explain Endpoint)
  * NFR-008 (Labels legíveis)

### CSF-3 — Estabilidade da Versão de Política
- **Linked objective:** OBJ-3
- **Definition:** Implementação de snapshots imutáveis que previnem alterações na lógica de cálculo sem novo versionamento.
- **Evidence:** Consistência do `inputsHash` e `policyVersion` nos logs de execução.
- **Variant-driven:** **Yes**
- **Linked requirements (3):**
  * REQ-007 (Policy Versioning)
  * REQ-010 (Determinism & Replay)
  * NFR-006 (Consistência de Output)