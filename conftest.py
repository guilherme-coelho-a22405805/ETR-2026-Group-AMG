"""
conftest.py — raiz do projeto.

Grooming Lab 14 (acao 4): centraliza a resolucao do caminho do motor `ai_engine`
num unico local, em vez de cada ficheiro de teste repetir o mesmo
`sys.path.insert(...)` com o caminho profundo hard-coded.

Mantem-se o ficheiro como marcador de raiz para o PyTest reconhecer o pacote
(requisito ja documentado em docs/test_execution.md).
"""
import os
import sys

_AI_ENGINE_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "docs", "ams_prototype_lab8", "ams_prototype",
)
if _AI_ENGINE_ROOT not in sys.path:
    sys.path.insert(0, _AI_ENGINE_ROOT)
