# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    Demo class of a persistent object in the model level.

    .. note::
        All methods are required to be classmethod.

    .. note::
        Using ``get`` method, your function name should consists of ``get``, t-
        he same when using ``query`` method.
'''
from database import get_connection


class DemoObject(object):
    '''
        Demo class of a persistent object in the model level.
    '''
    db = 'demo'

    @classmethod
    @get_connection
    def get_object_by_id(cls, connection, object_id):
        sql = 'SELECT * FROM object WHERE object_id = {0}'.format(object_id)
        return connection.get(sql)
