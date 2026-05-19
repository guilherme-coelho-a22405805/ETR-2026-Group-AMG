# Vibe Coding Log — Lab 8

## Tool used

- **Tool:** Claude (assistente AI conversacional, modo "vibe coding")
- **Environment / stack:** Python 3.9+, Tkinter (UI), JSON local (storage)
- **Sem dependências externas:** o protótipo corre com a biblioteca standard
  do Python — sem `pip install` necessário.

## Approach summary

Em vez de delegar ao tool a decisão de scope, alimentámo-lo com:

- o nosso **Variant Assignment** (Grupo 3 — Determinism + Explainability),
- a `Requirements v1` com os REQs marcados como variant-driven,
- os Use Cases v2 (UC-02 e UC-05) com main + alt + exception flows,
- os Acceptance Criteria (incluindo os Given/When/Then do REQ-006 e REQ-010).

A partir daí seguimos **2 ciclos** de prompt → generate → run → fix, descritos abaixo.

---

## Iteration 1 — Núcleo do motor (engine-first)

**Prompt (resumo):**

> "Gera o núcleo de um motor de Continuity Score em Python:
> - módulo `policy.py` com 2 versões de política (uma `active`, uma `deprecated`)
>   e checksum SHA-256 estável (REQ-007).
> - módulo `validator.py` que valide `application_id`, `sector` (enum) e `responses`,
>   e devolva `uncertainty_applied=True` quando faltarem campos opcionais
>   (REQ-009, REQ-002 AC-3). MISSING_FIELDS quando faltarem campos obrigatórios (E1).
> - módulo `scoring.py` que calcule score 0-100 e produza `inputsHash`
>   SHA-256 calculado **apenas** sobre features analíticas — para que metadados
>   diferentes produzam o mesmo hash (REQ-010 AC).
> - módulo `explain.py` que devolva os **Top 5** drivers ordenados por contribuição
>   absoluta (REQ-006 + NFR-008), com bloqueio se o replay do hash falhar
>   (UC-05 E1)."

**Generated output (o que apareceu):**

- 4 ficheiros em `ai_engine/`: `policy.py`, `validator.py`, `scoring.py`, `explain.py`
- Estrutura limpa por responsabilidade
- Classes `ValidationError` e `DeterminismError` para flows de exceção

**Kept (accepted):**

- Toda a arquitetura modular do `ai_engine/`
- A separação entre `compute_inputs_hash` (utility pura) e `calculate_continuity_score`
- O método `replay_score` em `scoring.py` (essencial para o check de integridade)
- O parâmetro `limit=5` no `explain_score` com default — alinhado com o AC do REQ-006

**Rejected (feature drift / out of scope):**

- A primeira versão do tool propunha um módulo `risk.py` para Change Risk (REQ-003)
  → **rejeitado:** fora do slice escolhido.
- Sugestão de adicionar logs estruturados JSON (NFR-005)
  → **rejeitado:** NFR-005 não está nos 7 REQs deste lab; deixámos para Lab 11.
- Sugestão de criar um endpoint Flask
  → **rejeitado:** o utilizador pediu **desktop**, não REST.

**Manual verification (smoke_test.py):**

- ✅ Happy path: payload completo → score 73/100, `uncertainty_applied=False`
- ✅ Alternative flow A1: 4 fatores omitidos → `uncertainty_applied=True`, score 38/100
- ✅ Exception E1 `MISSING_FIELDS`: payload sem `application_id` → `ValidationError`
- ✅ REQ-010 AC: payload com `application_id` diferente mas mesmas features
  produziu **exatamente o mesmo `inputsHash`** — variant constraint satisfeita.

**Changes made after generation (manual edits):**

- Ajustar `compute_inputs_hash` para serializar **só** as `responses` + `policy_version`,
  excluindo `application_id` e `timestamp` (o tool inicialmente incluía tudo, o que
  quebrava o AC do REQ-010 — metadados não-analíticos NÃO devem afetar o hash).
- Adicionar `clamp` de valores [0.0, 1.0] no validator para robustez.

---

## Iteration 2 — UI desktop + storage + exception flow do UC-05

**Prompt (resumo):**

> "Cria agora uma UI desktop em Tkinter com 3 abas:
> 1. **Calcular Score**: form com sliders para os 6 fatores (com checkbox 'incluir'
>    para simular o alternative flow A1), submeter e mostrar resultado.
> 2. **Explicar Score**: dropdown com runIds existentes, botão Explicar, output
>    formatado com os Top 5 drivers. **Botão extra de 'Simular adulteração'**
>    que altera o payload guardado e mostra o `DeterminismError` (UC-05 E1).
> 3. **Registo de Políticas**: tabela com versões + checksums.
> Persistir cada execução em `data/scoring_runs.json`."

**Generated output:**

- `ui/app.py` (Tkinter, 3 abas via `ttk.Notebook`)
- `storage/runs_store.py` (CRUD em JSON local)
- `main.py` como entry point

**Kept:**

- Sliders 0–1 com label dinâmica que atualiza enquanto se arrasta
- Checkbox "incluir" por fator → permite demonstrar A1 (uncertainty) sem editar código
- Combobox de runIds que faz refresh automaticamente após cada cálculo
- Botão **"Simular adulteração"** — útil para demos, mostra a Variant 3 a bloquear

**Rejected:**

- Sugestão de gráfico matplotlib para o breakdown
  → **rejeitado:** introduzia dependência externa, scope creep para um Lab 8.
- Sugestão de export PDF (alternative flow A1 do UC-05 menciona PDF)
  → **rejeitado por agora:** documentado como out-of-scope explícito em
  `generated_scope.md`; ficou candidato a um Lab futuro.
- Validação no lado da UI antes de chamar o motor
  → **rejeitado:** o validador do `ai_engine` é a única fonte de verdade
  (single source of truth). Duplicar validação criaria divergência.

**Manual verification (via UI + smoke_test.py):**

- ✅ Happy path: preencher form e calcular score → resultado com runId persistido
- ✅ Alternative flow A1: desmarcar 3-4 checkboxes → resultado mostra
  `uncertainty: True` e lista os missing fields
- ✅ Exception E1: vazar Application ID → popup "Erro de Validação: MISSING_FIELDS"
- ✅ UC-05 happy path: selecionar runId da combobox → Top 5 drivers formatados
- ✅ **UC-05 E1 Variant:** botão "Simular adulteração" → explicação bloqueada,
  hashes original e replay impressos lado a lado.

**Changes made after generation:**

- Trocar o "show" do output entre abas: original era um único `Text`,
  separámos em `score_output` e `explain_output` para não sobrescrever.
- Adicionar refresh do combobox depois de cada cálculo
  (`_refresh_explain_runs`) para não obrigar a fechar e abrir a app.

---

## Notes (lessons learned)

- **Ambiguidade detetada no REQ-010 AC:** O AC original diz "features idênticas
  mas metadados não-analíticos diferentes". Não definíamos quais campos eram
  "metadados não-analíticos". Resolvemos isso considerando que **só** `responses`
  e `policy_version` entram no hash; `application_id`, `timestamp` e o que
  vier futuramente como traçabilidade ficam fora. Vamos refletir isto numa
  nota no Lab 10 (`docs/ac_dod_updates.md`).
- **Constraint que faltava inicialmente no prompt:** quando pedimos a UI, esquecemos
  de dizer "sem dependências externas". O tool propôs `customtkinter` (mais
  bonito mas requer `pip install`). Tivemos de pedir refactor para `ttk` standard.
  → Lição: ao prompt-arrastar a IA, **explicitar sempre os limites de stack**.
- **O que mudaríamos nos requisitos depois desta experiência:**
  - O REQ-006 deveria especificar o comportamento quando há **menos** de 5
    drivers (ex.: política com 4 fatores) — atualmente devolveríamos os 4 sem
    erro, mas o NFR-008 diz "obrigatoriamente os top 5". Conflito documentado
    para Lab 10.
  - O AC-2 do REQ-002 ("incluir `policyVersion`") deveria também exigir o
    `policyChecksum`, porque sem checksum a auditoria não consegue distinguir
    duas versões com o mesmo nome ressuscitadas.
- **Sucesso da abordagem "engine-first":** Começar pelo motor (Iteration 1)
  antes da UI (Iteration 2) facilitou o smoke test e permitiu validar a Variant 3
  **sem depender** de cliques em UI — algo que vai ser muito útil quando
  chegarmos ao Lab 11 (test-first).
