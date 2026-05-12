"""
Local JSON storage para ScoringRuns (REQ-010).
Mantém scope mínimo do Lab 8 — sem DB.
"""
import json
import os
from typing import Dict, Any, List, Optional


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
RUNS_FILE = os.path.join(DATA_DIR, "scoring_runs.json")


def _ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def save_run(normalized_payload: Dict[str, Any], result: Dict[str, Any]) -> str:
    """Persiste um ScoringRun completo. Retorna o runId."""
    _ensure_storage()
    runs = load_all_runs()
    record = {
        "normalizedPayload": normalized_payload,
        "result": result,
    }
    runs.append(record)
    with open(RUNS_FILE, "w", encoding="utf-8") as f:
        json.dump(runs, f, indent=2, ensure_ascii=False)
    return result["runId"]


def load_all_runs() -> List[Dict[str, Any]]:
    _ensure_storage()
    with open(RUNS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_run(run_id: str) -> Optional[Dict[str, Any]]:
    for r in load_all_runs():
        if r["result"]["runId"] == run_id:
            return r
    return None


def clear_all() -> None:
    """Helper para testes — limpa storage."""
    _ensure_storage()
    with open(RUNS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
