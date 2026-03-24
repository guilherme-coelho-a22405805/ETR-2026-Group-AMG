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