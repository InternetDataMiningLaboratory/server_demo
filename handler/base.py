# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
import tornado.web
import traceback
import email_sender

class BaseHandler(tornado.web.RequestHandler):
    '''
       The base class of other handlers and redirect to 404 page if any exception raised.
    '''

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        try:
            message = '\n'.join(traceback.format_exception(*kwargs['exc_info']))
        except KeyError:
            message = str(status_code)
        email_sender.async_send(title="The Exception Raised", message=message)
        self.render('404.html', page_title="404")
