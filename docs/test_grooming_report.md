# Test Grooming Report — Lab 14

**Team:** ETR-2026-Group-AMG (G3 — AI Engine) · **Variant 3** · Slice: Continuity Score + Explain
**Data:** 07/06/2026
**Stack:** Python 3.12 · PyTest 9.0.3 · Behave 1.3.3

Sprint de manutenção de qualidade: limpeza de ativos de teste, com prova de execução antes/depois.

---

## Grooming actions performed (min. 5)

### 1. Remover step BDD duplicado (resolve `AmbiguousStep`)
- **File(s):** `bdd/steps/steps_lab13.py` (removida 1 definição), reutiliza `bdd/steps/steps.py:143`
- **Why:** O step `@then('the drivers are ordered by absolute contribution descending')` estava definido em **dois** módulos com texto idêntico. Como o Behave carrega todos os módulos de `bdd/steps/` num único registo, versões ≥ 1.3 abortam o suite inteiro com `AmbiguousStep` — nem chega a correr cenários. Princípio aplicado: "um comportamento = um único step partilhado" (reuse de step definitions).
- **Antes (execução real):** `behave bdd/features/lab13.feature` → `behave.step_registry.AmbiguousStep: ... already been defined ... at bdd/steps/steps.py:143` (suite não arranca).
- **Depois:** suite completo corre — 3 features / 12 cenários / 94 steps / 0 falhas.

### 2. Reescrever UT-03 para testar o motor real (eliminar falso positivo)
- **File(s):** `tests/test_engine.py` (função `test_explain_returns_top_5_ordered`)
- **Why:** A versão anterior construía um `mock_run` local, re-implementava a ordenação numa lista e fazia asserts sobre essa lista — **nunca chamava `explain_score()`**. Era um teste que passava sempre, mesmo que o código de produção partisse (falso positivo permanente). Reescrito para gerar um `stored_run` válido (`validate_and_normalize` + `calculate_continuity_score`) e chamar `explain_score(stored_run, limit=5)`, assertando sobre o output real (5 drivers, ordenação por contribuição absoluta desc, labels não-vazios).
- **Prova de valor:** com `explain_score()` propositadamente partido (drivers invertidos), a versão antiga continuaria verde; a versão nova **falha** o assert de ordenação. Logo passou a detetar regressões reais.
- **Depois:** 8/8 unit tests continuam a passar.

### 3. Adicionar dependências de teste documentadas
- **File(s):** `requirements-test.txt` (novo)
- **Why:** Não existia ficheiro de dependências de teste. O `requirements.txt` do protótipo lista apenas `streamlit`, deixando `pytest`/`behave` por documentar — o que provoca `ModuleNotFoundError`/`behave: not found` numa máquina limpa (o próprio `docs/test_execution.md` já alertava para o `ModuleNotFoundError`). Acrescentado `pytest>=8.0` e `behave>=1.2.6`. Decisão consciente: **não** fixar `behave<1.3` para mascarar o `AmbiguousStep` — a causa-raiz foi corrigida na ação 1, portanto o suite corre em qualquer versão recente.

### 4. Centralizar a resolução de `sys.path` no `conftest.py`
- **File(s):** `conftest.py` (estava vazio; agora resolve o caminho do `ai_engine`)
- **Why:** O caminho profundo `docs/ams_prototype_lab8/ams_prototype` estava hard-coded em três sítios (`tests/test_engine.py`, `bdd/steps/steps_lab13.py`, `bdd/environment.py`). Centralizar reduz a duplicação e o risco de partir tudo de uma vez quando a pasta do motor for movida (ponto frágil F-4). O `conftest.py` continua a servir de marcador de raiz do pacote, como exigido em `docs/test_execution.md`.
- **Prova:** um teste sem `sys.path` próprio passa a resolver `ai_engine` apenas via `conftest.py` (verificado em execução).

### 5. Consolidar traceability num único source-of-truth
- **File(s):** `docs/traceability_master.md` (novo)
- **Why:** A rastreabilidade estava dispersa por 4 ficheiros parciais (`traceability_req_tc.md`, `traceability_req_bdd.md`, `traceability_req_ac_tc.md`, `traceability_uc_req.md`), cada um de um lab. Consolidados numa matriz REQ → AC → TC/UT → BDD → Evidência (18 linhas REQ/NFR), com os REQ fora do slice marcados explicitamente como OOS. Os ficheiros antigos ficam como histórico.

### 6. Padronizar nomenclatura e cruzamento de IDs
- **File(s):** `docs/traceability_master.md`, `docs/gap_analysis_lab14.md`
- **Why:** Os labs anteriores misturavam "TC-###" (especificação) e "UT-##" (teste implementado) sem distinção clara. Padronizada a legenda (TC = caso de teste documentado; UT = teste automatizado em `tests/test_engine.py`) e garantido cross-link em ambos os sentidos (REQ↔teste). Resolve a leitura "teste sem REQ" / "REQ sem teste".

---

## Traceability updates
- **O que mudou em `traceability_master.md`:** criada a matriz consolidada; UT-03 agora referenciado como execução real do motor; estado BDD atualizado para o suite completo pós-correção (3/12/94); REQ fora do slice classificados como OOS.
- **Gaps resolvidos:** falso positivo do UT-03 (F-2); bloqueio de arranque do BDD (F-1); ausência de dependências de teste; dispersão de matrizes. Gaps **registados mas não corrigidos** (exigem decisão de requisito primeiro): REQ-007 AC-3 sem teste de política deprecated; conflito NFR-008 "< 5 fatores" (ver `gap_analysis_lab14.md` e `test_retrocompatibility.md`).

---

## Test execution evidence
- **Date:** 07/06/2026
- **Commands used:**
  - `python -m pytest tests/test_engine.py -v`
  - `python -m behave bdd`
  - `python -m behave bdd/features/lab13.feature`
- **Unit tests:** executados **8**, passed **8**, failed **0**
- **BDD scenarios (suite completo bdd/):** executados **12**, passed **12**, failed **0** (3 features, 94 steps)
- **BDD scenarios (só lab13):** executados **4**, passed **4**, failed **0** (30 steps)
- **Notes on failures:**
  - **Antes do grooming**, o suite BDD **não arrancava** em Behave ≥ 1.3 (`AmbiguousStep` por step duplicado). Após a ação 1, passa em qualquer versão.
  - Nota de calibração: o `docs/bdd_report.md` do Lab 13 reportava "22 steps" para o lab13 isolado; a contagem real após grooming é **30 steps** (4 cenários). A diferença vem da contagem de steps do `Background`/`And` — o número atual é o correto e reprodutível.

---

## Lessons learned
- **Maior fonte de fragilidade:** dependência da **versão da ferramenta** (Behave) combinada com **duplicação de steps**. Um problema que "passava" num ambiente quebrava o suite noutro — exatamente o cenário de retrocompatibilidade que a teórica 14 descreve. A lição: tratar a causa-raiz (deduplicar) em vez de fixar a versão antiga.
- **Melhoria de maior valor:** a reescrita do UT-03 (ação 2). Um teste que passa sempre dá falsa confiança; transformá-lo num teste que chama o código real e que comprovadamente falha perante uma regressão é o ganho de qualidade mais relevante desta sprint.
- **Alinhamento lifecycle:** duas lacunas de AC (REQ-007 AC-3 e NFR-008) ficaram deliberadamente por automatizar até a decisão de requisito estar formalizada — respeitando o princípio de que o test-lifecycle acompanha o requirement-lifecycle, e não o contrário.
