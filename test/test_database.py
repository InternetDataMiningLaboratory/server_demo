# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    Test of the function which creates a singleton connection of database.
'''
import mock
import tornado.options
from nose.tools import assert_equal


@mock.patch('logging.error')
@mock.patch('torndb.Connection')
@mock.patch.object(tornado.options, 'options')
@mock.patch('email_sender.async_send')
def test_get_connection(mock_mail, mock_options, mock_connection, mock_error):
    '''
        Test ``database.get_connection`` decorator
    '''
    # If import get_connection before the mock then the options won't be mocked
    from database import get_connection

    class test_c(object):
        '''
            The test class build to mock a persistent object.
        '''

        @classmethod
        @get_connection
        def test_connection(cls, connection):
            '''
                The test function of a normal database action.
            '''
            mock_connection.get()
            return 'test'

        @classmethod
        @get_connection
        def test_query(cls, connection):
            '''
                The test function of a database action which requires a list.
            '''
            return ['test']

    _mock_options(mock_options)

    # If cls.db is None
    result = test_c.test_connection()

    # The return result is None and logs an error
    assert result is None
    mock_error.assert_called_with(
        'Mysql Connection Error: Occured when class test_c try to build con'
        'nection')

    # Or the return result is an empty list if requires a list as return
    result = test_c.test_query()
    assert_equal(result, [])

    # If cls.db is assigned
    test_c.db = 'test'

    # If any exception raised during the action of database
    mock_connection.get.side_effect = Exception('test')
    result = test_c.test_connection()
    mock_mail.assert_called_with(title="The Exception Raised", message='test')

    # Cancel the exception
    mock_connection.get.side_effect = None

    # Return the expect result as set in the mock of connection
    result = test_c.test_connection()
    assert_equal(result, 'test')

    # Or return a expected list
    test_c.db = 'test'
    result = test_c.test_query()
    assert_equal(result, ['test'])


def _mock_options(options):
    '''
        Build a mock object of tornado.options and set database settings
    '''
    options.database_address = 'test'
    options.database_port = 'test'
    options.database_user = 'test'
    options.database_password = 'test'
    return options


class TestModel(object):
    '''
        The base class of all test class to test the persistent objects in the
        model. The class create a mock object of the singleton database connec-
        tion in the ``setUp`` function, which would be inherited by all son
        classes. Then you can use ``self.mock_db`` to replace the connection in
        your database function.

        ::

            class TestPersistentObject(TestModel):
                def test_action(self):
                    # Set the return value
                    self.mock_db.get.return_value = 'test'

                    # Now mock_db is replaced of the connection
                    assert action() == 'test'
    '''

    def setUp(self):
        '''
            Set up a mock object of the singleton database and a mock object of
            options.
        '''
        self.mock_db = mock.Mock()
        patch = mock.patch('torndb.Connection')
        self.mock_connection = patch.start()
        self.mock_connection.return_value = self.mock_db

        patch_options = mock.patch.object(tornado.options, 'options')

        mock_options = patch_options.start()
        _mock_options(mock_options)
