from behave import when, then
from hamcrest import assert_that, equal_to


@when(u'I multiply the numbers')
def step_impl(context):
    context.multi = context.a * context.b


@then(u'the result is valid')
def step_impl(context):
    assert_that(2, equal_to(context.multi))

@when(u'a is subtract from b')
def step_impl(context):
    context.subtract = context.b - context.a

@then(u'the subtract result is valid')
def step_impl(context):
    assert_that(1, equal_to(context.subtract))
