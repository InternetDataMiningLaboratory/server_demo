# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    Tests of modules
'''
import modules
from module.test import TestModule
from nose.tools import assert_equal


def test_name_rule_translation():
    '''
        Test ``modules.name_rule_translation``
    '''
    assert 'TestTest' == modules.name_rule_translation('test_test')
    assert 'Test' == modules.name_rule_translation('test')


def test_get_ui_modules():
    '''
        Test ``modules.get_ui_modules``
    '''
    assert_equal(modules.get_ui_modules(['test']), {'test':TestModule})
