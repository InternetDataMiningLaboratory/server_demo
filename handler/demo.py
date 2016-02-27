# -*- coding: utf-8 -*-
#
# Author: jimin.huang
#
import base


class DemoHandler(base.BaseHandler):
    '''
        The demo of a handler which respond requests with demo page.
    '''
    def get(self):
        # String to be shown in the page
        welcome_string = 'The Demo Server Is Running'

        # Render the shown page
        self.render(
            'demo.html',
            welcome_string=welcome_string,
            page_title='My Homepage',
        )
