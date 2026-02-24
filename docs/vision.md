# Vision - AI Engine (Continuity, Change Risk & Sizing)

### Vision Statement
Desenvolver a camada de inteligência do sistema AMS que atua como o "cérebro" da plataforma. O motor deve garantir uma transição de serviços sem riscos, utilizando uma lógica de Next-Best-Question (NBQ) para guiar o intake de dados, algoritmos de scoring para medir a prontidão (Continuity) e o risco de mudanças, e um estimador preciso para o dimensionamento (Sizing) e custo da equipa de suporte.

### Objectives
1. **Inteligência Adaptativa (NBQ):** Implementar uma política determinística que seleciona a próxima pergunta mais valiosa para reduzir a incerteza do projeto.
2. **Scoring Explicável:** Fornecer scores de Continuidade e Risco de Mudança (0-100) que incluam os "top 5 drivers" (fatores que mais influenciaram o resultado) para garantir transparência.
3. **Estimativa de Esforço:** Criar um motor de sizing que entregue bandas de confiança (P10/P50/P90) para o número de FTEs necessários, baseando-se em volumetria e SLAs.

### Non-Objectives
1. **Persistência de Respostas:** O Grupo 3 é "stateless"; não somos responsáveis por guardar as respostas finais (isso é o Grupo 1).
2. **Interface de Chat:** Não construiremos a UI do assistente (isso é o Grupo 2).
3. **Machine Learning Complexo:** O MVP foca-se em lógica baseada em regras e pesos ponderados, não em treino de modelos generativos ou redes neuronais.