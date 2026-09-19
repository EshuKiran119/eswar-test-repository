@ui
Feature: Sample Store browser journey
  @smoke
  Scenario: Confirm a browser order against the API
    Given the customer is signed in through the browser
    When the customer buys 2 units of "notebook" through the browser
    Then the browser displays an order total of "$25.00"
    And the browser order matches the stored API order
  @regression @auth
  Scenario: Reject invalid browser credentials
    Given the login page is open
    When an incorrect password is submitted through the browser
    Then the browser shows an invalid credentials message
  @regression @auth
  Scenario: Return to login after browser sign out
    Given the customer is signed in through the browser
    When the customer signs out through the browser
    Then the login form is visible
