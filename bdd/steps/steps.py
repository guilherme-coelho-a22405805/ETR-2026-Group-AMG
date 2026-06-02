"""
Step definitions BDD — behave
Cobre lab9.feature e lab11.feature completos.
"""
import sys
import os
import pytest
from behave import given, when, then

from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.scoring import calculate_continuity_score
from ai_engine.explain import explain_score, DeterminismError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_stored_run(result: dict, normalized_payload: dict) -> dict:
    return {
        "runId": result["runId"],
        "inputsHash": result["inputsHash"],
        "policyVersion": result["policyVersion"],
        "normalizedPayload": normalized_payload,
        "result": result,
        "breakdown": result["breakdown"],
    }

FULL_RESPONSES = {
    "documentation_completeness": 0.80,
    "monitoring_coverage": 0.60,
    "dr_bcp_readiness": 0.70,
    "access_management": 0.90,
    "integrations_mapped": 0.50,
    "support_model_defined": 0.85,
}


# ---------------------------------------------------------------------------
# Background / setup
# ---------------------------------------------------------------------------

@given(u'the active scoring policy is "v1.0.0"')
def step_active_policy(context):
    context.policy_version = "v1.0.0"

@given(u'the storage for ScoringRuns is empty')
def step_storage_empty(context):
    context.storage = {}


# ---------------------------------------------------------------------------
# Happy path — lab11.feature
# ---------------------------------------------------------------------------

@given(u'the following intake payload with complete readiness factors')
def step_complete_payload_lab11(context):
    context.raw_payload = {
        "application_id": "APP-HP-001",
        "sector": "healthcare",
        "responses": FULL_RESPONSES.copy(),
    }

# ---------------------------------------------------------------------------
# Happy path — lab9.feature (tabelas)
# ---------------------------------------------------------------------------

@given(u'the following intake payload:')
def step_intake_payload_table(context):
    row = context.table[0]
    context.raw_payload = {
        "application_id": row["application_id"],
        "sector": row["sector"],
        "responses": {},
    }

@given(u'the following readiness factors:')
def step_readiness_factors_table(context):
    for row in context.table:
        context.raw_payload["responses"][row["factor"]] = float(row["value"])

@given(u'only the following readiness factors are provided:')
def step_partial_factors_table(context):
    context.raw_payload["responses"] = {}
    for row in context.table:
        context.raw_payload["responses"][row["factor"]] = float(row["value"])


# ---------------------------------------------------------------------------
# When — submeter payload
# ---------------------------------------------------------------------------

@when(u'the Transition Manager submits the payload to POST /continuity-score')
def step_submit_payload(context):
    try:
        normalized, uncertainty = validate_and_normalize(context.raw_payload)
        result = calculate_continuity_score(normalized, uncertainty, "v1.0.0")
        context.result = result
        context.normalized = normalized
        context.uncertainty = uncertainty
        context.validation_error = None
        # guardar no storage simulado (inicializar se o Background não o fez)
        if not hasattr(context, "storage"):
            context.storage = {}
        run_id = result["runId"]
        context.storage[run_id] = _build_stored_run(result, normalized)
    except ValidationError as e:
        context.validation_error = e
        context.result = None


# ---------------------------------------------------------------------------
# Then — score e policyVersion
# ---------------------------------------------------------------------------

@then(u'the response includes a score between 0 and 100')
def step_score_range(context):
    assert context.result is not None
    assert 0 <= context.result["score"] <= 100

@then(u'the response includes a "policyVersion" equal to "v1.0.0"')
def step_policy_version(context):
    assert context.result["policyVersion"] == "v1.0.0"

@then(u'the response includes a non-empty "inputsHash"')
def step_inputs_hash(context):
    assert context.result["inputsHash"] != ""

@then(u'the response includes "uncertainty_applied" equal to false')
def step_uncertainty_false(context):
    assert context.result["uncertainty_applied"] is False

@then(u'the response includes "uncertainty_applied" equal to true')
def step_uncertainty_true(context):
    assert context.result["uncertainty_applied"] is True

@then(u'the response includes "missingOptionalFields" with 4 entries')
def step_missing_optional(context):
    assert len(context.result["missingOptionalFields"]) == 4

@then(u'the score is calculated successfully')
def step_score_success(context):
    assert context.result is not None
    assert 0 <= context.result["score"] <= 100

@then(u'the score is strictly lower than the same payload with all factors filled')
def step_score_lower(context):
    full_payload = {
        "application_id": context.raw_payload["application_id"],
        "sector": context.raw_payload["sector"],
        "responses": FULL_RESPONSES.copy(),
    }
    norm_full, unc_full = validate_and_normalize(full_payload)
    result_full = calculate_continuity_score(norm_full, unc_full, "v1.0.0")
    assert context.result["score"] < result_full["score"]


# ---------------------------------------------------------------------------
# When/Then — explain
# ---------------------------------------------------------------------------

@when(u'the Transition Manager requests GET /explain for the returned runId')
def step_explain(context):
    run_id = context.result["runId"]
    stored_run = context.storage[run_id]
    context.explanation = explain_score(stored_run)

@then(u'the response contains exactly 5 drivers')
def step_five_drivers(context):
    assert len(context.explanation["drivers"]) == 5

@then(u'the drivers are ordered by absolute contribution descending')
def step_drivers_ordered(context):
    contribs = [abs(d["contribution"]) for d in context.explanation["drivers"]]
    assert contribs == sorted(contribs, reverse=True)

@then(u'every driver has a human-readable label')
def step_drivers_labels(context):
    for d in context.explanation["drivers"]:
        assert "label" in d and d["label"] != ""


# ---------------------------------------------------------------------------
# Negative path
# ---------------------------------------------------------------------------

@given(u'the following intake payload is incomplete (missing "responses")')
def step_incomplete_lab11(context):
    context.raw_payload = {
        "application_id": "",
        "sector": "retail",
    }

@given(u'the following intake payload is incomplete:')
def step_incomplete_table(context):
    row = context.table[0]
    context.raw_payload = {
        "application_id": row["application_id"],
        "sector": row["sector"],
    }

@then(u'the request is rejected with error code "MISSING_FIELDS"')
def step_missing_fields_error(context):
    assert context.validation_error is not None
    assert context.validation_error.code == "MISSING_FIELDS"

@then(u'the error response lists "responses" among the missing fields')
def step_responses_missing(context):
    assert "responses" in context.validation_error.fields

@then(u'the error response lists "application_id" among the missing fields')
def step_app_id_missing(context):
    assert "application_id" in context.validation_error.fields

@then(u'no ScoringRun is persisted in storage')
def step_no_storage(context):
    assert context.result is None


# ---------------------------------------------------------------------------
# Determinism — mesmo hash, scores iguais, runIds distintos
# ---------------------------------------------------------------------------

@given(u'two intake payloads with identical readiness factors')
def step_two_payloads(context):
    context.payload_a = {"sector": "healthcare", "responses": FULL_RESPONSES.copy()}
    context.payload_b = {"sector": "healthcare", "responses": FULL_RESPONSES.copy()}

@given(u'the first payload has "application_id" equal to "APP-DET-A"')
def step_payload_a_id(context):
    context.payload_a["application_id"] = "APP-DET-A"

@given(u'the second payload has "application_id" equal to "APP-DET-B"')
def step_payload_b_id(context):
    context.payload_b["application_id"] = "APP-DET-B"

@when(u'both payloads are scored under policy "v1.0.0"')
def step_score_both(context):
    norm_a, unc_a = validate_and_normalize(context.payload_a)
    norm_b, unc_b = validate_and_normalize(context.payload_b)
    context.result_a = calculate_continuity_score(norm_a, unc_a, "v1.0.0")
    context.result_b = calculate_continuity_score(norm_b, unc_b, "v1.0.0")

@then(u'both runs produce the same "inputsHash"')
def step_same_hash(context):
    assert context.result_a["inputsHash"] == context.result_b["inputsHash"]

@then(u'both runs produce the same numerical score')
def step_same_score(context):
    assert context.result_a["score"] == context.result_b["score"]

@then(u'both runs are persisted with distinct "runId" values')
def step_distinct_run_ids(context):
    assert context.result_a["runId"] != context.result_b["runId"]


# ---------------------------------------------------------------------------
# Determinism — payload adulterado bloqueia explain (lab9.feature)
# ---------------------------------------------------------------------------

@given(u'a ScoringRun "RUN-1" persisted from a valid payload')
def step_valid_run(context):
    payload = {
        "application_id": "APP-003",
        "sector": "healthcare",
        "responses": FULL_RESPONSES.copy(),
    }
    normalized, uncertainty = validate_and_normalize(payload)
    result = calculate_continuity_score(normalized, uncertainty, "v1.0.0")
    stored = _build_stored_run(result, normalized)
    context.storage["RUN-1"] = stored

@when(u'the stored payload of "RUN-1" is tampered (factor "documentation_completeness" changed from 0.80 to 0.99)')
def step_tamper_payload(context):
    context.storage["RUN-1"]["normalizedPayload"]["responses"]["documentation_completeness"] = 0.99

@when(u'the Transition Manager requests GET /explain for "RUN-1"')
def step_explain_run1(context):
    try:
        explain_score(context.storage["RUN-1"])
        context.determinism_error = None
    except DeterminismError as e:
        context.determinism_error = e

@then(u'the request is rejected with error "DeterminismError"')
def step_determinism_error(context):
    assert context.determinism_error is not None

@then(u'the response shows the original hash and the replay hash side by side')
def step_hashes_side_by_side(context):
    e = context.determinism_error
    assert e.original_hash is not None
    assert e.replay_hash is not None
    assert e.original_hash != e.replay_hash

@then(u'no driver list is returned')
def step_no_drivers(context):
    assert context.determinism_error is not None