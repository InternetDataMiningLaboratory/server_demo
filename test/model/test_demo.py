# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    The test of ``DemoObject``
'''
from test.test_database import TestModel
from nose.tools import assert_equal


class TestDemoObject(TestModel):
    '''
        The test class of ``DemoObject`` which inherits from ``TestModel``
    '''

    def test_get_object_by_id(self):
        '''
            The test of ``DemoObject.get_object_by_id``
        '''
        from model.demo_action import DemoObject

        # Mock the return value of ``connection.get``
        self.mock_db.get.return_value = 'test'

        # Assert the result
        assert_equal(DemoObject.get_object_by_id(1), 'test')
