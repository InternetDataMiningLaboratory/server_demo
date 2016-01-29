# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
Set url mapping rules as::

    ('[re_mapping]', handler)
'''
import handler.base
import handler.demo

urls = [
    (r"/", handler.demo.DemoHandler),
    (r".*", handler.base.BaseHandler),
]
