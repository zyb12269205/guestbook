#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



import os
import webapp2
from google.appengine.ext.webapp.template import render

from data_access import access_key, Access

ACCESS_DETAIL = None

class HomePage(webapp2.RequestHandler):
  def get(self):
    tmpl = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(render(tmpl,{}))


class Login(webapp2.RequestHandler):
  def post(self):
    access = Access(parent=access_key)
    access_detail = access.verify_access(self.request.get('member_id'), self.request.get('password'))
    if access_detail:
        self.redirect('/member')
        ACCESS_DETAIL = access_detail
    else:
        self.redirect('/')

class MemberPage(webapp2.RequestHandler):
  def get(self):
    tmpl = os.path.join(os.path.dirname(__file__), 'member.html')
    self.response.out.write(render(tmpl,{}))



class SignUp(webapp2.RequestHandler):
  def post(self):
    access = Access(parent=access_key)
    try:
        access.member_id = int(self.request.get('member_id'))
        access.password = self.request.get('password')
        access.project_access = 1
        access.member_access = 0
        access.progress_access = 0
        access.attendance_access = 1
        access.meeting_access = 1
        access.put()
    except:
        pass
    self.redirect('/')


class Dummy(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello World!")



app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', Login),
  ('/member', MemberPage),
  ('/signup', SignUp),
  ('/home', Dummy),
], debug=True)
