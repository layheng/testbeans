Feature: TC-0005 website3 login


  @web3
  Scenario: TC-0005 website3 login
    Given Website is accessible
    When website login with user element username and password element password
    Then login is success