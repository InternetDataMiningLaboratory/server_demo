# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    The test module for the test of modules
'''
import tornado.web


class TestModule(tornado.web.UIModule):

    def render(self):
        return 'Hello World'
