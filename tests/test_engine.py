import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'ams_prototype_lab8', 'ams_prototype')))

import pytest
from ai_engine.scoring import compute_inputs_hash, calculate_continuity_score
from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.explain import explain_score, DeterminismError
from ai_engine.policy import policy_checksum, get_policy

def test_determinism_ignores_metadata():
    responses = {"documentation_completeness": 0.80, "monitoring_coverage": 0.60}
    policy_v = "v1.0.0"
    hash_payload_a = compute_inputs_hash(responses, policy_v)
    hash_payload_b = compute_inputs_hash(responses, policy_v)
    assert hash_payload_a == hash_payload_b
    assert len(hash_payload_a) == 64

def test_missing_mandatory_fields_rejected():
    incomplete_payload = {"application_id": "APP-001", "sector": "healthcare"}
    with pytest.raises(ValidationError) as excinfo:
        validate_and_normalize(incomplete_payload)
    assert excinfo.value.code == "MISSING_FIELDS"
    assert "responses" in excinfo.value.fields

def test_explain_returns_top_5_ordered():
    # GROOMED (Lab 14): chama explain_score() do motor real em vez de re-implementar
    # a ordenacao numa lista local. Assim o teste falha se o codigo de producao partir.
    payload = {
        "application_id": "APP-UT03",
        "sector": "healthcare",
        "responses": {
            "documentation_completeness": 0.80,
            "monitoring_coverage": 0.60,
            "dr_bcp_readiness": 0.70,
            "access_management": 0.90,
            "integrations_mapped": 0.50,
            "support_model_defined": 0.85,
        },
    }
    normalized, uncertainty = validate_and_normalize(payload)
    result = calculate_continuity_score(normalized, uncertainty, "v1.0.0")
    stored_run = {
        "runId": result["runId"],
        "inputsHash": result["inputsHash"],
        "policyVersion": result["policyVersion"],
        "normalizedPayload": normalized,
        "result": result,
        "breakdown": result["breakdown"],
    }

    explanation = explain_score(stored_run, limit=5)
    drivers = explanation["drivers"]

    assert len(drivers) == 5
    contribs = [abs(d["contribution"]) for d in drivers]
    assert contribs == sorted(contribs, reverse=True)
    assert all(d.get("label", "").strip() for d in drivers)

def test_invalid_sector_rejected():
    payload_invalido = {"application_id": "APP-002", "sector": "aerospace",
        "responses": {"documentation_completeness": 0.5}}
    with pytest.raises(ValidationError) as excinfo:
        validate_and_normalize(payload_invalido)
    assert excinfo.value.code == "INVALID_SECTOR"
    assert "sector" in excinfo.value.fields

def test_boundary_clamp_min_max():
    payload_limites = {"application_id": "APP-BOUND", "sector": "healthcare",
        "responses": {"documentation_completeness": 1.5, "monitoring_coverage": -0.2}}
    norm_payload, uncertainty = validate_and_normalize(payload_limites)
    assert norm_payload["responses"]["documentation_completeness"] == 1.0
    assert norm_payload["responses"]["monitoring_coverage"] == 0.0

def test_explain_blocks_tampered_payload():
    tampered_run = {
        "runId": "RUN-TAMPERED-001", "inputsHash": "hash_original_valido_123",
        "policyVersion": "v1.0.0",
        "normalizedPayload": {"application_id": "APP-003", "sector": "retail",
            "responses": {"documentation_completeness": 0.99}},
        "result": {"uncertainty_applied": False, "policyVersion": "v1.0.0",
            "inputsHash": "hash_original_valido_123"},
        "breakdown": []
    }
    with pytest.raises(DeterminismError) as excinfo:
        explain_score(tampered_run)
    assert excinfo.value.run_id == "RUN-TAMPERED-001"

def test_policy_checksum_uniqueness():
    checksum1 = policy_checksum("v1.0.0")
    checksum2 = policy_checksum("v1.0.0")
    assert checksum1 == checksum2
    assert len(checksum1) == 64
    with pytest.raises(ValueError):
        get_policy("v9.9.9")

def test_missing_optional_trigger_uncertainty():
    payload_parcial = {"application_id": "APP-ALT-001", "sector": "bfsi",
        "responses": {"documentation_completeness": 0.90, "monitoring_coverage": 0.80}}
    norm_payload, uncertainty = validate_and_normalize(payload_parcial)
    assert uncertainty is True
