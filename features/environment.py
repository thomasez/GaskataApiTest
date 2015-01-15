# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import os
import sys
import pprint

# Zato
from zato.apitest.util import new_context

def before_feature(context, feature):
    environment_dir = os.path.dirname(os.path.realpath(__file__))
    context.zato = new_context(None, environment_dir)

from distutils.util import strtobool as _bool

BEHAVE_DEBUG_ON_ERROR = _bool(os.environ.get("BEHAVE_DEBUG_ON_ERROR", "no"))
PRINT_DOC_ON_PASSED = _bool(os.environ.get("PRINT_DOC_ON_PASSED", "no"))
PRINT_VERBOSE_OUTPUT = _bool(os.environ.get("PRINT_VERBOSE_OUTPUT", "no"))

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        print("Feila!")
        print("request:\n")
        pp = pprint.PrettyPrinter(indent=4, depth=3)
        pp.pprint(context.zato.request)
        print("response:\n")
        try:
            pp.pprint(context.zato.response)
        except:
            print("No response object")
        print("/ context")
        print("steps:" + str(step.status))
        pp.pprint(step)
        print("/ steps")
        print("debuginfo")
        print("DEBUG:" + str(context.zato.get('debug_info', 'Nothing')))
        print("/ debuginfo")
        sys.exit(1)
        
def after_scenario(context, scenario):
    pp = pprint.PrettyPrinter(indent=4, depth=5)
        
    if PRINT_VERBOSE_OUTPUT:
        try:
            print("Request:")
            pp.pprint(context.zato.request.get('method', 'GET'))
            print("Response:")
            pp.pprint(context.zato.response)
        except:
            print("after_feature:" + "printing debug failed.")
        print("debuginfo")
        pp.pprint(context.zato.get('debug_info', None))
        print("/ debuginfo")

    if PRINT_DOC_ON_PASSED:
        import json
        print("= " + str(feature.name) + " =")
        try:
            print("== Example ==")
            print("=== Request: ===")
            print("{{{")
            print(context.zato.request.get('method', 'GET'))
            print(context.zato.request.get('url_path', '') + context.zato.request.get('query_string', ''))
            try:
                pp.pprint(context.zato.request.data_impl)
            except:
                pass
            print("}}}")
            print("=== Response: ===")
            print("{{{")
            print(json.dumps(context.zato.response.data_impl, indent=4))
            print("}}}")
        except:
            print("after_feature:" + "printing docs failed.")

