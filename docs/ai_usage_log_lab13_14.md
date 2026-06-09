# AI Usage & Prompt Engineering Log — Labs 13 e 14

**Team:** ETR-2026-Group-AMG (G3 — AI Engine) · Variante 3
**Ferramenta:** Claude (assistente conversacional)
**Âmbito deste documento:** registo do uso de IA nos Labs 13 (BDD + Lighthouse) e 14
(Quality Maintenance: traceability, retrocompatibilidade, grooming).

> Complementa os registos de IA já existentes no repositório:
> - `docs/vibe_coding_log.md` — uso de IA no Lab 8 (geração do protótipo)
> - `docs/test_first_log.md` (secção *AI usage*) — uso de IA no Lab 11 (TDD)
>
> Princípio seguido: documentar o que **realmente** foi pedido e decidido, incluindo o que
> foi **rejeitado** e porquê. A racionalidade da exploração é tão importante como o resultado.

---

## Lab 13 — Bónus Lighthouse (UI quality check)

### Contexto
O Lab 13 (BDD) já estava entregue na parte obrigatória (feature files, steps, `bdd_report.md`,
`traceability_req_bdd.md`). Faltava o bónus opcional do Lighthouse, que requer uma página web.
A equipa tem UI Streamlit (`ui/app_web.py`), pelo que era aplicável.

### Prompts / interação (resumo)
1. **Setup e compreensão:** pedido de explicação do que é o Lighthouse e onde se aplica ao
   projeto (Tkinter vs Streamlit). Conclusão: o Lighthouse só corre na UI **web** (Streamlit),
   não na desktop (Tkinter).
2. **Execução real:** corremos `streamlit run ui/app_web.py`, abrimos a app em `localhost:8501`
   e corremos o Lighthouse via DevTools do Chrome (modo Navigation, device Desktop, categorias
   Performance/Accessibility/Best Practices/SEO).
3. **Geração do relatório:** a partir do PDF exportado pelo Lighthouse (scores e diagnósticos
   reais), pedimos a redação de `docs/lighthouse_report.md` com 3 achados + ações.

### O que foi aceite
- Estrutura do `lighthouse_report.md` (scores, métricas core, 3 findings, ligação a NFRs).
- A leitura de que a Performance baixa (49) vem do framework Streamlit, não da lógica do motor.

### O que foi rejeitado / corrigido (racionalidade)
- **Inventar scores:** recusado por princípio. Só avançámos depois de termos o relatório real
  exportado (Performance 49, Accessibility 99, Best Practices 100, SEO 82).
- **Tratar a Performance 49 como falha do NFR-001:** rejeitado. O NFR-001 mede o *server
  response time* interno do motor (≤ 500ms), não o tempo de carregamento do front-end que o
  Lighthouse mede. A distinção ficou registada no relatório (alinhada com `requirements_validation.md`).

### Evidência
- `docs/lighthouse_report.md` + `docs/assets/lighthouse_report.pdf`

---

## Lab 14 — Quality & Testing Maintenance (Traceability + Retrocompat + Grooming)

### Contexto
Sprint de manutenção. Decisão inicial da equipa: fazer grooming **real** (corrigir problemas
no código/testes), não apenas documental. Antes de escrever qualquer relatório, **executámos
os testes** para diagnosticar com factos.

### Prompts / interação (resumo)
1. **Diagnóstico por execução:** pedido para correr PyTest e Behave e reportar o estado real,
   em vez de assumir pelo que os relatórios antigos diziam.
2. **Análise de pontos frágeis:** pedido para identificar o que poderia partir os testes ao
   longo do tempo (retrocompatibilidade).
3. **Correções de grooming:** pedido para aplicar e validar correções reais, re-executando os
   testes após cada uma.
4. **Consolidação:** pedido para unificar as 4 matrizes de traceability parciais num único
   `traceability_master.md`.

### Descobertas (factos confirmados em execução)
- **`AmbiguousStep`:** o step `the drivers are ordered by absolute contribution descending`
  estava duplicado em `steps.py` e `steps_lab13.py`. Em Behave ≥ 1.3 o suite **não arrancava**
  (o `bdd_report.md` original, em Behave 1.2.6, reportava passagem — exemplo de problema de
  retrocompatibilidade de ferramenta).
- **UT-03 falso positivo:** `test_explain_returns_top_5_ordered` re-implementava a ordenação
  numa lista local e **nunca chamava `explain_score()`** — passava mesmo com o motor partido.
- **Recolha do PyTest:** `python -m pytest` apanhava o `smoke_test.py` (script manual do Lab 8),
  que executa código ao ser importado e quebrava a recolha (`KeyError: 'runId'`).

### O que foi aceite (correções aplicadas)
- Remover o step duplicado e reutilizar a definição única (resolve `AmbiguousStep`).
- Reescrever o UT-03 para chamar `explain_score()` real (provado que agora deteta regressões).
- `conftest.py` a centralizar o `sys.path`; `pytest.ini` com `testpaths = tests`.
- `requirements.txt` na raiz cobrindo app + testes; consolidação da traceability.

### O que foi rejeitado / corrigido (racionalidade)
- **Fixar `behave<1.3` para "fazer o relatório antigo continuar verdade":** rejeitado. Seria
  mascarar a causa-raiz; a teórica 14 trata dependency-pinning evasivo como anti-padrão.
  Optámos por corrigir a duplicação na origem.
- **Reescrever o `bdd_report.md` do Lab 13 como se sempre tivesse dado 30 steps:** rejeitado.
  Seria falsificar histórico. Em vez disso, mantivemos o registo original (24-05) e
  acrescentámos uma secção de **update datada** (07-06) explicando a mudança.
- **Corrigir o bug do `smoke_test.py` (`KeyError`):** rejeitado como fora de âmbito. É um
  utilitário de demo legado, não um teste de validação; isolámo-lo via `pytest.ini` em vez de
  mexer nele.
- **Mexer no `objectives_fcs.md` para preencher o nº da variante:** rejeitado. Alterar um
  deliverable de um lab já entregue por um detalhe cosmético cria mais risco que valor; a
  variante (Grupo 3) já está clara no README e noutros documentos.
- **Fabricar user stories / prompts retroativas de labs antigos:** rejeitado por princípio de
  honestidade — só documentamos o que realmente aconteceu.

### Evidência de execução (após grooming)
- PyTest: 8 passed (`python -m pytest`)
- Behave: 3 features / 12 scenarios / 94 steps — 0 failed (`python -m behave bdd`)
- Detalhe completo em `docs/test_grooming_report.md`, `docs/gap_analysis_lab14.md`,
  `docs/test_retrocompatibility.md`, `docs/traceability_master.md`.

---

## Nota de honestidade sobre o âmbito deste log

Este documento cobre **apenas** os Labs 13 e 14, onde o uso de IA é conhecido e verificável.
O uso de IA noutros labs está registado onde aplicável (`vibe_coding_log.md` — Lab 8;
`test_first_log.md` — Lab 11). Não foram fabricadas prompts para labs onde o uso de IA não
está documentado, por uma questão de integridade da evidência.

> **Para extensão pela equipa (opcional):** se algum elemento tiver histórico real de uso de
> IA noutros labs (ex.: prompts guardados), pode acrescentar aqui uma secção por lab no mesmo
> formato — *Contexto · Prompts (resumo) · Aceite · Rejeitado + racionalidade · Evidência* —
> desde que corresponda a uso que efetivamente ocorreu.
