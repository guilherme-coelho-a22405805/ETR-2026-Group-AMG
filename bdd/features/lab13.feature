Feature: Continuity Score Computation and Explainability
  This feature validates key acceptance behaviors for the selected requirements.

  # REQ links: REQ-002, REQ-006, REQ-009, REQ-010

  Background:
    Given the active scoring policy is "v1.0.0"

  # REQ-002, REQ-006 — happy path
  Scenario: Happy path — complete payload produces a valid score with top 5 drivers
    Given a complete intake payload for application "APP-LAB13-001" in sector "healthcare"
    When the payload is scored
    Then the score is between 0 and 100
    And the policyVersion in the response is "v1.0.0"
    And the inputsHash in the response is not empty
    And uncertainty_applied is false
    When the explanation is requested for the run
    Then the explanation contains exactly 5 drivers
    And the drivers are ordered by absolute contribution descending
    And every driver has a non-empty label

  # REQ-009 — negative path
  Scenario: Negative path — payload missing responses field is rejected
    Given an incomplete payload without the responses field
    When the payload is submitted for scoring
    Then the submission is rejected with error code "MISSING_FIELDS"
    And "responses" is listed among the missing fields

  # REQ-002 AC-3 — alternative flow
  Scenario: Alternative flow — partial responses trigger uncertainty flag
    Given a partial intake payload for application "APP-LAB13-002" in sector "bfsi"
    And only 2 out of 6 readiness factors are provided
    When the payload is scored
    Then the score is between 0 and 100
    And uncertainty_applied is true
    And the response includes 4 missing optional fields

  # REQ-010 — boundary scenario
  Scenario: Boundary — score of zero when all factors are 0.0
    Given an intake payload for application "APP-LAB13-003" in sector "retail"
    And all readiness factors are set to 0.0
    When the payload is scored
    Then the score is exactly 0
    And uncertainty_applied is false
    And the inputsHash is deterministic across two identical runs
