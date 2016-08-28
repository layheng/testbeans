from behave import given, when, then
from hamcrest import assert_that, equal_to


@given("I have two integers a and b")
def step_impl(context):
    context.a = 1
    context.b = 2


@when("I add the numbers")
def step_impl(context):
    context.sum = int(context.a) + int(context.b)


@then("I print the addition result")
def step_impl(context):
    context.logger.debug(context.sum)
    assert_that(3, equal_to(context.sum))