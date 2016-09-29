import time
from behave import given, when, then
from hamcrest import assert_that, equal_to
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pyvirtualdisplay import Display


@given(u'Website2 is accessible')
def step_impl(context):
    context.display = Display(visible=0, size=(1024, 768))
    context.display.start()
    context.driver = webdriver.Firefox()
    url = "https://" + context.server_ip
    context.driver.get(url)
    time.sleep(1)
    context.logger.info(context.driver.title)


@when(u'login with user element and password element')
def step_impl(context):
    signin = context.driver.find_element_by_link_text("Sign In")
    signin.click()
    time.sleep(1)
    context.logger.info(context.driver.title)
    user = context.driver.find_element_by_id("K1")
    user.send_keys(context.username)
    password = context.driver.find_element_by_id("Q1")
    password.send_keys(context.password)
    password.submit()
    time.sleep(1)
    context.logger.info(context.driver.title)
    pvq = context.driver.find_element_by_id("pvqAnswer")
    pvq.send_keys(context.pvq)
    pvq.submit()
    time.sleep(1)
    context.logger.info(context.driver.title)


@then(u'website2 login is successful')
def step_impl(context):
    assert_that(True, equal_to("Accounts" in context.driver.title))
    context.driver.quit()
    context.display.stop()
