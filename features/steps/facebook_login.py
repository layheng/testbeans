from behave import given, when, then
from hamcrest import assert_that, is_not
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pyvirtualdisplay import Display
import time


@given(u'Website is accessible')
def step_impl(context):
    context.display = Display(visible=0, size=(1024, 768))
    context.display.start()
    context.driver = webdriver.Firefox()
    url = "https://" + context.server_ip
    context.driver.get(url)
    context.title_logout = context.driver.title


@when(u'login with user element {user} and password element {password}')
def step_impl(context, user, password):
    driver_username = context.driver.find_element_by_id(user)
    driver_password = context.driver.find_element_by_id(password)
    driver_username.send_keys(context.username)
    driver_password.send_keys(context.password)
    time.sleep(0.1)
    driver_password.submit()


@then(u'login is success')
def step_impl(context):
    assert_that(context.driver.title, is_not(context.title_logout))
    context.driver.quit()
    context.display.stop()


@when(u'website login with user element {user} and password element {password}')
def step_impl(context, user, password):
    driver_username = context.driver.find_element_by_id(user)
    driver_password = context.driver.find_element_by_id(password)
    driver_username.send_keys(context.username)
    driver_password.send_keys(context.password)
    time.sleep(0.1)
    driver_password.submit()
