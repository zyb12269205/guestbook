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
        try:
            meeting_id = int(self.request.get(MEETING_ID,'0'))
        except:
            self.redirect_cookie(ADMIN_MEETING_LIST_PAGE)
            return  
        meeting_select = Meeting(id=int(meeting_id),parent=meeting_key)
        meeting_select.meeting_time = self.request.get('meeting_time')
        meeting_select.key_name = meeting_id
        meeting_select.meeting_id = meeting_id
        meeting_select.put()

        self.redirect_cookie(ADMIN_MEETING_LIST_PAGE)

class AdminMeetingDeleteClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            meeting_id = int(self.request.get(MEETING_ID,0))
            meeting = Meeting(parent=meeting_key)
            meeting_select = meeting.get_or_insert(meeting_id)
            meeting_select.key.delete()
        except:
            pass
        self.redirect_cookie(ADMIN_MEETING_LIST_PAGE)



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
        try:
            project_id = int(self.request.get(PROJECT_ID,'0'))
        except:
            self.redirect_cookie(ADMIN_PROJECT_LIST_PAGE)
            return
        project_select = Project(id=project_id,parent=project_key)
        project_select.project_name = self.request.get('project_name')
        project_select.project_requirement = self.request.get('project_requirement')
        project_select.project_id = project_id
        project_select.put()

        self.redirect_cookie(ADMIN_PROJECT_LIST_PAGE)

class AdminProjectDeleteClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            project_id = int(self.request.get(PROJECT_ID,0))
            project = Project(id=project_id,parent=project_key)
            project.key.delete()
        except:
            pass
        self.redirect_cookie(ADMIN_PROJECT_LIST_PAGE)



###################
# member related
#
##################
class AdminMemberListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        member = Member(parent=member_key)
        all_members_detail = member.get_all()
        self.render_page(ADMIN_MEMBER_LIST_HTML,{'members':all_members_detail})

class AdminMemberPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            member = Member.get_by_id(id=int(self.request.get(MEMBER_ID)),parent=member_key)
        except:
            member = None
        self.render_page(ADMIN_MEMBER_ADD_HTML,{'member':member})


class AdminMemberAddUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        try:
            member_id = int(self.request.get(MEMBER_ID,'0'))
            member_select = Member(id=member_id,parent=member_key)
            member_select.member_id = member_id
            member_select.english_name = self.request.get('english_name', '')
            member_select.chinese_name = self.request.get('chinese_name', '')
            member_select.salutation = self.request.get('salutation', '')
            member_select.nric = self.request.get('nric', '')
            member_select.nationality = self.request.get('nationality', '')
            #member.join_time = self.request.get('join_time')
            member_select.title = self.request.get('title', '')
            #member.date_of_birth = self.request.get('date_of_birth')
            member_select.contact = self.request.get('contact', '')
            member_select.address = self.request.get('address', '')
            member_select.email = self.request.get('email', '')
            member_select.company = self.request.get('company', '')
            member_select.industry = self.request.get('industry', '')
            member_select.job_title = self.request.get('job_title', '')
            member_select.key_name = member_id
            member_select.put()
        except:
            self.redirect_cookie(ADMIN_MEMBER_LIST_PAGE)
            return
        self.redirect_cookie(ADMIN_MEMBER_LIST_PAGE)

class AdminMemberDeleteClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect('/')
        member_id = self.request.get(MEMBER_ID,0)
        member = Member(parent=member_key)
        member_select = member.get_or_insert(member_id)
        member_select.key.delete()
        self.redirect_cookie(ADMIN_MEMBER_LIST_PAGE)


##########################
#attendance related
#
##########################
class AdminAttendanceListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect_cookie('/')
        attendance = Attendance(parent=attendance_key)
        attendance_details = attendance.get_all()
        self.render_page(ADMIN_ATTENDANCE_LIST_HTML,{'attendances':attendance_details})


class AdminAttendanceUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect_cookie('/')
        try:
            attendance = Attendance(parent=attendance_key)
            attendance.update_all(self.request)

        except:
            pass
        self.redirect_cookie(ADMIN_ATTENDANCE_LIST_PAGE)


class AdminProgressListPageClass(BasePage):
    def get(self):
        if not self.is_admin_log_in(): self.redirect_cookie('/')
        progress = Progress(parent=progress_key)
        progress_details = progress.get_all()
        self.render_page(ADMIN_PROGRESS_LIST_HTML,{'progresses': progress_details})


class AdminProgressUpdateClass(BasePage):
    def post(self):
        if not self.is_admin_log_in(): self.redirect_cookie('/')
        try:
            progress = Progress(parent=progress_key)
            progress.update_all(self.request)
        except:
            pass
        self.redirect_cookie(ADMIN_PROGRESS_LIST_PAGE)



