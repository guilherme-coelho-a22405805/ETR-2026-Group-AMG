# Use Case Diagram — Lab 5

## System boundary
- System name: AMS Intake Platform
- Slice covered: AI Engine

## Actors 
- AI Researcher / Data Scientist: O ator que submete o modelo de IA para ser integrado na "Engine".
- AI Operations (AIOps) Lead: Quem valida se o modelo tem performance e segurança para entrar em produção.
- Governance Auditor: Ator externo/interno que verifica se o modelo cumpre as normas éticas e de privacidade.
- Model Registry (Sistema Externo): Onde os modelos ficam guardados

## Use cases 
- Registar Novo Modelo: O Researcher submete os metadados do motor de IA.
- Upload de Dataset de Teste: Anexar os dados usados para validar a precisão do modelo.
- Executar Teste de Bias: O sistema verifica automaticamente se a IA tem comportamentos discriminatórios.
- Rever Métricas de Performance: O AIOps analisa o tempo de resposta e consumo de recursos.
- Aprovar Deploy para Produção: O AIOps ou o Auditor autoriza a integração final na AI Engine.
- Gerar Cartão de Modelo (Model Card): Exportar a documentação técnica automática do modelo.

## Diagram file
- Path: `docs/diagrams/use_case_diagram.png` *(or `.puml`)*
- System name: AI Engine (G3)
- Slice covered: Intake & Scoring Logic

## Actors (3)
- **A1: G2 Interface (Intelligent Assistant):** Sistema externo que consome os endpoints de NBQ e Scoring para interagir com o utilizador final.
- **A2: Transition Manager:** Utilizador humano (persona) que consulta as explicações e resultados gerados pelo motor.
- **A3: G1 Core (Operational Core):** Sistema externo que fornece os dados normalizados de infraestrutura e histórico.

## Use cases (6)
- **UC-01: Sugerir próxima pergunta (NBQ):** Determinar a pergunta mais valiosa para reduzir a incerteza.
- **UC-02: Calcular Continuity Score:** Gerar a métrica de prontidão operacional (0-100).
- **UC-03: Avaliar risco de mudança (Change Risk):** Analisar o risco de falha em alterações planeadas.
- **UC-04: Gerar estimativa de Sizing (FTE):** Calcular as bandas P10/P50/P90 de esforço.
- **UC-05: Consultar explicação de score (Explain):** [Variante 3] Identificar os Top 5 drivers de um resultado.
- **UC-06: Validar integridade da execução (Replay):** [Variante 3] Confirmar o determinismo de um cálculo anterior.

## Diagram file
- Path: `docs/diagrams/use_case_diagram.puml`
