Feature: TC-0002 Facebook login


  @web
  Scenario: TC-0002 Facebook login
    Given Website is accessible
    When login with user element email and password element pass
    And submit element login_form
    Then login is success
