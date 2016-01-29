# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
#
'''
Sending email via `tornado_email <https://github.com/windworship/tornado_email>_`
'''
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import tornado.gen
import tornado_email.client as async_smtp
from tornado.options import options


def deal_with_address(declare_name, address):
    '''
        Deal with the address of mail.
    '''
    return formataddr(
        (
            Header(declare_name, 'utf-8').encode(),
            address.encode('utf-8'),
        )
    )


def send(
    title=None,
    message=None,
    host=None,
    user=None,
    password=None,
    to=None,
    callback=None,
):
    '''
        Send emails sync.
    '''

    # Default parameter
    if host is None:
        host = options.mail_server
    if user is None:
        user = options.mail_user
    if password is None:
        password = options.mail_password
    if to is None:
        to = options.alert_list

    server = smtplib.SMTP()
    server.connect(host)
    server.starttls()
    server.login(user, password)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] =\
        deal_with_address(
            'Wuhan University Internet Data Mining Laboratory',
            user
        )
    msg['Subject'] = Header(title, 'utf-8').encode()
    to_addrs = [to_addr.encode('utf-8') for to_addr in to.split('|')]
    msg['To'] = ', '.join(to_addrs)
    server.sendmail(user, to_addrs, msg.as_string())
    server.quit()


@tornado.gen.coroutine
def async_send(
    title=None,
    message=None,
    host=None,
    user=None,
    password=None,
    to=None,
    callback=None,
):
    '''
        Send emails async.
    '''

    # Default parameter
    if host is None:
        host = options.mail_server
    if user is None:
        user = options.mail_user
    if password is None:
        password = options.mail_password
    if to is None:
        to = options.alert_list

    server = async_smtp.AsyncSMTP()
    yield server.connect(host=host)
    yield server.start_tls()
    yield server.login(username=user, password=password)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] =\
        deal_with_address(
            'Wuhan University Internet Data Mining Laboratory',
            user
        )
    msg['Subject'] = Header(title, 'utf-8').encode()
    to_addrs = [to_addr.encode('utf-8') for to_addr in to.split('|')]
    msg['To'] = ', '.join(to_addrs)
    yield server.send_mail(user, to_addrs, msg.as_string())
    yield server.quit()
