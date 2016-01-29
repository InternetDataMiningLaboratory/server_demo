# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时19分22秒
#
'''
    The main file to start server.
'''

import tornado.ioloop
import tornado.autoreload
import tornado.web
import settings
import email_sender
import urls

import logging
import datetime
import traceback

from tornado.options import options

if __name__ == "__main__":
    # Load settings
    settings.load_settings()

    application = tornado.web.Application(urls.urls, **options.as_dict())
    application.listen(options.port)
    server_instance = tornado.ioloop.IOLoop.instance()
    # tornado.autoreload.add_reload_hook(database.release)

    try:
        server_instance.start()
    except KeyboardInterrupt:
        logging.error("Existing")
        exit_error = u'Keyboard Exit'
    except Exception, e:
        logging.exception(e)
        exit_error = traceback.format_exec()
    finally:
        server_instance.add_callback(server_instance.stop)
        exit_error = str(datetime.datetime.now()) + '\n' + exit_error
        email_sender.send(title='Server exit unexpectly', message=exit_error)
