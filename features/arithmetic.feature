Feature: Arithmetic

  @arithmetic
  Scenario: Multiply two numbers
    Given I have two integers a and b
    When I multiply the numbers
    Then the result is valid


  @arithmetic
  Scenario: Subtract two numbers
    Given I have two integers a and b
    When a is subtract from b
    Then the subtract result is valid
  