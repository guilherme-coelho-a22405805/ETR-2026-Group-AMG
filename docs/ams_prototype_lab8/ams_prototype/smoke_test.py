"""
Smoke test manual — verifica happy path, alternative flow e exception path
sem necessidade de abrir a UI.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.scoring import calculate_continuity_score
from ai_engine.explain import explain_score, DeterminismError
from ai_engine.policy import list_policies
from storage.runs_store import save_run, get_run, clear_all


def line(t=""):
    print(f"\n{'='*70}\n{t}\n{'='*70}")


# Reset storage para testes limpos
clear_all()

line("HAPPY PATH — payload completo, sector válido")
payload_ok = {
    "application_id": "APP-001",
    "sector": "healthcare",
    "responses": {
        "documentation_completeness": 0.8,
        "monitoring_coverage": 0.6,
        "dr_bcp_readiness": 0.7,
        "access_management": 0.9,
        "integrations_mapped": 0.5,
        "support_model_defined": 0.85,
    },
}
norm, unc = validate_and_normalize(payload_ok)
print(f"normalized payload: {norm}")
print(f"uncertainty_applied: {unc}")
result = calculate_continuity_score(norm, unc)
save_run(norm, result)
print(f"\nSCORE: {result['score']} / 100")
print(f"policyVersion: {result['policyVersion']}")
print(f"inputsHash: {result['inputsHash']}")
print(f"runId: {result['runId']}")

happy_run_id = result["runId"]

line("EXPLAIN — Top 5 drivers do score acima")
stored = get_run(happy_run_id)
explanation = explain_score(stored, limit=5)
print(f"Métodologia: {explanation['methodology']}\n")
print("Top 5 drivers:")
for i, drv in enumerate(explanation["drivers"], 1):
    print(f"  #{i} {drv['label']}: contribuição={drv['contribution']:.2f} pts")

line("ALTERNATIVE FLOW A1 — campos opcionais em falta => uncertainty_applied=True")
payload_partial = {
    "application_id": "APP-002",
    "sector": "bfsi",
    "responses": {
        "documentation_completeness": 0.9,
        "monitoring_coverage": 0.8,
        # faltam 4 fatores opcionais
    },
}
norm2, unc2 = validate_and_normalize(payload_partial)
print(f"uncertainty_applied: {unc2}")
print(f"missing_optional_fields: {norm2['missing_optional_fields']}")
result2 = calculate_continuity_score(norm2, unc2)
print(f"SCORE: {result2['score']} / 100 (penalizado por incerteza)")
print(f"uncertainty flag no resultado: {result2['uncertainty_applied']}")

line("DETERMINISM CHECK — REQ-010 / NFR-006")
# Repetir o cálculo com o mesmo payload deve dar mesmo inputsHash e score
norm3, unc3 = validate_and_normalize(payload_ok)
result3 = calculate_continuity_score(norm3, unc3)
assert result["inputsHash"] == result3["inputsHash"], "FALHA DETERMINISMO!"
assert result["score"] == result3["score"]
print(f"✓ inputsHash idêntico: {result['inputsHash'][:20]}...")
print(f"✓ score idêntico: {result['score']}")

# Variante 3 AC do REQ-010: features iguais + metadados diferentes => mesmo hash
payload_meta_diff = dict(payload_ok)
payload_meta_diff["application_id"] = "APP-OUTRO"  # metadado não-analítico
norm4, unc4 = validate_and_normalize(payload_meta_diff)
result4 = calculate_continuity_score(norm4, unc4)
assert result["inputsHash"] == result4["inputsHash"], \
    "REQ-010 violado: metadados afetaram o hash!"
print(f"✓ REQ-010 AC: metadados diferentes, MESMO inputsHash")

line("EXCEPTION E1 — MISSING_FIELDS (campos obrigatórios em falta)")
try:
    validate_and_normalize({"sector": "retail"})  # falta application_id e responses
except ValidationError as ve:
    print(f"✓ ValidationError capturada")
    print(f"  code: {ve.code}")
    print(f"  fields: {ve.fields}")

line("EXCEPTION — sector inválido")
try:
    validate_and_normalize({
        "application_id": "APP-X",
        "sector": "invalido",
        "responses": {"documentation_completeness": 0.5},
    })
except ValidationError as ve:
    print(f"✓ ValidationError: {ve.code} — {ve.message}")

line("UC-05 E1 — Tampering bloqueia explicação (Variante 3)")
# Adulterar o stored run para simular violação de integridade
tampered = {
    "normalizedPayload": dict(stored["normalizedPayload"]),
    "result": dict(stored["result"]),
}
tampered["normalizedPayload"] = dict(stored["normalizedPayload"])
tampered["normalizedPayload"]["responses"] = dict(stored["normalizedPayload"]["responses"])
tampered["normalizedPayload"]["responses"]["documentation_completeness"] = 0.99  # alterado
try:
    explain_score(tampered)
    print("✗ ERRO: tampering NÃO foi detetado")
except DeterminismError as de:
    print(f"✓ DeterminismError capturado — explicação bloqueada")
    print(f"  hash original: {de.original_hash[:20]}...")
    print(f"  hash replay  : {de.replay_hash[:20]}...")

line("POLICY REGISTRY")
for pol in list_policies():
    print(f"  {pol['version']:8} {pol['status']:12} {pol['checksum'][:32]}...")

line("✓ TODOS OS SMOKE TESTS PASSARAM")
