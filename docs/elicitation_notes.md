# Elicitation Notes — Lab 2 (AMS)

## Interview setup
- **Date:** 19/02/2026
- **Client team:** AMS Transition Lead
- **DevTeam:** Grupo 3 (AI Engine)
- **Slice discussed:** Intake & Discovery (AMS)
- **Variant:** Grupo 3

## Context anchors (AMS)
- **Sector:** Serviços de Gestão de Aplicações (AMS)
- **Solution type:** Motor de IA para scoring e sizing
- **Support model:** L1/L2/L3 (24/7)
- **Key transition pain points:** Falta de visibilidade sobre a prontidão operacional e dificuldade em estimar esforço de equipa

## Questions & Answers (10)
1. **Q:** Como é que o sistema decide qual a pergunta mais importante a fazer a seguir?
   **A:** Usamos um serviço chamado NBQ que calcula o "peso" da informação em falta para o score final.
2. **[Evidence] Q:** Como é que justificam um "Continuity Score" baixo?
   **A:** O sistema devolve um breakdown com os fatores (features) que mais contribuíram negativamente, como a falta de testes de Disaster Recovery.
3. **[Variant] Q:** Se eu fizer a mesma pergunta duas vezes com os mesmos dados, o resultado da IA pode mudar?
   **A:** Não, o motor é determinístico. Para a mesma versão da política e inputs, o resultado é idêntico.
4. **[Variant] Q:** O sistema consegue prever quantos técnicos preciso para o projeto?
   **A:** Sim, o Sizing Estimate dá bandas de esforço (P10/P50/P90) baseadas no volume de tickets e SLAs.
5. **[Evidence] Q:** Onde é que o motor de IA vai buscar os dados reais para os cálculos?
   **A:** Consumimos os dados do Grupo 1 (Core), especificamente métricas de observabilidade e KPIs.
6. **[Evidence] Q:** Como é validada a existência de um plano de Disaster Recovery (DR)?
   **A:** O sistema requer um link para o documento no SharePoint ou um log de teste de DR recente como prova.
7. **[Variant] Q:** Quantos fatores de influência (drivers) devem ser mostrados no score?
   **A:** Devem ser mostrados os "Top 5 drivers" para garantir que o utilizador percebe o que mais afeta o score.
8. **Q:** O que acontece se o utilizador não souber responder a uma pergunta da NBQ?
   **A:** O sistema permite saltar, mas o score de incerteza aumenta, e a pergunta voltará a aparecer mais tarde.
9. **Q:** O motor de sizing considera diferentes fusos horários?
   **A:** Sim, o cálculo de FTEs (Full-Time Equivalent) ajusta-se conforme a janela de suporte (ex: 8x5 vs 24/7).
10. **Q:** A lógica de scoring é fixa para todos os clientes?
    **A:** A estrutura é a mesma, mas os pesos podem ser ajustados por versão da política de transição.

## Assumptions (3)
- **A1:** Os dados fornecidos pelo Grupo 1 (Core) chegam em formato estruturado (JSON/API).
- **A2:** O motor não precisa de guardar histórico, sendo totalmente stateless.
- **A3:** Existe uma política de pesos pré-definida para o cálculo inicial do Continuity Score.

## Open questions (3)
- **Q1 [Variant]:** Como apresentar o breakdown de drivers se o cálculo utilizar menos de 5 variáveis?
- **Q2 [Variant]:** Como garantir o determinismo se houver atualizações na política de pesos a meio de um processo de intake?
- **Q3:** Qual o nível de confiança estatística exigido para as bandas P90 no sizing estimate?

## Variant notes
- A nossa variante (Grupo 3) obrigou-nos a focar na transparência do algoritmo. Em vez de um score opaco, tivemos de detalhar como os "drivers" são expostos ao utilizador e garantir que o motor não produz resultados aleatórios.