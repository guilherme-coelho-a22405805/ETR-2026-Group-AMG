import sys
import os

# Calcula a raiz do projecto a partir da localização deste ficheiro (bdd/environment.py)
_BDD_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_BDD_DIR)  # sobe de bdd/ para a raiz

_AI_ENGINE_ROOT = os.path.join(
    _PROJECT_ROOT,
    "docs",
    "ams_prototype_lab8",
    "ams_prototype",
)

if _AI_ENGINE_ROOT not in sys.path:
    sys.path.insert(0, _AI_ENGINE_ROOT)


def before_all(context):
    pass