# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.

Extended by Thomas Lundquist <github at bisonlab.no>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Behave
from behave import given, then

# Zato
from zato.apitest import steps as default_steps
from zato.apitest.steps.json import set_pointer
from zato.apitest.util import obtain_values

@given('Autheticate user without user but with password "{auth_user_password}"')
@obtain_values
def given_authenticate_password_only(context,auth_user_password):
    url = "/aa/auth"
    context.zato.request.query_string = ''
    context.zato.request.url_path = url
    post_data = {'password': auth_user_password}
    context.zato.request.data_impl = post_data
    context.zato.debug_info = post_data

@given('Autheticate user with user ident "{auth_user_ident}" and no password nor token')
@obtain_values
def given_authenticate_user_ident(context,auth_user_ident):
    url = "/aa/auth"
    context.zato.request.query_string = ''
    context.zato.request.url_path = url
    post_data = {'user_ident': auth_user_ident}
    context.zato.request.data_impl = post_data
    context.zato.debug_info = post_data

@given('Autheticate user with user ident "{auth_user_ident}" and password "{auth_user_password}"')
@obtain_values
def given_authenticate_user_ident_password(context,auth_user_ident,auth_user_password):
    url = "/aa/auth"
    context.zato.request.query_string = ''
    context.zato.request.url_path = url
    post_data = {'user_ident': auth_user_ident, 'password': auth_user_password}
    context.zato.request.data_impl = post_data
    context.zato.debug_info = post_data

@given('Autheticate user with email "{auth_user_email}" and password "{auth_user_password}"')
@obtain_values
def given_authenticate_user_email_password(context,auth_user_email,auth_user_password):
    url = "/aa/auth"
    context.zato.request.query_string = ''
    context.zato.request.url_path = url
    post_data = {'email': auth_user_email, 'password': auth_user_password}
    context.zato.request.data_impl = post_data
    context.zato.debug_info = post_data

@then('The text "{text}" is in the response data.')
@obtain_values
def then_text_in_response(context, text):
    import re
    value = context.zato.response.data_impl
    assert text in value, 'Text "`{}`" is not in response.'.format(text)
    return True

@then('The text "{text}" isn\'t in the response data.')
@obtain_values
def then_text_in_response(context, text):
    import re
    value = context.zato.response.data_impl
    assert text not in value, 'Text "`{}`" is in response.'.format(text)

