"""
Input Validation & Normalization (REQ-009)
Rejeita campos em falta, normaliza tipos/enums/datas para UTC.
"""
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, List


REQUIRED_FIELDS = [
    "application_id",
    "sector",
    "responses",
]

VALID_SECTORS = {"healthcare", "bfsi", "retail", "other"}

# Campos esperados em "responses" (mapeiam para os weights da política)
EXPECTED_RESPONSE_KEYS = [
    "documentation_completeness",
    "monitoring_coverage",
    "dr_bcp_readiness",
    "access_management",
    "integrations_mapped",
    "support_model_defined",
]


class ValidationError(Exception):
    """Erro de validação — devolve código + lista de campos."""
    def __init__(self, code: str, fields: List[str], message: str = ""):
        self.code = code
        self.fields = fields
        self.message = message or f"{code}: {', '.join(fields)}"
        super().__init__(self.message)


def validate_and_normalize(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """
    Valida e normaliza um payload de Continuity Score.

    Returns:
        (normalized_payload, uncertainty_applied)

    Raises:
        ValidationError(MISSING_FIELDS) se faltarem campos obrigatórios (E1 do UC-02).
        ValidationError(INVALID_SECTOR) se sector for inválido.
    """
    # E1 — campos obrigatórios em falta
    missing = [f for f in REQUIRED_FIELDS if f not in payload or payload[f] in (None, "", {})]
    if missing:
        raise ValidationError("MISSING_FIELDS", missing)

    # Validar sector (enum)
    sector = str(payload["sector"]).lower().strip()
    if sector not in VALID_SECTORS:
        raise ValidationError(
            "INVALID_SECTOR",
            ["sector"],
            f"Sector inválido: {sector}. Permitidos: {sorted(VALID_SECTORS)}",
        )

    # Normalizar responses: valores entre 0.0 e 1.0
    responses_raw = payload["responses"]
    if not isinstance(responses_raw, dict):
        raise ValidationError("INVALID_RESPONSES", ["responses"],
                              "Campo 'responses' deve ser um dicionário")

    responses_norm: Dict[str, float] = {}
    for key in EXPECTED_RESPONSE_KEYS:
        if key in responses_raw and responses_raw[key] is not None:
            val = float(responses_raw[key])
            # Clamp entre 0 e 1
            val = max(0.0, min(1.0, val))
            responses_norm[key] = val

    # AC-3 do REQ-002: se faltarem campos NÃO obrigatórios → uncertainty_applied
    missing_optional = [k for k in EXPECTED_RESPONSE_KEYS if k not in responses_norm]
    uncertainty_applied = len(missing_optional) > 0

    # Para os campos em falta, assume valor 0 (pior caso) → penalização por incerteza
    for key in missing_optional:
        responses_norm[key] = 0.0

    # Normalizar timestamp para UTC (REQ-009)
    if "timestamp" in payload and payload["timestamp"]:
        ts = payload["timestamp"]
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                normalized_ts = dt.astimezone(timezone.utc).isoformat()
            except ValueError:
                raise ValidationError("INVALID_TIMESTAMP", ["timestamp"])
        else:
            normalized_ts = datetime.now(timezone.utc).isoformat()
    else:
        normalized_ts = datetime.now(timezone.utc).isoformat()

    normalized = {
        "application_id": str(payload["application_id"]).strip(),
        "sector": sector,
        "responses": responses_norm,
        "timestamp": normalized_ts,
        "missing_optional_fields": missing_optional,
    }

    return normalized, uncertainty_applied
