# ETR 2026 — Grupo AMG
**G3 — AI Engine · Variante 3 (Determinism + Explainability)**

Plataforma **AMS Intake** — motor de cálculo do *Continuity Score* com explicabilidade
e garantias de determinismo. Slice implementado: **Continuity Score (UC-02) + Explain (UC-05)**.
Persona: *Transition Manager*.

## Elementos do grupo
- Afonso Rodrigues
- Guilherme Coelho
- Miguel Lopes
- Diogo Faísca

## Stack técnica
- **Track de testes:** PyTest (unitários) + Behave (BDD / integração)
- **Aplicação:** Python — UI web em Streamlit
- **Projeto:** AMS Baseline (Opção A)

---

## Estrutura do repositório

```
ETR-2026-Group-AMG/
├── README.md                  # este ficheiro
├── requirements.txt           # dependencias (app + testes)
├── conftest.py                # raiz do pacote de testes (resolve o ai_engine)
├── ai-engine/ ...             # ver docs/ams_prototype_lab8/ams_prototype
├── tests/
│   └── test_engine.py         # testes unitarios (PyTest)
├── bdd/
│   ├── environment.py         # setup do Behave
│   ├── features/              # cenarios Gherkin (lab9, lab11, lab13)
│   └── steps/                 # step definitions
└── docs/
    ├── ams_prototype_lab8/ams_prototype/
    │   ├── ai_engine/         # MOTOR: policy, validator, scoring, explain
    │   └── ui/app_web.py      # aplicacao web (Streamlit)
    └── *.md                   # documentacao de requisitos e testes (Labs 1-14)
```

A lógica de negócio vive em `docs/ams_prototype_lab8/ams_prototype/ai_engine/`.
A UI web (`ui/app_web.py`) e os testes chamam diretamente esse motor.

---

## Pré-requisitos

- **Python 3.9+** (desenvolvido e testado em 3.12 / 3.13/ 3.14)
- **pip** e, opcionalmente, **git**

Confirmar a versão do Python:
```bash
python --version
```

---

## Configuração do ambiente

A partir da **raiz** do projeto (`ETR-2026-Group-AMG`).

### 1. (Recomendado) Criar e ativar um ambiente virtual

**Windows (cmd):**
```bat
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

Isto instala a aplicação (Streamlit) e as ferramentas de teste (PyTest, Behave).

---

## Como executar a aplicação

A aplicação web (Streamlit) corre no browser:

```bash
streamlit run docs/ams_prototype_lab8/ams_prototype/ui/app_web.py
```

O browser abre automaticamente em `http://localhost:8501`. A interface tem três
separadores:
1. **Calcular Score (UC-02)** — submeter um payload de prontidão e obter o Continuity Score.
2. **Explicar Score (UC-05)** — ver os Top 5 drivers de um score; inclui demo da
   exceção de determinismo (E1).
3. **Registo de Políticas** — versões de política e respetivos checksums SHA-256.

> Existe também uma UI desktop equivalente em Tkinter
> (`docs/ams_prototype_lab8/ams_prototype/ui/app.py`), correndo
> `python docs/ams_prototype_lab8/ams_prototype/main.py`. A via recomendada é a web.

---

## Como executar os testes

Todos os comandos a partir da **raiz** do projeto.

### Testes unitários (PyTest)
```bash
python -m pytest
```
Resultado esperado: **8 passed** (`tests/test_engine.py`).

### Testes de integração BDD (Behave)
Suite completo (lab9 + lab11 + lab13):
```bash
python -m behave bdd
```
Resultado esperado: **3 features, 12 scenarios, 94 steps — 0 failed**.

Apenas os cenários do Lab 13:
```bash
python -m behave bdd/features/lab13.feature
```

> **Nota:** o `conftest.py` na raiz resolve automaticamente o caminho do módulo
> `ai_engine`. Se ocorrer `ModuleNotFoundError: No module named 'ai_engine'`,
> confirmar que os comandos são executados a partir da raiz do projeto.

---

## Documentação

A pasta `docs/` contém toda a documentação produzida ao longo dos laboratórios:
requisitos (`requirements_v1.md`, `acceptance_criteria.md`), use cases, planos e
casos de teste (`test_plan.md`, `test_cases.md`), relatórios de execução
(`unit_test_report.md`, `bdd_report.md`) e a rastreabilidade consolidada
(`traceability_master.md`).
