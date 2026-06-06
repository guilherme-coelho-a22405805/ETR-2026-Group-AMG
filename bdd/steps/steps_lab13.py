"""
Step definitions — Lab 13
bdd/steps/steps_lab13.py
"""
import sys
import os
from behave import given, when, then

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs", "ams_prototype_lab8", "ams_prototype")))

from ai_engine.validator import validate_and_normalize, ValidationError
from ai_engine.scoring import calculate_continuity_score
from ai_engine.explain import explain_score

FULL_RESPONSES = {
    "documentation_completeness": 0.80,
    "monitoring_coverage": 0.60,
    "dr_bcp_readiness": 0.70,
    "access_management": 0.90,
    "integrations_mapped": 0.50,
    "support_model_defined": 0.85,
}

PARTIAL_RESPONSES = {
    "documentation_completeness": 0.90,
    "monitoring_coverage": 0.80,
}

ZERO_RESPONSES = {k: 0.0 for k in FULL_RESPONSES}


def _build_stored_run(result, normalized):
    return {
        "runId": result["runId"],
        "inputsHash": result["inputsHash"],
        "policyVersion": result["policyVersion"],
        "normalizedPayload": normalized,
        "result": result,
        "breakdown": result["breakdown"],
    }


@given(u'a complete intake payload for application "{app_id}" in sector "{sector}"')
def step_complete_payload(context, app_id, sector):
    context.raw_payload = {
        "application_id": app_id,
        "sector": sector,
        "responses": FULL_RESPONSES.copy(),
    }

@when(u'the payload is scored')
def step_score_payload(context):
    if not hasattr(context, "storage"):
        context.storage = {}
    normalized, uncertainty = validate_and_normalize(context.raw_payload)
    result = calculate_continuity_score(normalized, uncertainty, context.policy_version)
    context.result = result
    context.normalized = normalized
    context.validation_error = None
    context.storage[result["runId"]] = _build_stored_run(result, normalized)

@then(u'the score is between 0 and 100')
def step_score_range(context):
    assert 0 <= context.result["score"] <= 100

@then(u'the policyVersion in the response is "v1.0.0"')
def step_policy_version(context):
    assert context.result["policyVersion"] == "v1.0.0"

@then(u'the inputsHash in the response is not empty')
def step_hash_not_empty(context):
    assert context.result["inputsHash"] != ""

@then(u'uncertainty_applied is false')
def step_uncertainty_false(context):
    assert context.result["uncertainty_applied"] is False

@then(u'uncertainty_applied is true')
def step_uncertainty_true(context):
    assert context.result["uncertainty_applied"] is True

@when(u'the explanation is requested for the run')
def step_request_explain(context):
    run_id = context.result["runId"]
    stored = context.storage[run_id]
    context.explanation = explain_score(stored)

@then(u'the explanation contains exactly 5 drivers')
def step_five_drivers(context):
    assert len(context.explanation["drivers"]) == 5

@then(u'every driver has a non-empty label')
def step_driver_labels(context):
    for d in context.explanation["drivers"]:
        assert "label" in d and d["label"].strip() != ""


@given(u'an incomplete payload without the responses field')
def step_incomplete_payload(context):
    context.raw_payload = {
        "application_id": "APP-NEG-001",
        "sector": "retail",
    }

@when(u'the payload is submitted for scoring')
def step_submit_invalid(context):
    try:
        validate_and_normalize(context.raw_payload)
        context.validation_error = None
    except ValidationError as e:
        context.validation_error = e

@then(u'the submission is rejected with error code "MISSING_FIELDS"')
def step_rejected_missing(context):
    assert context.validation_error is not None
    assert context.validation_error.code == "MISSING_FIELDS"

@then(u'"{field}" is listed among the missing fields')
def step_field_missing(context, field):
    assert field in context.validation_error.fields


@given(u'a partial intake payload for application "{app_id}" in sector "{sector}"')
def step_partial_payload(context, app_id, sector):
    context.raw_payload = {
        "application_id": app_id,
        "sector": sector,
        "responses": PARTIAL_RESPONSES.copy(),
    }

@given(u'only 2 out of 6 readiness factors are provided')
def step_only_two_factors(context):
    assert len(context.raw_payload["responses"]) == 2

@then(u'the response includes 4 missing optional fields')
def step_four_missing(context):
    assert len(context.result["missingOptionalFields"]) == 4


@given(u'an intake payload for application "{app_id}" in sector "{sector}"')
def step_generic_payload(context, app_id, sector):
    context.raw_payload = {
        "application_id": app_id,
        "sector": sector,
        "responses": {},
    }

@given(u'all readiness factors are set to 0.0')
def step_all_zeros(context):
    context.raw_payload["responses"] = ZERO_RESPONSES.copy()

@then(u'the score is exactly 0')
def step_score_zero(context):
    assert context.result["score"] == 0

@then(u'the inputsHash is deterministic across two identical runs')
def step_hash_deterministic(context):
    normalized2, uncertainty2 = validate_and_normalize(context.raw_payload)
    result2 = calculate_continuity_score(normalized2, uncertainty2, context.policy_version)
    assert context.result["inputsHash"] == result2["inputsHash"]
