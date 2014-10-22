__author__ = 'zhanyingbo'


import webapp2
from constants import *
import time
import os
from google.appengine.ext.webapp.template import render

SLEEP_TIME = 0.3
class BasePage(webapp2.RequestHandler):
    def is_user_log_in(self):
        if not self.is_log_in():
            return False
        if not self.is_admin:
            return True
        return False

    def is_admin_log_in(self):
        if not self.is_log_in:
            return False
        if self.is_admin:
            return True

    def is_log_in(self):
        if self.request.cookies.get(MEMBER_ID, None) is None:
            return False
        return True

    def is_admin(self):
        if self.request.cookies.get(MEMBER_ID, None) == '1':
            return True
        return False

    def get_member(self):
        return self.request.cookies.get(MEMBER_ID, None)

    def update_expires(self, key_detail):
        expires = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT",
                                time.gmtime(time.time() + 0.5 * 3600))#  half an hour from now))
        if key_detail is not None:
            self.response.headers.add_header(
                'Set-Cookie',
                'member_id=%s; expires=%s'
                % ( key_detail.encode(), expires))

    def update_cookie(self):
        key_detail = self.get_member()
        self.update_expires(key_detail)


    def redirect_cookie(self, url):
        time.sleep(SLEEP_TIME)
        self.update_cookie()
        self.redirect(url)

    def insert_cookie(self, url):
        time.sleep(SLEEP_TIME)
        key_detail = self.request.get(MEMBER_ID, None)
        if key_detail is None: return
        self.update_expires(key_detail)
        self.redirect(url)

    def render_page(self, page, content):
        template = os.path.join(os.path.dirname(__file__), page)
        #self.response.out.write(content)
        self.response.out.write(render(template, content))
        self.update_cookie()