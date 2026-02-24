# Elicitation Notes — Lab 2 (AMS)

## Interview setup
- Date: 19/02/2026
- Client team:
- DevTeam:
- Slice discussed: Intake & Discovery (AMS)
- Variant: Grupo 3

## Context anchors (AMS)
- Sector:
- Solution type:
- Support model (L1/L2/L3 + hours + languages):
- Key transition pain points (summary):

## Questions & Answers (min. 10)
1. Q: Como é que o sistema decide qual a pergunta mais importante a fazer a seguir?
   A: Usamos um serviço chamado NBQ que calcula o "peso" da informação em falta para o score final.
2. [Evidence] Q: Como é que justificam um "Continuity Score" baixo?
   A: O sistema devolve um breakdown com os fatores (features) que mais contribuíram negativamente, como a falta de testes de Disaster Recovery.
3. [Variant] Q: Se eu fizer a mesma pergunta duas vezes com os mesmos dados, o resultado da IA pode mudar?
   A: Não, o motor é determinístico. Para a mesma versão da política e inputs, o resultado é idêntico.
4. [Variant] Q: O sistema consegue prever quantos técnicos preciso para o projeto?
   A: Sim, o Sizing Estimate dá bandas de esforço (P10/P50/P90) baseadas no volume de tickets e SLAs.
5. [Evidence] Q: Onde é que o motor de IA vai buscar os dados reais para os cálculos?
   A: Consumimos os dados do Grupo 1 (Core), especificamente métricas de observabilidade, histórico de mudanças e KPIs.


...

## Assumptions (min. 3)
- A1: ...
- A2: ...
- A3: ...

## Open questions (min. 3)
- Q1: ...
- Q2: ...
- Q3: ...

## Variant notes (required)
- How did the variant change our elicitation focus?
  - ...