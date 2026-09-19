Feature: Fictional Sample Store performance contract
  # Design specification. The suite flag selects the matching k6/JMeter workload.
  Scenario: Login feature
    Given one synthetic identity per virtual user
    When the login suite runs
    Then every response contains a usable session and the expected username
    And each session is invalidated outside business timing
  Scenario: Catalog feature
    Given an authenticated synthetic user
    When the catalog suite runs
    Then the product contract is correct and the journey budget is met
  Scenario: Integrated checkout
    Given a synthetic user and the notebook product
    When two notebooks are ordered and read back
    Then the stored total is 2500 cents and belongs to that user
    And test-owned orders and sessions are cleaned up
