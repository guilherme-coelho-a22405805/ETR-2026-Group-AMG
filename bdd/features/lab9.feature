# REQ links: REQ-002, REQ-006, REQ-009, REQ-010, NFR-006, NFR-008
# Slice: Continuity Score + Explain (UC-02 + UC-05)
# Variant: Group 3 — Determinism + Explainability

Feature: Continuity Score and Explainability for Application Intake
  As a Transition Manager
  I want to compute a deterministic readiness score and inspect its top drivers
  So that I can justify go/no-go decisions with auditable evidence

  Background:
    Given the active scoring policy is "v1.0.0"
    And the storage for ScoringRuns is empty

  # ----------------------------------------------------------------------------
  # Happy path — covers REQ-002, REQ-006, REQ-009, NFR-008
  # ----------------------------------------------------------------------------
  Scenario: Happy path — compute score and retrieve top 5 drivers
    Given the following intake payload:
      | application_id | sector     |
      | APP-HP-001     | healthcare |
    And the following readiness factors:
      | factor                       | value |
      | documentation_completeness   | 0.80  |
      | monitoring_coverage          | 0.60  |
      | dr_bcp_readiness             | 0.70  |
      | access_management            | 0.90  |
      | integrations_mapped          | 0.50  |
      | support_model_defined        | 0.85  |
    When the Transition Manager submits the payload to POST /continuity-score
    Then the response includes a score between 0 and 100
    And the response includes a "policyVersion" equal to "v1.0.0"
    And the response includes a non-empty "inputsHash"
    And the response includes "uncertainty_applied" equal to false
    When the Transition Manager requests GET /explain for the returned runId
    Then the response contains exactly 5 drivers
    And the drivers are ordered by absolute contribution descending
    And every driver has a human-readable label

  # ----------------------------------------------------------------------------
  # Negative path — covers REQ-009, UC-02 Exception E1
  # ----------------------------------------------------------------------------
  Scenario: Negative path — payload missing mandatory fields is rejected
    Given the following intake payload is incomplete:
      | application_id | sector |
      |                | retail |
    When the Transition Manager submits the payload to POST /continuity-score
    Then the request is rejected with error code "MISSING_FIELDS"
    And the error response lists "application_id" among the missing fields
    And the error response lists "responses" among the missing fields
    And no ScoringRun is persisted in storage

  # ----------------------------------------------------------------------------
  # Alternative flow — covers REQ-002 AC-3 (UC-02 A1)
  # ----------------------------------------------------------------------------
  Scenario: Alternative flow — partial responses trigger uncertainty flag
    Given the following intake payload:
      | application_id | sector |
      | APP-ALT-001    | bfsi   |
    And only the following readiness factors are provided:
      | factor                       | value |
      | documentation_completeness   | 0.90  |
      | monitoring_coverage          | 0.80  |
    When the Transition Manager submits the payload to POST /continuity-score
    Then the score is calculated successfully
    And the response includes "uncertainty_applied" equal to true
    And the response includes "missingOptionalFields" with 4 entries
    And the score is strictly lower than the same payload with all factors filled

  # ----------------------------------------------------------------------------
  # Variant scenario — covers REQ-010 + NFR-006 (UC-05 E1)
  # ----------------------------------------------------------------------------
  @variant @determinism
  Scenario: Determinism — identical features with different metadata produce the same hash
    Given two intake payloads with identical readiness factors
    And the first payload has "application_id" equal to "APP-DET-A"
    And the second payload has "application_id" equal to "APP-DET-B"
    When both payloads are scored under policy "v1.0.0"
    Then both runs produce the same "inputsHash"
    And both runs produce the same numerical score
    And both runs are persisted with distinct "runId" values

  @variant @determinism
  Scenario: Determinism — tampering with a stored payload blocks the explanation
    Given a ScoringRun "RUN-1" persisted from a valid payload
    When the stored payload of "RUN-1" is tampered (factor "documentation_completeness" changed from 0.80 to 0.99)
    And the Transition Manager requests GET /explain for "RUN-1"
    Then the request is rejected with error "DeterminismError"
    And the response shows the original hash and the replay hash side by side
    And no driver list is returned
