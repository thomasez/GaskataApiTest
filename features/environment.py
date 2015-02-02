# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os

# Zato
from zato.apitest.util import new_context

# Behave formatting/pretty printing
import behave.formatter.pretty

import logging

def before_all(context):
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

def before_feature(context, feature):
    environment_dir = os.path.dirname(os.path.realpath(__file__))
    context.zato = new_context(None, environment_dir)

from distutils.util import strtobool as _bool

BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "no"))
PRINT_VERBOSE_OUTPUT = _bool(os.environ.get("PRINT_VERBOSE_OUTPUT", "no"))
PRINT_DOC_ON_PASSED = os.environ.get("PRINT_DOC_ON_PASSED", None)
PRINT_DOC_TO_FILENAME = os.environ.get("PRINT_DOC_TO_FILENAME", None)

# I don't feel like hacking myself into the loggin features. Aka, we just add
# everything to a document string.
# I cannot use the context to store stuff, since that can be cleared..
global documentation
documentation = ''

def after_all(context):
    if PRINT_DOC_ON_PASSED:
        if PRINT_DOC_TO_FILENAME:
            print("Printing docs to file " + PRINT_DOC_TO_FILENAME)
            with open(PRINT_DOC_TO_FILENAME, "w") as docfile:
                docfile.write(documentation)
        else:
            print(documentation)

def add_to_doc(text, type):
    global documentation
    if PRINT_DOC_ON_PASSED == 'trac':
        if type == "h1":
            documentation += '= ' + text + ' =' + '\n'
        if type == "h2":
            documentation += '== ' + text + ' ==' + '\n'
        if type == "h3":
            documentation += '=== ' + text + ' ===' + '\n'
        if type == "code" or type == "javascript":
            documentation += '{{{\n' + text + '\n}}}\n' + '\n'
    elif PRINT_DOC_ON_PASSED == 'html':
        if type == "h1":
            documentation += '<h1>' + text + '</h1>' + '\n'
        if type == "h2":
            documentation += '<h2>' + text + '</h2>' + '\n'
        if type == "h3":
            documentation += '<h3>' + text + '</h3>' + '\n'
        if type == "code" or type == "javascript":
            documentation += '<pre>\n' + text + '</pre>\n'
    # Default, Markdown
    else:
        pass

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        print(u"Request:")
        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=3)
        pp.pprint(context.zato.request)
        print("response:\n")
        try:
            pp.pprint(context.zato.response.data.text)
        except:
            print("No response object")
        print("/ context")
        print("steps:" + str(step.status))
        pp.pprint(step)
        print("/ steps")
        print("debuginfo")
        print(u"DEBUG: %s", context.zato.get('debug_info', 'Nothing'))
        print("/ debuginfo")
        
def after_scenario(context, scenario):
    import pprint
    pp = pprint.PrettyPrinter(indent=4, depth=5)
        
    if BEHAVE_DEBUG_ON_ERROR and scenario.status == "failed":
        print("Failed " + scenario.name)
        print("request:\n")
        pp.pprint(context.zato.request)
        print("response:\n")
        try:
            print(context.log_capture)
            print(context.stdout_capture)
        except:
            pass
        try:
            pp.pprint(context.zato.response)
        except:
            print("No response object")
        print("/ context")
        print("scenario:" + str(scenario.status))
        pp.pprint(scenario)
        print("/ scenario")
        print("debuginfo")
        print("DEBUG:" + str(context.zato.get('debug_info', 'Nothing')))
        print("/ debuginfo")
        
    if PRINT_VERBOSE_OUTPUT and scenario.status == "passed":
        try:
            sys.stdout.write("Request:")
            pp.pprint(context.zato.request)
            sys.stdout.write("Response:")
            pp.pprint(context.zato.response)
        except:
            sys.stdout.write("after_feature:" + "printing debug failed.")
        sys.stdout.write("debuginfo")
        pp.pprint(context.zato.get('debug_info', None))
        sys.stdout.write("/ debuginfo")

    if PRINT_DOC_ON_PASSED and scenario.status == "passed":
        add_to_doc(str(scenario.name), "h1")
        add_to_doc("Request:", "h3")
        code = context.zato.request.get('method', 'GET') + "\n"
        code += context.zato.request.get('url_path', '') + context.zato.request.get('query_string', '') + "\n"
        try:
            code += pp.pformat(context.zato.request.data_impl) + "\n"
        except:
            pass
        add_to_doc(code, "code")
        # Need to put these here, since we might have cleaned up the context..
        try:
            add_to_doc("Response-code:" + str(context.zato.response.data.status_code), "h3")
            import json
            text = json.dumps(context.zato.response.data_impl, indent=4)
            if text:
                add_to_doc("Response-data:", "h3")
                add_to_doc(str(text), "javascript")
            text = pp.pformat(context.zato.response)
        except:
            pass

