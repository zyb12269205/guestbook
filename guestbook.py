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




import os
from google.appengine.ext.webapp.template import render


from constants import *
from data_access import *
from util import *
from admin import *


class HomePage(BasePage):
    def get(self):
        self.render_page(HOME_HTML,{})
#        template = os.path.join(os.path.dirname(__file__), 'home.html')
#        self.response.out.write(render(template, {}))

class Login(BasePage):
    def post(self):
        access = Access(parent=access_key)
        access_detail = access.verify_access(self.request.get(MEMBER_ID), self.request.get('password'))
        if access_detail:
            if self.request.get(MEMBER_ID) == '1':
                self.insert_cookie(ADMIN_HOME_PAGE)
                return
            self.insert_cookie('/individual')
        else:
            self.redirect('/')

# class SignUp(webapp2.RequestHandler):
#     def get(self):
#         try:
#             access = Access(parent=access_key).get_or_insert(self.request.get('member_id'))
#             if access.member_id is not None:
#                 self.redirect('/')
#                 return
#             access.member_id = int(self.request.get('member_id'))
#             access.password = self.request.get('password')
#             access.project_access = 1
#             access.member_access = 0
#             access.progress_access = 0
#             access.attendance_access = 1
#             access.meeting_access = 1
#             access.key_name = access.member_id
#             access.put()
#         except:
#             pass
#         self.insert_cookie('/')
#
#
# class MemberPage(BasePage):
#     def get(self):
#         if self.request.cookies.get(MEMBER_ID) is None:
#             self.redirect('/')
#         member = Member(parent=member_key)
#         member_detail = member.retrieval_member_detail(self.request.cookies.get(MEMBER_ID))
#         template = os.path.join(os.path.dirname(__file__), 'member.html')
#         self.response.out.write(member_detail)
#         self.response.out.write(render(template, {"member": member_detail}))
#
#
# class MemberUpdate(BasePage):
#     def post(self):
#         if self.request.cookies.get(MEMBER_ID) == '':
#             self.redirect('/')
#         member = Member(parent=member_key).retrieval_member_detail(self.request.cookies.get(MEMBER_ID))
#         if member is None: member = Member(parent=member_key)
#         member.member_id = int(self.request.cookies.get(MEMBER_ID))
#         member.english_name = self.request.get('english_name', '')
#         member.chinese_name = self.request.get('chinese_name', '')
#         member.salutation = self.request.get('salutation', '')
#         member.nric = self.request.get('nric', '')
#         member.nationality = self.request.get('nationality', '')
#         #member.join_time = self.request.get('join_time')
#         member.title = self.request.get('title', '')
#         #member.date_of_birth = self.request.get('date_of_birth')
#         member.contact = self.request.get('contact', '')
#         member.address = self.request.get('address', '')
#         member.email = self.request.get('email', '')
#         member.company = self.request.get('company', '')
#         member.industry = self.request.get('industry', '')
#         member.job_title = self.request.get('job_title', '')
#         member.key_name = member.member_id
#         member.put()
#         template = os.path.join(os.path.dirname(__file__), 'member.html')
#         self.response.out.write(member)
#         self.response.out.write(render(template, {"member": member}))
#
#
# class Dummy(webapp2.RequestHandler):
#     def get(self):
#         self.response.out.write("Hello World!")
#
# class Project(webapp2.RequestHandler):
#     def get(self):
#         template = os.path.join(os.path.dirname(__file__), 'project.html')
#         self.response.out.write(render(template,{}))
#
# class refresh_project(webapp2.RequestHandler):
#     projects = {
#         1: '破冰时间', 2: '组织语言',
#         3: '切入重点', 4: '表达方式',
#         5: '身体会说话', 6: '发声的多样性',
#         7: '主题研究', 8: '习惯视觉辅助工具',
#         9: '有力的劝说', 10: '激发听众'
#     }
#
#     def get(self):
#         for project_id in self.projects.keys():
#             project = Project(
#                 project_id=project_id,
#                 project_name=self.projects[project_id])
#             project.put()
#         self.response.out.write("Hello World!")
#
#
# class PersonalProgressPage(BasePage):
#     def get(self):
#         if self.request.cookies.get(MEMBER_ID) is None:
#             self.redirect('/')
#         progress = Progress(parent=progress_key)
#         progress_detail = progress.get_progress_detail(self.request.cookies.get(MEMBER_ID))
#         template = os.path.join(os.path.dirname(__file__), 'personal_progress.html')
#         self.response.out.write(progress_detail)
#         self.response.out.write(render(template, {"progress": progress_detail}))
#
#
# class PersonalAttendancePage(BasePage):
#     def get(self):
#         if self.request.cookies.get(MEMBER_ID) is None:
#             self.redirect('/')
#         attendance = Attendence(parent=attendance_key)
#         attendance_detail = attendance.get_or_insert(self.request.cookies.get(MEMBER_ID))
#         template = os.path.join(os.path.dirname(__file__), 'personal_attendance.html')
#         self.response.out.write(attendance_detail)
#         self.response.out.write(render(template, {"attendance": attendance_detail}))
#
#
#
#


app = webapp2.WSGIApplication([
    ('/', HomePage),
    (LOG_IN_ACTION, Login),
    (ADMIN_HOME_PAGE,AdminHomePageClass),
#    ('/individual', MemberPage),
    # ('/personal_progress',PersonalProgressPage),
    # ('/personal_attendance', PersonalAttendancePage),
    # ('/add_update_detail', MemberUpdate),
    # ('/signup', SignUp),
    # ('/refresh_project', refresh_project),
    # ('/home', Dummy),
    # ('/project', Project),
    (ADMIN_MEETING_LIST_PAGE,AdminMeetingListPageClass),
    (ADMIN_MEETING_HOME_PAGE,AdminMeetingListPageClass),
    (ADMIN_MEETING_MODI_PAGE,AdminMeetingPageClass),
    (ADMIN_MEETING_MODI_ACTION, AdminMeetingAddUpdateClass),
    (ADMIN_MEETING_DELE_ACTION, AdminMeetingDeleteClass),

    (ADMIN_PROJECT_LIST_PAGE,AdminProjectListPageClass),
    (ADMIN_PROJECT_HOME_PAGE,AdminProjectListPageClass),
    (ADMIN_PROJECT_MODI_PAGE,AdminProjectPageClass),
    (ADMIN_PROJECT_MODI_ACTION, AdminProjectAddUpdateClass),
    (ADMIN_PROJECT_DELE_ACTION, AdminProjectDeleteClass),

    (ADMIN_MEMBER_LIST_PAGE,AdminMemberListPageClass),
    (ADMIN_MEMBER_HOME_PAGE,AdminMemberListPageClass),
    (ADMIN_MEMBER_MODI_PAGE,AdminMemberPageClass),
    (ADMIN_MEMBER_MODI_ACTION, AdminMemberAddUpdateClass),
    (ADMIN_MEMBER_DELE_ACTION, AdminMemberDeleteClass),
], debug=True)
