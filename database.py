# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    The singleton database connection. Every action of database would
    create a new connection if no connection is created before or use the exis-
    ted one.

    Also the decorator catch all raised exception during the connection. Once a
    exception is raised, it logs an error message and sends alert emails to all
    users in the alert list.

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
import email_sender

from tornado.options import options


# TODO: Choose different modules depending on the type of database.
def get_connection(function):
    '''
        The decorator with a singleton connection of database.
    '''
    def wrapper(cls, *args, **kwargs):
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
            return function(cls, connection, *args, **kwargs)
        except Exception, e:
            # Log error
            logging.error(
                (
                    'Mysql Connection Error: '
                    'Occured when class {0} try to build connection'
                ).format(
                    cls.__name__
                )
            )

            # Send alert email
            message = str(e)
            email_sender.async_send(
                title="The Exception Raised",
                message=message
            )

            return None if 'query' not in function.__name__ else []

    return wrapper
