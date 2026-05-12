"""
Policy Registry (REQ-007) — Variant 3
Gere versões imutáveis de políticas de scoring com checksums SHA-256.
"""
import hashlib
import json
from typing import Dict, Any


# Snapshot imutável das políticas (em produção viria de DB)
# Cada política define os pesos dos fatores que compõem o Continuity Score
POLICIES: Dict[str, Dict[str, Any]] = {
    "v1.0.0": {
        "version": "v1.0.0",
        "status": "active",
        "weights": {
            "documentation_completeness": 0.25,
            "monitoring_coverage": 0.20,
            "dr_bcp_readiness": 0.20,
            "access_management": 0.15,
            "integrations_mapped": 0.10,
            "support_model_defined": 0.10,
        },
        "labels": {
            "documentation_completeness": "Cobertura da documentação",
            "monitoring_coverage": "Cobertura de observabilidade",
            "dr_bcp_readiness": "Prontidão DR/BCP",
            "access_management": "Gestão de acessos (RBAC)",
            "integrations_mapped": "Integrações mapeadas",
            "support_model_defined": "Modelo de suporte definido",
        },
    },
    "v0.9.0": {
        "version": "v0.9.0",
        "status": "deprecated",
        "weights": {
            "documentation_completeness": 0.30,
            "monitoring_coverage": 0.25,
            "dr_bcp_readiness": 0.20,
            "access_management": 0.10,
            "integrations_mapped": 0.10,
            "support_model_defined": 0.05,
        },
        "labels": {
            "documentation_completeness": "Documentação",
            "monitoring_coverage": "Monitorização",
            "dr_bcp_readiness": "DR/BCP",
            "access_management": "Acessos",
            "integrations_mapped": "Integrações",
            "support_model_defined": "Suporte",
        },
    },
}


def get_active_policy() -> Dict[str, Any]:
    """Retorna a política ativa."""
    for pol in POLICIES.values():
        if pol["status"] == "active":
            return pol
    raise RuntimeError("Nenhuma política ativa encontrada")


def get_policy(version: str) -> Dict[str, Any]:
    """Recupera uma política por versão. AC-1: políticas nunca são apagadas."""
    if version not in POLICIES:
        raise ValueError(f"Versão de política desconhecida: {version}")
    return POLICIES[version]


def policy_checksum(version: str) -> str:
    """AC-2: Cada política tem um checksum SHA-256 único e estável."""
    pol = get_policy(version)
    # Serialização canónica para garantir hash determinístico
    canonical = json.dumps(pol["weights"], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def list_policies() -> list:
    """Lista todas as versões com checksum e status."""
    return [
        {
            "version": v,
            "status": p["status"],
            "checksum": policy_checksum(v),
        }
        for v, p in POLICIES.items()
    ]
