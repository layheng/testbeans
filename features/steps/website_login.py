from behave import *
from selenium import webdriver
from hamcrest import *


@given(u'Website is accessible')
def step_impl(context):
    url = "https://" + context.server_ip
    context.driver.get(url)
    context.title_logout = context.driver.title


@when(u'login with user element {user} and password element {password}')
def step_impl(context, user, password):
    driver_username = context.driver.find_element_by_id(user)
    driver_password = context.driver.find_element_by_id(password)
    driver_username.send_keys(context.username)
    driver_password.send_keys(context.password)


@when(u'submit element {login}')
def step_impl(context, login):
    driver_login = context.driver.find_element_by_id(login)
    driver_login.submit()


@then(u'login is success')
def step_impl(context):
    title_login = context.driver.title
    assert_that(title_login, is_not(context.title_logout))
