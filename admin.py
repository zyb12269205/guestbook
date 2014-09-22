__author__ = 'yingbozhan'

from util import *
from constants import *
from data_access import *

import logging
import os
from google.appengine.ext.webapp.template import render


class AdminHomePageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        self.render_page(ADMIN_HOME_HTML,{})

###################
# meeting related
#
##################
class AdminMeetingListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting = Meeting(parent=meeting_key)
        all_meetings_detail = meeting.get_all()
        self.render_page(ADMIN_MEETING_LIST_HTML,{'meetings':all_meetings_detail})

class AdminMeetingPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            meeting = Meeting.get_by_id(id=int(self.request.get(MEETING_ID)),parent=meeting_key)
        except:
            meeting = None
        self.render_page(ADMIN_MEETING_ADD_HTML,{'meeting':meeting})


class AdminMeetingAddUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting_id = int(self.request.get(MEETING_ID,'-1'))
        meeting_select = Meeting(id=int(meeting_id),parent=meeting_key)
        meeting_select.meeting_time = self.request.get('meeting_time')
        meeting_select.key_name = meeting_id
        try:
            meeting_select.meeting_id = meeting_id
            meeting_select.put()
        except:
            self.redirect_cookie('/')
            return
        self.redirect_cookie(ADMIN_MEETING_LIST_PAGE)

class AdminMeetingDeleteClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting_id = self.request.get(MEETING_ID,-1)
        meeting = Meeting(parent=meeting_key)
        meeting_select = meeting.get_or_insert(meeting_id)
        meeting_select.key.delete()



###################
# project related
#
##################
class AdminProjectListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project = Project(parent=project_key)
        all_projects_detail = project.get_all()
        self.render_page(ADMIN_PROJECT_LIST_HTML,{'projects':all_projects_detail})

class AdminProjectPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            project = Project.get_by_id(id=int(self.request.get(PROJECT_ID)),parent=project_key)
        except:
            project = None
        self.render_page(ADMIN_PROJECT_ADD_HTML,{'project':project})


class AdminProjectAddUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project_id = int(self.request.get(PROJECT_ID,'-1'))
        project_select = Project(id=project_id,parent=project_key)
        project_select.project_name = self.request.get('project_name')
        project_select.project_requirement = self.request.get('project_requirement')
        project_select.key_name = project_id
        try:
            project_select.project_id = project_id
            project_select.put()
        except:
            self.redirect_cookie('/')
            return
        self.redirect_cookie(ADMIN_PROJECT_LIST_PAGE)

class AdminProjectDeleteClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project_id = self.request.get(PROJECT_ID,-1)
        project = Project(parent=project_key)
        project_select = project.get_or_insert(project_id)
        project_select.key.delete()
        self.redirect_cookie(ADMIN_PROJECT_LIST_PAGE)


class AdminMemberListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        member = Member(parent=member_key)
        all_members = member.get_all()
        self.render_page(ADMIN_PROJECT_LIST_HTML,all_members)


