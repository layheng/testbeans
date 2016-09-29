Feature: TC-0003 Gmail login


  @gmail
  Scenario: TC-0003 Gmail login
    Given Gmail website is accessible
    When entering to Gmail user element Email
    When entering to Gmail password element Passwd
    Then Gmail login is success