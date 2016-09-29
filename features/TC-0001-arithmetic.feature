Feature: TC-0001 Arithmetic


  @arithmetic
  Scenario: TC-0001.01 Add two numbers
    Given two integers a and b
    When adding the numbers
    Then sum result is valid


  @arithmetic
  Scenario: TC-0001.02 Subtract two numbers
    Given two integers a and b
    When subtracting a from b
    Then subtract result is valid


  @arithmetic
  Scenario: TC-0001.03 Multiply two numbers
    Given two integers a and b
    When multiplying the numbers
    Then multiply result is valid