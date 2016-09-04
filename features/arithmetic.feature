Feature: Arithmetic

  @sum
  Scenario: Add two numbers
    Given two integers a and b
    When adding the numbers
    Then sum result is valid


  @arithmetic
  Scenario: Multiply two numbers
    Given two integers a and b
    When multiplying the numbers
    Then multiply result is valid


  @arithmetic
  Scenario: Subtract two numbers
    Given two integers a and b
    When a is subtracted from b
    Then subtract result is valid
  