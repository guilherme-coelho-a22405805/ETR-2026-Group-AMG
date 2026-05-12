# AMS Intake Platform — Desktop Prototype (Lab 8)

Protótipo Python desktop (Tkinter) gerado durante o Lab 8 — Vibe Coding.

## Variant 3 — Determinism + Explainability

- **Persona:** Transition Manager
- **Slice:** Continuity Score (UC-02) + Explain (UC-05)
- **REQs implementados:** REQ-002, REQ-006, REQ-007, REQ-009, REQ-010 + NFR-006, NFR-008

## Como correr

Requisitos: Python 3.9+ (Tkinter já vem incluído na maioria das instalações).

```bash
cd ams_prototype
python main.py
```

Para validar o motor sem abrir a UI:

```bash
python smoke_test.py
```

## Estrutura

```
ams_prototype/
├── main.py                # entry point — corre a UI
├── smoke_test.py          # smoke test manual end-to-end
├── ai_engine/
│   ├── policy.py          # REQ-007 (versionamento + checksum)
│   ├── validator.py       # REQ-009 (validação + normalização)
│   ├── scoring.py         # REQ-002 + REQ-010 (score + inputsHash)
│   └── explain.py         # REQ-006 (Top 5 drivers + integrity check)
├── storage/
│   └── runs_store.py      # persistência JSON dos ScoringRuns
├── ui/
│   └── app.py             # Tkinter UI com 3 abas
└── data/
    └── scoring_runs.json  # criado em runtime
```

## Variant constraints implementadas

1. **Determinismo (REQ-010 / NFR-006):** `inputsHash` SHA-256 ignora metadados não-analíticos. Replay do payload original valida o hash.
2. **Explicabilidade (REQ-006 / NFR-008):** Top 5 drivers ordenados por contribuição absoluta, com labels legíveis.
3. **Policy versioning (REQ-007):** Políticas imutáveis com checksum único. Aviso `DEPRECATED` quando aplicável.
4. **UC-05 E1:** Falha de determinismo (tampering) bloqueia a explicação e gera aviso.

## Out of scope (Lab 8)

- Testes automatizados (PyTest) → Lab 11
- Endpoints REST → este protótipo é desktop
- NBQ, Sizing, Change Risk → não fazem parte deste slice
- Autenticação real / RBAC → fora do scope mínimo
