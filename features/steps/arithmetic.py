from behave import given, when, then
from hamcrest import assert_that, equal_to


@given(u'two integers a and b')
def step_impl(context):
    context.a = 1
    context.b = 2


@when(u'adding the numbers')
def step_impl(context):
    context.sum = int(context.a) + int(context.b)


@then(u'sum result is valid')
def step_impl(context):
    context.logger.debug(context.sum)
    assert_that(3, equal_to(context.sum))


@when(u'subtracting a from b')
def step_impl(context):
    context.subtract = context.b - context.a


@then(u'subtract result is valid')
def step_impl(context):
    assert_that(1, equal_to(context.subtract))


@ when(u'multiplying the numbers')
def step_impl(context):
    context.multi = context.a * context.b


@ then(u'multiply result is valid')
def step_impl(context):
    assert_that(2, equal_to(context.multi))