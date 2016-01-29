# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
import base


class SafeHandler(base.BaseHandler):
    '''
        Define the default get_current_user, which is called when son class check if a user have login in.
    '''

    def get_current_user(self):
        return self.get_secure_cookie('user_id') # We use user_id as the default cookie value to be checked
