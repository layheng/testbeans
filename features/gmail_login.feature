Feature: Gmail login


  @gmail
  Scenario: Gmail login
    Given Gmail website is accessible
    When entering to Gmail user element Email
    When entering to Gmail password element Passwd
    Then Gmail login is success