"""
Continuity Score Engine (REQ-002, REQ-010)
Variant 3: Determinismo garantido via inputsHash (SHA-256).
"""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

from .policy import get_active_policy, get_policy, policy_checksum


def _canonical_features(responses: Dict[str, float]) -> str:
    """
    Serialização canónica APENAS das features analíticas.
    REQ-010 AC: dois payloads com features idênticas mas metadados diferentes
    devem produzir o mesmo inputsHash.
    """
    return json.dumps(responses, sort_keys=True, separators=(",", ":"))


def compute_inputs_hash(responses: Dict[str, float], policy_version: str) -> str:
    """
    Calcula o inputsHash determinístico para garantir reprodutibilidade (Variant 3).
    Combina features analíticas + versão de política.
    """
    canonical = _canonical_features(responses) + "|" + policy_version
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def calculate_continuity_score(
    normalized_payload: Dict[str, Any],
    uncertainty_applied: bool,
    policy_version: str = None,
) -> Dict[str, Any]:
    """
    Calcula o Continuity Score (0-100).

    REQ-002 AC-1: score deve ser inteiro entre 0 e 100.
    REQ-002 AC-2: resposta deve incluir policyVersion.
    REQ-002 AC-3: flag uncertainty_applied quando há campos opcionais em falta.
    REQ-010: persistir inputsHash para replay determinístico.
    """
    policy = get_active_policy() if policy_version is None else get_policy(policy_version)
    pol_version = policy["version"]
    weights = policy["weights"]
    labels = policy["labels"]

    responses = normalized_payload["responses"]

    # Calcular contribuição de cada fator (peso * valor normalizado * 100)
    breakdown = []
    raw_score = 0.0
    for factor, weight in weights.items():
        value = responses.get(factor, 0.0)
        contribution = weight * value * 100  # contribuição em pontos do score (0-100)
        raw_score += contribution
        breakdown.append({
            "factor": factor,
            "label": labels[factor],
            "value": round(value, 4),
            "weight": weight,
            "contribution": round(contribution, 4),
        })

    # AC-1: arredondar para inteiro, clamp [0, 100]
    final_score = int(round(max(0.0, min(100.0, raw_score))))

    # Calcular inputsHash determinístico (REQ-010)
    inputs_hash = compute_inputs_hash(responses, pol_version)

    result = {
        "runId": str(uuid.uuid4()),
        "applicationId": normalized_payload["application_id"],
        "score": final_score,
        "policyVersion": pol_version,             # REQ-002 AC-2
        "policyChecksum": policy_checksum(pol_version),
        "inputsHash": inputs_hash,                # REQ-010
        "breakdown": breakdown,
        "uncertainty_applied": uncertainty_applied,  # REQ-002 AC-3
        "missingOptionalFields": normalized_payload.get("missing_optional_fields", []),
        "computedAt": datetime.now(timezone.utc).isoformat(),
    }
    return result


def replay_score(stored_run: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    REQ-010 / NFR-006: re-executa o cálculo a partir do payload original
    e verifica que o output é matematicamente idêntico (100% determinismo).

    Returns:
        (is_deterministic, fresh_result)
    """
    original_payload = stored_run["normalizedPayload"]
    uncertainty = stored_run["result"]["uncertainty_applied"]
    pol_version = stored_run["result"]["policyVersion"]

    fresh = calculate_continuity_score(original_payload, uncertainty, pol_version)

    # Comparar hashes — REQ-010 AC: "validado por comparação de hash"
    is_deterministic = (
        fresh["inputsHash"] == stored_run["result"]["inputsHash"]
        and fresh["score"] == stored_run["result"]["score"]
    )
    return is_deterministic, fresh
