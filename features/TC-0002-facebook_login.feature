Feature: TC-0002 Facebook login


  @facebook
  Scenario: TC-0002 Facebook login
    Given Website is accessible
    When login with user element email and password element pass
    Then login is success
