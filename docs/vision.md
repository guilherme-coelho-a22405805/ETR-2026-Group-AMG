# Vision — AI Engine (Continuity, Change Risk & Sizing)

### Vision Statement
Desenvolver a camada de inteligência do sistema AMS que atua como o "cérebro" da plataforma. O motor deve garantir uma transição de serviços sem riscos, utilizando uma política de Next-Best-Question (NBQ) para guiar o intake de dados, algoritmos de scoring para medir a prontidão (Continuity) e o risco de mudanças, e um estimador preciso para o dimensionamento (Sizing) e custo da equipa de suporte.

### Objectives
1. **Inteligência Adaptativa (NBQ):** Implementar uma política determinística (rule-based com pesos) que seleciona a próxima pergunta mais valiosa para reduzir a incerteza do projeto.
2. **Scoring Explicável:** Fornecer scores de Continuidade e Risco de Mudança (0-100) que incluam obrigatoriamente os "top 5 drivers" para garantir transparência total ao utilizador.
3. **Estimativa de Esforço:** Criar um motor de sizing que entregue bandas de confiança (P10/P50/P90) para o número de FTEs necessários, baseando-se em volumetria, SLAs e janelas de serviço.

### Non-Objectives
1. **Persistência de Respostas:** O motor é stateless; não somos responsáveis por guardar as respostas finais (tarefa do Grupo 1).
2. **Interface de Chat:** Não construiremos a UI do assistente ou ferramentas de autoria (tarefa do Grupo 2).
3. **Machine Learning Complexo:** O MVP foca-se em lógica baseada em regras e pesos ponderados, excluindo treino de modelos generativos ou RL policies.