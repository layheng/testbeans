from behave import given, when, then
from hamcrest import assert_that, is_not
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pyvirtualdisplay import Display


@given(u'Gmail website is accessible')
def step_impl(context):
    context.display = Display(visible=0, size=(1024, 768))
    context.display.start()
    context.driver = webdriver.Firefox()
    url = "https://" + context.server_ip + "/gmail"
    context.driver.get(url)
    context.title_logout = context.driver.title


@when(u'entering to Gmail user element {user}')
def step_impl(context, user):
    driver_username = context.driver.find_element_by_id(user)
    driver_next = context.driver.find_element_by_id("next")
    driver_username.send_keys(context.username)
    driver_next.click()


@when(u'entering to Gmail password element {password}')
def step_impl(context, password):
    driver_password = context.driver.find_element_by_id(password)
    driver_sing_in = context.driver.find_element_by_id("signIn")
    driver_password.send_keys(context.password)
    driver_sing_in.click()
    try:
        WebDriverWait(context.driver, 10).until(ec.title_contains("Inbox"))
        context.logger.info(context.driver.title)
    except Exception as error:
        context.logger.info(error)


@then(u'Gmail login is success')
def step_impl(context):
    assert_that(context.driver.title, is_not(context.title_logout))
    context.driver.quit()
    context.display.stop()
