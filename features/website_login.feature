Feature: Website login

  @facebook
  Scenario: Website login
    Given Website is accessible
    When login with user element email and password element pass
    And submit element login_form
    Then login is success

  @gmail
  Scenario: Gmail login
    Given Gmail website is accessible
    When entering to Gmail user element Email
    When entering to Gmail password element Passwd
    Then login is success
