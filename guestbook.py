#!/usr/bin/python
# -*- coding: utf-8 -*-

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



import logging
import webapp2
import time
import os

from data_access import access_key, member_key, Access, Member, Project, project_key
from google.appengine.ext.webapp.template import render


KEY = 'member_id'
class BasePage(webapp2.RequestHandler):
  def redirect_cookie(self, url):
    key_detail = self.request.cookies.get(KEY, None)

    if key_detail is None or key_detail == '':
      key_detail = self.request.get(KEY, None)

    expires = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT",
                            time.gmtime(time.time() + 0.5 * 3600))#  half an hour from now))
    if key_detail is not None:
      self.response.headers.add_header(
        'Set-Cookie',
        'member_id=%s; expires=%s'
        % ( key_detail.encode(), expires))

    self.redirect(url)

  def update_cookie(self, url):
    key_detail = self.request.get(KEY, None)
    if key_detail is None: self.redirect_cookie('/')
    expires = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT",
                            time.gmtime(time.time() + 0.5 * 3600))#  half an hour from now))
    self.response.headers.add_header(
      'Set-Cookie',
      'member_id=%s; expires=%s'
      % ( key_detail.encode(), expires))
    self.redirect(url)

class HomePage(BasePage):
  def get(self):
    template = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(render(template, {}))

class Login(BasePage):
  def post(self):
    access = Access(parent=access_key)
    logging.error(self.request)
    access_detail = access.verify_access(self.request.get(KEY), self.request.get('password'))
    if access_detail:
      self.update_cookie('/member')
    else:
      self.redirect('/')

class MemberPage(BasePage):
  def get(self):
    if self.request.cookies.get(KEY) is None:
      self.redirect('/')
    member = Member(parent=member_key)
    member_detail = member.retrieval_member_detail(self.request.cookies.get(KEY))
    template = os.path.join(os.path.dirname(__file__), 'member.html')
    self.response.out.write(member_detail)
    self.response.out.write(render(template, {"member": member_detail}))

class SignUp(webapp2.RequestHandler):
  def get(self):
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

class DetailUpdate(BasePage):
  def post(self):
    if self.request.cookies.get(KEY) == '':
      self.redirect('/')
    member = Member(parent=member_key).retrieval_member_detail(self.request.cookies.get(KEY))
    if member is None: member = Member(parent=member_key)
    member.member_id = int(self.request.cookies.get(KEY))
    member.english_name = self.request.get('english_name', '')
    member.chinese_name = self.request.get('chinese_name', '')
    member.salutation = self.request.get('salutation', '')
    member.nric = self.request.get('nric', '')
    member.nationality = self.request.get('nationality', '')
    #member.join_time = self.request.get('join_time')
    member.title = self.request.get('title', '')
    #member.date_of_birth = self.request.get('date_of_birth')
    member.contact = self.request.get('contact', '')
    member.address = self.request.get('address', '')
    member.email = self.request.get('email', '')
    member.company = self.request.get('company', '')
    member.industry = self.request.get('industry', '')
    member.job_title = self.request.get('job_title', '')
    member.put()
    template = os.path.join(os.path.dirname(__file__), 'member.html')
    self.response.out.write(member)
    self.response.out.write(render(template, {"member": member}))


class Dummy(webapp2.RequestHandler):
  def get(self):
    self.response.out.write("Hello World!")


class refresh_project(webapp2.RequestHandler):
  projects = {
    1: '破冰时间', 2: '组织语言',
    3: '切入重点', 4: '表达方式',
    5: '身体会说话', 6: '发声的多样性',
    7: '主题研究', 8: '习惯视觉辅助工具',
    9: '有力的劝说', 10: '激发听众'
  }

  def get(self):
    for project_id in self.projects.keys():
      project = Project(
        project_id = project_id,
        project_name = self.projects[project_id])
      project.put()
    self.response.out.write("Hello World!")


app = webapp2.WSGIApplication([
  ('/', HomePage),
  ('/login', Login),
  ('/member', MemberPage),
  ('/add_update_detail', DetailUpdate),
  ('/signup', SignUp),
  ('/refresh_project', refresh_project),
  ('/home', Dummy),
  ], debug=True)
