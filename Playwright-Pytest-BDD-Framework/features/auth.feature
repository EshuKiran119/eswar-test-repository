@api @auth
Feature: Sample Store session lifecycle
  @smoke
  Scenario: Sign in with a synthetic customer
    Given an anonymous API client
    When the customer signs in with valid demo credentials
    Then the response status is 200
    And a usable session is returned
  @regression
  Scenario: Reject an incorrect password
    Given an anonymous API client
    When the customer signs in with an incorrect password
    Then the response status is 401
    And the error code is "invalid_credentials"
  @regression
  Scenario: Reject a token after sign out
    Given an authenticated API customer
    When the customer signs out and replays the old token
    Then the response status is 401
    And the error code is "unauthorized"
