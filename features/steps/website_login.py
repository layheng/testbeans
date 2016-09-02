from behave import *
from selenium import webdriver
from hamcrest import *


@given(u'Website is accessible')
def step_impl(context):
    url = "https://" + context.server_ip
    context.driver.get(url)


@when(u'login with user element {user} and password element {password}')
def step_impl(context, user, password):
    username = context.driver.find_element_by_id(user)
    password = context.driver.find_element_by_id(password)
    username.send_keys(context.username)
    password.send_keys(context.password)


@when(u'submit element {login}')
def step_impl(context, login):
    login = context.driver.find_element_by_id(login)
    login.submit()


@then(u'login is success')
def step_impl(context):
    pass

