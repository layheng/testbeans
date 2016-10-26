Feature: TC-0004 Website2 login


  @web2
  Scenario: TC-0004 Website2 login
    Given Website2 is accessible
    When login with user element and password element
    Then website2 login is successful