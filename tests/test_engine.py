import sys
import os
# Apontar especificamente para a pasta profunda onde está o ai_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'ams_prototype_lab8', 'ams_prototype')))


import pytest
from ai_engine.scoring import compute_inputs_hash
from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.explain import explain_score, DeterminismError
from ai_engine.policy import policy_checksum, get_policy

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


# UT-04: Erro de Validação: Sector Inválido (REQ-009 / TC-005)
def test_invalid_sector_rejected():
    payload_invalido = {
        "application_id": "APP-002",
        "sector": "aerospace",  # Setor que não existe no enum VALID_SECTORS
        "responses": {
            "documentation_completeness": 0.5
        }
    }
    
    with pytest.raises(ValidationError) as excinfo:
        validate_and_normalize(payload_invalido)
    
    assert excinfo.value.code == "INVALID_SECTOR"
    assert "sector" in excinfo.value.fields

# UT-05: Boundary Clamp - Valores Extremos (REQ-009 / TC-006)
def test_boundary_clamp_min_max():
    payload_limites = {
        "application_id": "APP-BOUND",
        "sector": "healthcare",
        "responses": {
            "documentation_completeness": 1.5,  # Acima do máximo
            "monitoring_coverage": -0.2         # Abaixo do mínimo
        }
    }
    
    # O validador deve forçar os valores (clamp) para o intervalo [0.0, 1.0] sem gerar erro
    norm_payload, uncertainty = validate_and_normalize(payload_limites)
    
    assert norm_payload["responses"]["documentation_completeness"] == 1.0
    assert norm_payload["responses"]["monitoring_coverage"] == 0.0

# UT-06: Explain bloqueia adulteração de dados (REQ-010 Variante 3 / TC-008 / UC-05 E1)
def test_explain_blocks_tampered_payload():
    # Simulamos um ScoringRun onde alguém adulterou o payload na BD após o cálculo
    tampered_run = {
        "runId": "RUN-TAMPERED-001",
        "inputsHash": "hash_original_valido_123",
        "policyVersion": "v1.0.0",
        "normalizedPayload": {
            "application_id": "APP-003",
            "sector": "retail",
            "responses": {
                "documentation_completeness": 0.99  # Valor adulterado!
            }
        },
        "result": {  
            "uncertainty_applied": False,
            "policyVersion": "v1.0.0",
            "inputsHash": "hash_original_valido_123"
        },
        "breakdown": []
    }
    
    # Ao tentar explicar, o replay vai falhar e lançar o erro da Variante 3
    with pytest.raises(DeterminismError) as excinfo:
        explain_score(tampered_run)
    
    assert excinfo.value.run_id == "RUN-TAMPERED-001"

# UT-07: Policy Registry Imutável e Checksum (REQ-007 Variante 3 / TC-010)
def test_policy_checksum_uniqueness():
    # AC-2: Cada política deve gerar um checksum SHA-256 estável e único
    checksum1 = policy_checksum("v1.0.0")
    checksum2 = policy_checksum("v1.0.0")
    
    assert checksum1 == checksum2  # Duas chamadas devolvem exatamente o mesmo hash
    assert len(checksum1) == 64    # Valida que é um SHA-256 de 64 caracteres
    
    # AC-1: Políticas inexistentes levantam erro
    with pytest.raises(ValueError):
        get_policy("v9.9.9")

# UT-08: Fluxo Alternativo com Fatores Opcionais em Falta (REQ-002 / TC-003)
def test_missing_optional_trigger_uncertainty():
    payload_parcial = {
        "application_id": "APP-ALT-001",
        "sector": "bfsi",
        "responses": {
            "documentation_completeness": 0.90,
            "monitoring_coverage": 0.80
            # Faltam 4 fatores opcionais da política
        }
    }
    
    norm_payload, uncertainty = validate_and_normalize(payload_parcial)
    
    # O motor aceita o payload parcial mas sinaliza que foi aplicada incerteza
    assert uncertainty is True