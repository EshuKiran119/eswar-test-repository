@api @mapping
Feature: Order calculations and ownership
  @smoke
  Scenario Outline: Preserve order data across create and read
    Given an authenticated API customer
    When the customer orders <quantity> units of "<sku>"
    Then the response status is 201
    And the stored order has sku "<sku>", quantity <quantity> and total <total> cents
    Examples:
      | sku      | quantity | total |
      | notebook | 1        | 1250  |
      | notebook | 2        | 2500  |
      | mug      | 3        | 2700  |
  @regression
  Scenario Outline: Reject out-of-range quantities
    Given an authenticated API customer
    When the customer orders <quantity> units of "notebook"
    Then the response status is 400
    And the error code is "invalid_quantity"
    Examples:
      | quantity |
      | 0        |
      | -1       |
      | 11       |
  @regression
  Scenario: Enforce order ownership
    Given an authenticated API customer
    When the customer orders 1 units of "notebook"
    And a different customer requests that order
    Then the response status is 403
    And the error code is "forbidden"
