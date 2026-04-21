# Elicitation Notes — Lab 2 (AMS)

## Interview setup
- **Date:** 19/02/2026
- **Client team:** AMS Transition Lead
- **DevTeam:** Grupo 3 (AI Engine)
- **Slice discussed:** Intake & Discovery (AMS)
- **Variant:** Grupo 3

## Context anchors (AMS)
- **Sector:** Healthcare (ex: conformidade HIPAA/PHI).
- **Solution type:** Custom Data Platform.
- **Support model:** L2/L3 AMS (24/7).
- **Key transition pain points:** Falta de evidências de observabilidade e incerteza no dimensionamento da equipa.

## Questions & Answers (10)
1. **Q:** Como é que o sistema decide qual a pergunta mais importante a fazer a seguir?
   **A:** Usamos um serviço NBQ que calcula o peso da informação em falta para o score final.
2. **[Evidence] Q:** Como é que justificam um "Continuity Score" baixo?
   **A:** O sistema devolve um breakdown com os fatores que mais contribuíram negativamente (ex: falta de testes de Disaster Recovery).
3. **[Variant] Q:** Se eu submeter os mesmos dados duas vezes, o score pode mudar?
   **A:** Não, o motor é determinístico. Para a mesma versão da política e inputs, o resultado é idêntico.
4. **[Variant] Q:** O sistema consegue prever quantos técnicos preciso para o projeto?
   **A:** Sim, o Sizing Estimate dá bandas de esforço (P10/P50/P90) baseadas em volume e SLAs.
5. **[Evidence] Q:** Onde é que o motor de IA vai buscar os dados reais para os cálculos?
   **A:** Consumimos os dados do Grupo 1 (Core), como métricas de observabilidade e KPIs.
6. **[Evidence] Q:** Que evidência é necessária para validar o RTO/RPO de uma aplicação?
   **A:** É necessário um link para o último log de teste de DR bem-sucedido e a política de backup.
7. **[Variant] Q:** Quantos drivers de influência devem ser expostos ao utilizador?
   **A:** Devem ser mostrados os "Top 5 drivers" para garantir transparência no processo de decisão.
8. **Q:** O motor de sizing considera o "mix" de competências da equipa?
   **A:** Sim, o cálculo de FTEs deve separar necessidades por papel e nível de senioridade.
9. **Q:** O que acontece se uma recomendação de 90 dias não for cumprida?
   **A:** O Continuity Score será penalizado na próxima execução devido à "frescura" (freshness) dos dados.
10. **Q:** Como é garantida a performance em tempo real?
    **A:** O motor deve responder a pedidos de scoring em menos de 500ms (p95).

## Assumptions (3)
- **A1:** O Grupo 1 fornece os dados via endpoint `/export/{applicationId}` em formato JSON estruturado.
- **A2:** O Grupo 2 é responsável por lidar com a interface de recolha de links de evidência.
- **A3:** A política de pesos para o NBQ é versionada e imutável após publicação.

## Open questions (3)
- **Q1 [Variant]:** Como lidar com o "Top 5 drivers" se o sistema tiver menos de 5 respostas preenchidas?.
- **Q2 [Variant]:** Qual o procedimento de hash check para validar o determinismo entre diferentes ambientes?.
- **Q3:** Que critérios definem o "esforço S/M/L" nas recomendações de 90 dias?.

## Variant notes
- A nossa variante (Grupo 3) forçou o foco no determinismo e explicabilidade. Tivemos de garantir que o motor não é uma "caixa preta", fornecendo sempre os drivers que justificam cada score.