# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
'''
    The basic async tests in a async server.

    Test Async
    --------------------------------------------
    Run all async tests in a async server.

    Cases
    --------------------------------------------

'''
import threading

import handler.base
import os
import modules

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.testing import bind_unused_port
from tornado.web import Application
from nose.tools import assert_equal


class LoadingModuleHandler(handler.base.BaseHandler):
    def get(self):
        # Render the shown page
        self.render(
            'loading_test.html',
        )


class TestServerAsync(object):
    '''
        Async server for running async tests.
    '''
    def _create_file(self):
        '''
            Create files for testing.

            .. note::
                Create files in the root dir of the server.
        '''
        with open('test/loading_test.html', 'w') as f:
            f.write("{% module test() %}")

        with open('module/test.py', 'w') as f:
            f.write("""
import tornado.web


class TestModule(tornado.web.UIModule):

    def render(self):
        return 'Hello World'
            """)

    def _remove_file(self):
        '''
            Remove files created during testing.
        '''
        os.remove('test/loading_test.html')
        os.remove('module/test.py')

    def setUp(self):
        self._create_file()
        self.server_ioloop = IOLoop()

        sock, self.port = bind_unused_port()

        app = Application([
            ('/', LoadingModuleHandler),
            ], ui_modules=modules.get_ui_modules(['test']))

        self.server = HTTPServer(app, io_loop=self.server_ioloop)
        self.server.add_socket(sock)
        self.server_thread = threading.Thread(target=self.server_ioloop.start)
        self.server_thread.start()

        self.http_client = HTTPClient()

    def tearDown(self):
        def stop_server():
            self.server.stop()
            # Delay the shutdown of the IOLoop by one iteration because
            # the server may still have some cleanup work left when
            # the client finishes with the response (this is noticable
            # with http/2, which leaves a Future with an unexamined
            # StreamClosedError on the loop).
            self.server_ioloop.add_callback(self.server_ioloop.stop)
        self.server_ioloop.add_callback(stop_server)
        self.server_thread.join()
        self.http_client.close()
        self.server_ioloop.close(all_fds=True)
        self._remove_file()

    def get_url(self, path):
        return 'http://127.0.0.1:{0}{1}'.format(self.port, path)

    def test_module_loading_handler(self):
        '''
            Test ``modules.get_ui_modules`` in a async server.

            .. note::
                The case create ``test/loading_test.html`` and
                ``module/test.py`` during testing and would overwrite the cont-
                ent if files already exist.
        '''
        response = self.http_client.fetch(self.get_url('/'))
        assert_equal(response.body, b"""Hello World""")
