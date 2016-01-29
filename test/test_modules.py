# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    Tests of modules
'''
import modules


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
    ui_modules = modules.get_ui_modules(['test'])
