Feature: Continuity Score and Explainability for Application Intake
  This feature validates key acceptance behavior for the selected requirements, ensuring determinism and proper score explanation.

  ### REQ links: REQ-002, REQ-006, REQ-009, REQ-010

  Scenario: Happy path — compute score and retrieve top 5 drivers
    Given the active scoring policy is "v1.0.0"
    And the following intake payload with complete readiness factors
    When the Transition Manager submits the payload to POST /continuity-score
    Then the response includes a score between 0 and 100
    And the response includes a "policyVersion" equal to "v1.0.0"
    When the Transition Manager requests GET /explain for the returned runId
    Then the response contains exactly 5 drivers
    And the drivers are ordered by absolute contribution descending

  Scenario: Negative path — payload missing mandatory fields is rejected
    Given the following intake payload is incomplete (missing "responses")
    When the Transition Manager submits the payload to POST /continuity-score
    Then the request is rejected with error code "MISSING_FIELDS"
    And the error response lists "responses" among the missing fields

  @variant @determinism
  Scenario: Determinism — identical features with different metadata produce the same hash
    Given two intake payloads with identical readiness factors
    And the first payload has "application_id" equal to "APP-DET-A"
    And the second payload has "application_id" equal to "APP-DET-B"
    When both payloads are scored under policy "v1.0.0"
    Then both runs produce the same "inputsHash"