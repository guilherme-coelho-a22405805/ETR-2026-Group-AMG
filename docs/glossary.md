# Glossário — AI Engine

- **NBQ (Next-Best-Question):** Mecanismo lógico que seleciona a pergunta mais informativa a ser feita a seguir para reduzir a incerteza do projeto.
- **Continuity Score:** Métrica de 0 a 100 que avalia a prontidão operacional (ex: existência de DR/BCP, observabilidade).
- **Change Risk Assessment:** Avaliação do risco de falha numa mudança planeada com base no histórico e estratégia de deployment.
- **Sizing Estimate:** Previsão do esforço da equipa (FTEs) e inputs de preço.
- **FTE Bands (P10/P50/P90):** Intervalos estatísticos de confiança para o dimensionamento (P10: Otimista, P50: Provável, P90: Conservador).
- **Policy Version:** Snapshot imutável de regras e pesos que garante que o motor é determinístico e auditável.
- **Feature Definition:** Registo de variáveis consumidas pelo motor, mapeando chaves (ex: `obs.apm`) para fontes de dados do Grupo 1.
- **Determinismo (Replay):** Capacidade de reproduzir exatamente o mesmo resultado através do armazenamento de metadados da execução (`inputsHash`).
- **Embeddings:** Representação vetorial de textos que permite ao motor realizar comparações semânticas entre perguntas e respostas.
- **NER (Named Entity Recognition):** Extração de entidades específicas (vendedores, produtos, ambientes) a partir de texto livre.
- **MTTR (Mean Time To Repair):** Tempo médio gasto para reparar um sistema após uma falha.
- **RTO / RPO:** Objetivos de tempo e ponto de recuperação em cenários de Disaster Recovery.
- **Stateless:** Característica do motor que não armazena o estado das respostas de forma persistente localmente.
- **Top 5 Drivers:** Os cinco fatores com maior peso absoluto que justificam a atribuição de um score.
- **Guardrails:** Restrições ou avisos automáticos incluídos na avaliação de risco para prevenir falhas críticas.