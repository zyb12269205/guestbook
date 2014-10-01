#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

access_key = ndb.Key('Access', 'default_access')
member_key = ndb.Key('Member', 'default_member')
project_key = ndb.Key('Project', 'default_project')
progress_key = ndb.Key('Progress', 'default_progress')
meeting_key = ndb.Key('Meeting', 'default_meeting')
attendance_key = ndb.Key('Attendance', 'default_attendance')



class Access(ndb.Model):
    member_id = ndb.IntegerProperty()
    password = ndb.StringProperty()

    #the following, 0  self access, 1  all access,
    member_access = ndb.IntegerProperty(required=True, default=0) # default 0
    project_access = ndb.IntegerProperty() # default 1
    progress_access = ndb.IntegerProperty(required=True, default=0) # default 0
    meeting_access = ndb.IntegerProperty() # default 1
    attendance_access = ndb.IntegerProperty(required=True, default=0) # default 0

    @classmethod
    def verify_access(cls, member_id_pass, password_pass):
        try:
            return cls.query(Access.member_id == int(member_id_pass), Access.password == password_pass)
        except:
            return None



class Member(ndb.Model):
    member_id = ndb.IntegerProperty()
    english_name = ndb.StringProperty()
    chinese_name = ndb.StringProperty()
    salutation = ndb.StringProperty()
    nric = ndb.StringProperty()
    nationality = ndb.StringProperty()
    join_time = ndb.DateProperty()
    title = ndb.StringProperty()
    date_of_birth = ndb.DateProperty()
    contact = ndb.StringProperty()
    address = ndb.StringProperty()
    email = ndb.StringProperty()
    company = ndb.StringProperty()
    industry = ndb.StringProperty()
    job_title = ndb.StringProperty()

    @classmethod
    def retrieval_member_detail(cls, member_id_pass):
      details =  cls.query(Member.member_id == int(member_id_pass)).fetch()
      if len(details) == 1: return details[0]
      else: return None


    def get_all(cls):
        list_members = []
        for member in cls.query().fetch():
            if member.member_id is not None and int(member.member_id) > 0:
                list_members.append(member)
        return list_members

    def member_name_dict(self):
        members = self.get_all()
        member_dict = {}
        for member in members:
            member_dict[member.member_id] = member.english_name
        return member_dict

class Project(ndb.Model):
    project_id = ndb.IntegerProperty()
    project_name = ndb.StringProperty()
    project_requirement = ndb.StringProperty()

    def get_all(cls):
        list_projects = []
        for project in cls.query().fetch():
            if project.project_id is not None and int(project.project_id) > 0:
                list_projects.append(project)
        return list_projects



class Meeting(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    meeting_time = ndb.StringProperty()


    def get_all(cls):
        list_meetings = []
        for meeting in cls.query().fetch():
            if meeting.meeting_id is not None and int(meeting.meeting_id) > 0:
                list_meetings.append(meeting)
        return list_meetings

class Attendance(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    member_id = ndb.IntegerProperty()
    attend = ndb.IntegerProperty()

    def get_all(self, meeting_id):
        list_attendance = []
        member_dict = Member(parent=member_key).member_name_dict()
        if meeting_id <=0: return None
        for attendance in self.query().fetch():
            attendance_dict = {}
            try:
                if int(meeting_id) != int(attendance.meeting_id): continue
            except:
                return None
            attendance_dict['meeting_id'] = meeting_id
            attendance_dict['member_id'] = attendance.member_id
            attendance_dict['member_name'] = member_dict.get(attendance.member_id, None)
            if attendance_dict['member_name'] is None: continue
            attendance_dict['attend'] = attendance.attend
            list_attendance.append(attendance_dict)
        return list_attendance







class Progress(ndb.Model):
    member_id = ndb.IntegerProperty()
    project_id = ndb.IntegerProperty()
    meeting_id = ndb.IntegerProperty()


