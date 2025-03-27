Feature: User API Tests
  Background:
    * url 'https://reqres.in/api'

  Scenario: Get all users
    Given path '/users'
    When method get
    Then status 200
    And match response.data[0] == { "id": 1, "email": "#notnull" }
