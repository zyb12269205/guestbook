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
import time
import logging

from google.appengine.ext.webapp.template import render


from data_access import access_key, member_key, Access, Member


KEY = 'member_id'
class BasePage(webapp2.RequestHandler):
  def redirect_cookie(self, url):
    key_detail = self.request.cookies.get(KEY, None)

    if key_detail is None:
      key_detail = self.request.get(KEY, None)

    expires = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(time.time() +  0.5 * 3600 ))#  half an hour from now))
    if key_detail is not None:
      self.response.headers.add_header(
        'Set-Cookie',
        'member_id=%s; expires=%s'
          % ( self.request.get(KEY).encode(), expires))
    
    self.redirect(url)


class HomePage(BasePage):
  def get(self):
    template = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(render(template,{}))


class Login(BasePage):
  def post(self):
    access = Access(parent=access_key)
    logging.error(self.request)
    access_detail = access.verify_access(self.request.get(KEY), self.request.get('password'))
    if access_detail:
        self.redirect_cookie('/member')
    else:
        self.redirect('/')

class MemberPage(BasePage):
  def get(self):
    if self.request.cookies.get(KEY) is None:
      self.redirect('/')
    member = Member(parent=member_key)
    member_detail = member.retrieval_member_detail(self.request.cookies.get(KEY))
    template = os.path.join(os.path.dirname(__file__), 'member.html')
    self.response.out.write(render(template,member_detail))


#
#class SignUp(webapp2.RequestHandler):
#  def post(self):
#    access = Access(parent=access_key)
#    try:
#        access.member_id = int(self.request.get('member_id'))
#        access.password = self.request.get('password')
#        access.project_access = 1
#        access.member_access = 0
#        access.progress_access = 0
#        access.attendance_access = 1
#        access.meeting_access = 1
#        access.put()
#    except:
#        pass
#    self.redirect('/')


class DetailUpdate(BasePage):
  def post(self):
    if self.request.cookies.get('member_id') is None:
      self.redirect('/')
    member = Member(parent=member_key)
    member_detail = Member(
      member_id = self.request.get('member_id'),
      english_name = self.request.get('engish_name'),
      chinese_name = self.request.get('chinese_name'),
      salutation = self.request.get('salutation'),
      nric = self.request.get('nric'),
      nationality = self.request.get('nationality'),
      join_time = self.request.get('join_time'),
      title = self.request.get('title'),
      date_of_birth = self.request.get('date_of_birth'),
      contact = self.request.get('contact'),
      address = self.request.get('address'),
      email = self.request.get('email'),
      company = self.request.get('company'),
      industry = self.request.get('industry'),
      job_title = self.request.get('job_title')
    )
    member.add_update_member_detail(self.request.cookies.get('member_id'), member_detail)
    self.redirect_cookie('/member')



class Dummy(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Hello World!")



app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', Login),
  ('/member', MemberPage),
  ('/add_update_detail', DetailUpdate),
  #('/signup', SignUp),
  ('/home', Dummy),
], debug=True)
