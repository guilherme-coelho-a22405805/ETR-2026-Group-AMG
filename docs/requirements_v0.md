# Requirements v0 — Lab 2 (AMS)

| Item | Requirement | Type | Stakeholder | Priority | Variant? |
|---:|---|---|---|---|---|
| 1 | O sistema deve expor o endpoint `POST /nbq/next` para sugerir a pergunta que maximiza a redução de incerteza. | FR | G2 Interface | H | No |
| 2 | O motor deve calcular o Continuity Score (0-100) baseando-se em Observabilidade, DR, Acessos e Runbooks. | FR | Transition Lead | H | No |
| 3 | **[Variante]** Cada score gerado deve incluir obrigatoriamente um breakdown dos "top 5 drivers" de influência. | FR | Transition Mgr | H | **Yes** |
| 4 | **[Variante]** O sistema deve garantir determinismo total; mesmos inputs + mesma versão de política = mesmo output. | NFR | Auditor / Dev | H | **Yes** |
| 5 | O motor de sizing deve retornar bandas FTE (P10, P50, P90) com base em volumetria e SLAs. | FR | Service Mgr | H | No |
| 6 | A latência p95 para os endpoints de scoring e NBQ não deve exceder os 500ms. | NFR | G2 Interface | M | No |
| 7 | O sistema deve gerar recomendações de 90 dias com campos de impacto (H/M/L) e esforço (S/M/L). | FR | Transition Lead | M | No |
| 8 | O motor deve ser stateless, consumindo dados do Grupo 1 sem persistir respostas localmente. | NFR | Architect | H | No |
| 9 | O sistema deve validar a autenticidade e validade temporal (freshness) dos links de evidência fornecidos. | FR | Auditor | M | No |
| 10 | **[Variante]** O sistema deve expor o endpoint `POST /explain` para detalhar a metodologia de cálculo de um score. | FR | Client | L | **Yes** |

## Ambiguity rewrite (min. 5)
1) **Original:** "O motor deve ser rápido."
   **Rewritten:** "A latência p95 para os endpoints de scoring (Continuity e Risk) deve ser inferior a 500ms em condições de carga normal.".
2) **Original:** "O sistema deve explicar o score."
   **Rewritten [Variant]:** "O motor deve retornar um array com os 5 fatores (drivers) que tiveram maior peso absoluto no cálculo final do Continuity Score.".
3) **Original:** "As estimativas de equipa devem ser realistas."
   **Rewritten:** "O motor de sizing deve apresentar bandas de FTE P10 (otimista), P50 (provável) e P90 (conservador) com base na volumetria histórica.".
4) **Original:** "O motor não deve mudar de ideias."
   **Rewritten [Variant]:** "Dada a mesma versão de PolicySnapshot e o mesmo payload de entrada, o sistema deve produzir um output com o mesmo hash de verificação.".
5) **Original:** "O sistema deve sugerir melhorias."
   **Rewritten:** "O sistema deve listar ações prioritárias para os próximos 90 dias, vinculadas a sinais fracos ou evidências em falta no intake.".