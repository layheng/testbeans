Feature: Web site

  
  Scenario: Website login
    Given Website is accessible
    When login with user element email and password element pass
    And submit element login_form
    Then login is success