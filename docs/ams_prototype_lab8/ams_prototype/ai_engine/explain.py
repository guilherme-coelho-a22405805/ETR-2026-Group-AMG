"""
Explain Endpoint (REQ-006) — Variant 3
Devolve Top 5 drivers ordenados por contribuição absoluta.
Reflecte UC-05 incluindo a exceção E1 (falha de determinismo bloqueia explicação).
"""
from typing import Dict, Any, List

from .scoring import replay_score
from .policy import get_policy


def explain_score(stored_run: Dict[str, Any], limit: int = 5) -> Dict[str, Any]:
    """
    REQ-006 AC: Top 5 drivers ordenados por contribuição absoluta, do maior para o menor.
    UC-05 E1 (variant): bloqueia se o replay não produzir o mesmo hash.

    Returns dict com:
        - drivers: lista ordenada (no máx. limit)
        - methodology: descrição da política e versão
        - integrity: status do check determinístico

    Raises:
        DeterminismError se inputsHash diferir no replay.
    """
    # UC-05 E1 — Falha de Determinismo bloqueia explicação
    is_deterministic, fresh = replay_score(stored_run)
    if not is_deterministic:
        raise DeterminismError(
            run_id=stored_run["result"]["runId"],
            original_hash=stored_run["result"]["inputsHash"],
            replay_hash=fresh["inputsHash"],
        )

    breakdown = stored_run["result"]["breakdown"]

    # REQ-006: ordenar por contribuição ABSOLUTA, descendente
    sorted_drivers = sorted(
        breakdown,
        key=lambda d: abs(d["contribution"]),
        reverse=True,
    )

    # NFR-008: top 5 drivers obrigatórios com labels legíveis
    top_drivers = sorted_drivers[:limit]

    policy_version = stored_run["result"]["policyVersion"]
    policy = get_policy(policy_version)

    return {
        "runId": stored_run["result"]["runId"],
        "applicationId": stored_run["result"]["applicationId"],
        "score": stored_run["result"]["score"],
        "policyVersion": policy_version,
        "policyStatus": policy["status"],     # avisa se DEPRECATED (REQ-007 AC-3)
        "drivers": top_drivers,
        "methodology": (
            f"Continuity Score calculado pela política {policy_version} "
            f"({policy['status']}). Cada driver corresponde a um fator ponderado "
            "do perfil de transição. Drivers ordenados por contribuição absoluta."
        ),
        "integrity": {
            "deterministic": True,
            "inputsHash": stored_run["result"]["inputsHash"],
        },
    }


class DeterminismError(Exception):
    """UC-05 E1 — falha de determinismo (Variant 3)."""
    def __init__(self, run_id: str, original_hash: str, replay_hash: str):
        self.run_id = run_id
        self.original_hash = original_hash
        self.replay_hash = replay_hash
        super().__init__(
            f"Determinism check FAILED for run {run_id}: "
            f"original={original_hash[:12]}... replay={replay_hash[:12]}..."
        )
