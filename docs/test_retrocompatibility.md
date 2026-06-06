# Test Retrocompatibility — Lab 14

**Team:** ETR-2026-Group-AMG (G3 — AI Engine) · **Variant 3**
**Scope:** `tests/test_engine.py` (UT-01..08) + `bdd/features/*.feature` + `bdd/steps/*.py`

"Retrocompatibilidade de testes" = a capacidade do suite continuar **válido e útil** à medida que o sistema evolui. Abaixo: que mudanças partem os nossos testes, seguido dos pontos frágeis concretos identificados (com prova) e a respetiva ação de melhoria.

---

## O que pode partir os nossos testes?

- **Mudança de requisito (wording / AC):** se o NFR-008 for reescrito para "todos os fatores avaliados" em vez de "exatamente 5", os asserts `len(drivers) == 5` deixam de ser corretos. Mitigação: versionar requisitos e atualizar AC + teste + matriz em conjunto (regra do Lab 14).
- **Mudança de UI:** baixo risco. Os nossos testes (PyTest e Behave) chamam diretamente as funções do `ai_engine`, **não** a UI (Tkinter/Streamlit). Não há seletores de UI nos testes, por isso alterações visuais não os afetam. (Esta é uma força do design "engine-first".)
- **Refactoring (estrutura interna):** risco médio. Os testes importam de caminhos profundos (`docs/ams_prototype_lab8/ams_prototype/ai_engine/...`) via manipulação de `sys.path`. Mover a pasta do motor parte os imports de todos os ficheiros de teste e steps.
- **Ambiente / dependências:** risco real e **comprovado**. O `behave` mudou de comportamento entre versões: o relatório do Lab 13 reporta Behave 1.2.6; em Behave ≥ 1.3 o suite deixa de arrancar por `AmbiguousStep` (ver F-1). A versão do Python e do PyTest também variam (Lab 12 menciona 3.13/pytest 9; execução de manutenção correu em 3.12/pytest 9.0.3).
- **Instabilidade de dados de teste:** baixo a médio. `runId` (UUID) e `computedAt` (timestamp) são não-determinísticos; qualquer assert sobre eles seria frágil. Atualmente evitamo-lo, mas há proximidade do risco (ver F-2).

---

## Pontos frágeis (com prova) + melhorias

### F-1 — Step BDD duplicado → `AmbiguousStep` (CRÍTICO, já corrigido nesta sprint)
- **Ponto frágil:** o step `@then('the drivers are ordered by absolute contribution descending')` estava definido em **dois** módulos: `bdd/steps/steps.py:143` e `bdd/steps/steps_lab13.py`. Como o Behave carrega todos os módulos de `bdd/steps/` num único registo (independentemente da feature a correr), versões recentes do Behave abortam com `AmbiguousStep`.
- **Por que é frágil:** depende da versão do Behave. Em 1.2.6 pode passar despercebido; em ≥ 1.3 o suite **não arranca de todo** — falha não por um cenário falhar, mas por o motor de testes recusar carregar.
- **Prova (execução real, Behave 1.3.3):**
  ```
  behave.step_registry.AmbiguousStep: @then('the drivers are ordered by absolute contribution descending')
  has already been defined in ... at bdd/steps/steps.py:143
  ```
- **Ação de melhoria (APLICADA):** remover a definição duplicada de `steps_lab13.py` e **reutilizar** a única definição em `steps.py` (comportamento idêntico). Após a correção, o suite completo corre: **3 features, 12 cenários, 94 steps, 0 falhas**. Regra de grooming associada: "um comportamento = um step partilhado".

### F-2 — Asserções sobre detalhes instáveis / teste que não exercita o motor (já corrigido nesta sprint)
- **Ponto frágil:** o UT-03 (`test_explain_returns_top_5_ordered`) construía um `mock_run` local, **re-implementava** a ordenação numa lista e fazia asserts sobre essa lista — **nunca chamava `explain_score()`**. Asserts adicionais (`top_5[0]["factor"] == "f3"`) prendiam-se a dados de mock arbitrários, não a comportamento real.
- **Por que é frágil:** o teste passa sempre, mesmo que o código de produção (`explain.py`) parta. É um falso positivo permanente — testa uma cópia da lógica, não o sistema.
- **Prova:** com `explain_score()` propositadamente alterado para devolver drivers por ordem inversa, a versão **antiga** continuaria verde; a versão **reescrita** falha o assert de ordenação (verificado em execução). Logo a nova versão deteta regressões reais.
- **Ação de melhoria (APLICADA):** UT-03 reescrito para gerar um `stored_run` válido (via `validate_and_normalize` + `calculate_continuity_score`) e chamar `explain_score(stored_run, limit=5)`, assertando sobre o **output real**: 5 drivers, ordenados por contribuição absoluta desc, labels não-vazios. Os 8 UT continuam a passar.

### F-3 — Asserção rígida `len(drivers) == 5` acoplada a uma política de 6 fatores
- **Ponto frágil:** vários testes (UT-03, cenários happy) assumem exatamente 5 drivers. Isto só é verdade porque as políticas atuais (`v1.0.0`, `v0.9.0`) têm 6 fatores. Se uma política futura tiver < 5 fatores, `explain_score` devolve `[:limit]` < 5 e os testes falham — **e o próprio NFR-008 fica em contradição** ("obrigatoriamente top 5").
- **Por que é frágil:** acopla o teste a um dado de configuração (nº de fatores da política) que pode mudar, e expõe uma ambiguidade não resolvida no requisito.
- **Ação de melhoria (REGISTADA, não corrigida):** primeiro reescrever a AC do NFR-008 para o comportamento "min(5, nº de fatores)" — proposta já existente em `docs/ac_dod_updates.md` (Item 2). Só depois ajustar o assert para `len(drivers) == min(5, n_fatores_da_policy)`. Não alterado nesta sprint para não mexer no teste antes de a decisão de requisito estar formalizada (alinhamento test-lifecycle ↔ requirement-lifecycle).

### F-4 — Imports por `sys.path` com caminho profundo fixo (fragilidade estrutural)
- **Ponto frágil:** `tests/test_engine.py` e os dois módulos de steps inserem manualmente `docs/ams_prototype_lab8/ams_prototype` em `sys.path`. O caminho está hard-coded em três sítios.
- **Por que é frágil:** mover/renomear a pasta do motor (provável quando sair do "protótipo Lab 8" para uma estrutura mais limpa) parte todos os imports de uma vez, em múltiplos ficheiros.
- **Ação de melhoria (REGISTADA):** centralizar a resolução do caminho num único local (`conftest.py` para PyTest, já existente mas vazio; `bdd/environment.py` para Behave, que já o faz parcialmente) e remover os `sys.path.insert` duplicados dos ficheiros individuais. Candidato a grooming de uma próxima sprint.
