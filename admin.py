__author__ = 'yingbozhan'

from util import *
from constants import *
from data_access import *

import logging
import os
from google.appengine.ext.webapp.template import render


class AdminHomePage(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        self.redirect_cookie(ADMIN_HOME_HTML)

###################
# meeting related
#
##################
class AdminMeetingListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting = Meeting(parent=meeting_key)
        all_meetings_detail = Meeting.get_all()
        self.render_page(ADMIN_MEETING_LIST_HTML,all_meetings_detail)

class AdminMeetingAddPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting = Meeting(parent=meeting_key)
        all_meetings_detail = meeting.get_or_insert(self.request.cookies.get('meeting_id','-1'))
        self.render_page(ADMIN_MEETING_ADD_HTML,all_meetings_detail)


class AdminMeetingAddUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        meeting = Meeting(parent=meeting_key)
        meeting_select = meeting.get_or_insert(self.request.get('meeting_id',-1))
        meeting_select.meeting_time = self.request.get('meeting_time')
        try:
            meeting_select.meeting_id = int(self.request.get('meeting_id'))
            meeting_select.put()
        except:
            self.redirect_cookie('/')
            return
        self.redirect_cookie('/admin_meeting_list')

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
        all_projects_detail = Project.get_all()
        self.render_page(ADMIN_PROJECT_LIST_HTML,all_projects_detail)

class AdminProjectAddPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project = Project(parent=project_key)
        all_projects_detail = project.get_or_insert(self.request.cookies.get('project_id','-1'))
        self.render_page(ADMIN_PROJECT_ADD_HTML,all_projects_detail)


class AdminProjectAddUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project = Project(parent=project_key)
        project_select = project.get_or_insert(self.request.get('project_id',-1))
        project_select.project_name = self.request.get('project_name')
        project_select.project_requirement = self.request.get('project_requirement')
        try:
            project_select.project_id = int(self.request.get('project_id'))
            project_select.put()
        except:
            self.redirect_cookie('/')
            return
        self.redirect_cookie('/admin_project_list')

class AdminProjectDeleteClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        project_id = self.request.get(PROJECT_ID,-1)
        project = Project(parent=project_key)
        project_select = project.get_or_insert(project_id)
        project_select.key.delete()
        self.redirect_cookie('/admin_project_list')


class AdminMemberListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        member = Member(parent=member_key)
        all_members = member.get_all()
        self.render_page(ADMIN_PROJECT_LIST_HTML,all_members)


