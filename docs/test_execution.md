# Test Execution — Lab 12

## Stack

**Language:** Python 3.13
**Test framework:** PyTest 9.0.3
**Version requirements:** Python 3.9+

## Setup

1. O repositório não requer dependências complexas nem instalação de pacotes além do `pytest`.
2. **Requisito obrigatório:** Deve existir um ficheiro vazio `conftest.py` na raiz do projeto (`ETR-2026-Group-AMG`) para o Python reconhecer o módulo `ai_engine` corretamente.

## Run all unit tests

**Command:**
    *  `python -m pytest` (executado a partir da raiz do projeto)

## Run a single test file

**Command:**
    *  `python -m pytest tests/test_engine.py`

## Run a single test (optional)

**Command:**
    *  `python -m pytest tests/test_engine.py::test_determinism_ignores_metadata`

## Notes

**Known limitations:** Os testes atuais são executados em memória sem persistência real num sistema de ficheiros externo para acelerar a execução.

**Troubleshooting tips:** Se ocorrer o erro `ModuleNotFoundError: No module named 'ai_engine'`,