# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    The singleton database connection. Every action of database would
    create a new connection if no connection is created before or use the exis-
    ted one.

    To use the connection in the function, you should decorate your function w-
    ith ``get_connection``

    ::

        @classmethod
        @get_connection
        def your_function(cls, connection, *args):
            pass

    .. note::
        The decorated function must be a class method!

    Methods
    ------------------------
'''

import torndb
import logging

from tornado.options import options


# TODO: Choose different modules depending on the type of database.
def get_connection(function):
    '''
        The decorator with a singleton connection of database.
    '''
    def wrapper(cls, *args, **kwargs):
        print options.database_address
        try:
            connection =\
                torndb.Connection(
                    ":".join(
                        [
                            options.database_address,
                            options.database_port,
                        ]
                    ),
                    cls.db,
                    options.database_user,
                    options.database_password,
                )
        except AttributeError:
            logging.error(
                (
                    'Mysql Connection Error: '
                    'Occured when class {0} try to build connection'
                ).format(
                    cls.__name__
                )
            )
            return None if 'query' not in function.__name__ else []
        else:
            logging.debug('Database action succeed!')
            return function(cls, connection, *args, **kwargs)

    return wrapper
