# Requirements v0 — Lab 2 (AMS)

| Item | Requirement | Type | Stakeholder | Priority | Variant? |
|---:|---|---|---|---|---|
| 1 | O sistema deve calcular o Continuity Score (0-100) com base em métricas de observabilidade e DR. | FR | Transition Lead | H | No |
| 2 | O motor deve identificar os "Top 5 drivers" que mais influenciaram cada score gerado. | FR | Transition Lead | H | **Yes** |
| 3 | O sistema deve manter um comportamento determinístico (mesmo input = mesmo output). | NFR | DevTeam | H | **Yes** |
| 4 | O motor deve sugerir a próxima pergunta (NBQ) baseando-se na redução de incerteza do score. | FR | Transition Manager | M | No |
| 5 | O sistema deve estimar o esforço de equipa em bandas P10, P50 e P90. | FR | Service Manager | H | No |
| 6 | O motor não deve armazenar dados de resposta (stateless), delegando a persistência ao Core. | NFR | Architect | M | No |
| 7 | O cálculo de risco deve considerar o histórico de falhas de mudanças (Change Risk). | FR | Transition Manager | M | No |
| 8 | O sistema deve validar se o link fornecido como evidência aponta para o domínio oficial da empresa. | FR | Auditor | M | No |
| 9 | O breakdown explicável do score deve ser gerado em menos de 2 segundos. | NFR | User | L | **Yes** |
| 10 | O sistema deve permitir a exportação dos drivers do score para formato PDF/Relatório. | FR | Client | L | No |

## Ambiguity rewrite (min. 5)
1) **Original:** "O motor de IA deve ser rápido."
   **Rewritten:** "O motor de IA deve retornar os resultados de scoring e NBQ em menos de 3 segundos após receber os inputs."
2) **Original:** "O sistema deve mostrar porque é que o score é baixo."
   **Rewritten [Variant]:** "O sistema deve listar explicitamente os 5 fatores (drivers) com maior peso negativo no cálculo do Continuity Score."
3) **Original:** "As estimativas de equipa devem ser precisas."
   **Rewritten:** "O motor de sizing deve calcular o número de FTEs necessários com base numa margem de confiança P90 para cenários conservadores."
4) **Original:** "O motor deve funcionar sempre da mesma maneira."
   **Rewritten [Variant]:** "Dada a mesma versão da política de scoring e o mesmo conjunto de dados de entrada, o output do sistema deve ser idêntico em todas as execuções."
5) **Original:** "O sistema deve pedir os dados em falta."
   **Rewritten:** "O mecanismo NBQ deve selecionar e apresentar a pergunta que, se respondida, resulte na maior redução percentual da incerteza do score final."