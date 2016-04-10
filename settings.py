# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
# Created Time: 2015年09月03日 星期四 14时26分03秒
#
'''
    Choose the config file
    ----------------------------

    Choose the config file in command line::

        python server.py --config=debug

    The server would try to read the configs from ``debug.conf`` at the directory.

    Debug mode
    -----------------------------

    When in debug mode:

    * Server autoreload when changes detected in the source code.
    * The level of ``logging`` is set to ``DEBUG``, default is ``INFO``

    Defined settings
    -----------------------------

    =================   ============================    ========    ===========
    Name                Usage                           Group       Default
    =================   ============================    ========    ===========
    port                The port listened by server     basic       8888
    name                Server name                     basic       my_homepage
    debug               Debug mode                      basic       False
    xsrf_cookies        Xsrf protection                 basic       True
    static_path         Path of static files            app         CONSTANT
    template_path       Path of frontend templates      app         CONSTANT
    ui_modules          Frontend modules                app         FILE
    login_url           Url of login page               app         '/login'
    cookie_secret       Cookie secret                   app         random gen-
                                                                    eration
    database_type       Database type                   database    mysql
    database_address    Database address                database    127.0.0.1
    database_port       Database port                   database    3306
    database_user       Database user                   database    admin
    database_password   Database password               database    my_homepage
    mail_type           Mail server type                mail        smtp
    mail_server         Mail server address             mail        127.0.0.1
    mail_port           Mail server port                mail        375
    mail_user           Mail user                       mail        noreply
    mail_password       Mail password                   mail        my_noreply
    alert_list          Send alert mails to             mail        \[\]
    =================   ============================    ========    ===========


    Methods
    -----------------------------

'''
import os
import base64
import uuid
import logging

from tornado.options import define, options, parse_command_line
from tornado.options import parse_config_file
from tornado.log import enable_pretty_logging

from modules import get_ui_modules

# TODO: Settings load from environments
# TODO: Logging settings which create loggers seperately for mail and database
# and allow to send mail or HTTP requests
# TODO: Test of load_settings
# TODO: Define settings of alert mails

# Path Defined
ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(ROOT, 'static')
TEMPLATE_ROOT = os.path.join(ROOT, 'template')

# Define settings
# It's so belong since someone don't hope you modify settings here
define("config", help="The config file of Tornado", group="basic")
define("port", default=8888, help="The port listened by server", group="basic")
define("name", default='my_homepage', help="Server name", group="basic")
define("debug", default=False, help="Debug mode", group="basic")
define("xsrf_cookies", default=True, help="Xsrf protection", group="basic")

define(
    "static_path",
    default=STATIC_ROOT,
    help="The path of static files",
    group="application"
)
define(
    "template_path",
    default=TEMPLATE_ROOT,
    help="The path of frontend templates",
    group="application"
)
define(
    "ui_modules",
    default=get_ui_modules(),
    help="The frontend modules",
    group="application"
)
define(
    "login_url",
    default='/login',
    help="Url of login page",
    group="application"
)
define(
    "cookie_secret",
    default=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    help="Cookie secret",
    group="application"
)

define(
    "database_type",
    default='mysql',
    help="The type of database adopted",
    group="database"
)
define(
    "database_address",
    default='127.0.0.1',
    help="The address of database",
    group="database"
)
define(
    "database_port",
    default=3306,
    help="The port of database",
    group="database"
)
define(
    "database_user",
    default='admin',
    help="The user of database",
    group="database"
)
define(
    "database_password",
    default='my_homepage',
    help="The password of database",
    group="database"
)

define(
    "mail_type",
    default='smtp',
    help="The type of mail server",
    group="mail"
)
define(
    "mail_server",
    default='127.0.0.1',
    help="The mail server",
    group="mail"
)
define(
    "mail_port",
    default='375',
    help="The port of mail server",
    group="mail"
)
define(
    "mail_user",
    default='noreply',
    help="The user of mail server",
    group="mail"
)
define(
    "mail_password",
    default='my_noreply',
    help="The password of mail server",
    group="mail"
)
define(
    "alert_list",
    multiple=True,
    default=[],
    help="The receive list of alert mails", group="mail"
)


def load_settings():
    '''
        Load settings from command line and config file.
    '''

    # Parse command line
    options.logging = 'none' # To turn off logging settings
    options.log_to_stderr = True # Log to stderr
    parse_command_line()

    # Load settings from another config file if given
    if options.config:
        parse_config_file(options.config + '.conf')

    # Log file prefix
    options.log_file_prefix = ''.join((
        'log/',
        options.name,
        '-',
        str(options.port),
        '.log',
    ))

    # Logging settings
    if options.logging == 'none': # There are no logging settings before
        options.logging = 'debug' if options.debug else 'info'
        enable_pretty_logging(options=options)

    pretty_options_output()

def pretty_options_output():
    '''
        Output options in a pretty format.
    '''
    pretty_options = ('{0}-----{1}'.format(key, value) for key, value in options.as_dict().iteritems())
    logging.info('[SERVER SETTINGS]')
    map(logging.info, pretty_options)
    logging.info('#'.join(('' for index in xrange(55))))
