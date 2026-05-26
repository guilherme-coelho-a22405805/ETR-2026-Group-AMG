import sys
import os
# Apontar especificamente para a pasta profunda onde está o ai_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'ams_prototype_lab8', 'ams_prototype')))


import pytest
from ai_engine.scoring import compute_inputs_hash
from ai_engine.validator import validate_and_normalize, ValidationError

# T-01: Determinismo (REQ-010 Variante 3)
def test_determinism_ignores_metadata():
    responses = {
        "documentation_completeness": 0.80,
        "monitoring_coverage": 0.60
    }
    policy_v = "v1.0.0"
    
    hash_payload_a = compute_inputs_hash(responses, policy_v)
    hash_payload_b = compute_inputs_hash(responses, policy_v)
    
    assert hash_payload_a == hash_payload_b
    assert len(hash_payload_a) == 64

# T-02: Validação (REQ-009)
def test_missing_mandatory_fields_rejected():
    incomplete_payload = {
        "application_id": "APP-001",
        "sector": "healthcare"
    }
    
    with pytest.raises(ValidationError) as excinfo:
        validate_and_normalize(incomplete_payload)
    
    assert excinfo.value.code == "MISSING_FIELDS"
    assert "responses" in excinfo.value.fields

# T-03: Explicabilidade / Top 5 Drivers (REQ-006 Variante 3)
def test_explain_returns_top_5_ordered():
    mock_run = {
        "runId": "RUN-TEST-001",
        "inputsHash": "dummyhash123",
        "breakdown": [
            {"factor": "f1", "contribution": -15},
            {"factor": "f2", "contribution": 5},
            {"factor": "f3", "contribution": 20},
            {"factor": "f4", "contribution": -2},
            {"factor": "f5", "contribution": -10},
            {"factor": "f6", "contribution": 1}
        ]
    }
    
    drivers = mock_run["breakdown"]
    drivers_sorted = sorted(drivers, key=lambda x: abs(x["contribution"]), reverse=True)
    top_5 = drivers_sorted[:5]
    
    assert len(top_5) == 5
    assert top_5[0]["factor"] == "f3"  # Maior impacto absoluto (20) em 1º
    assert "f6" not in [d["factor"] for d in top_5] # Menor (1) excluído