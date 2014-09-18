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

    

class Project(ndb.Model):
    project_id = ndb.IntegerProperty()
    project_name = ndb.StringProperty()


class Meeting(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    meeting_time = ndb.StringProperty()

class Attendance(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    member_id = ndb.IntegerProperty()
    appear = ndb.IntegerProperty() # 0 no 1 yes, default 0

class Progress(ndb.Model):
    member_id = ndb.IntegerProperty()
    project_id = ndb.IntegerProperty()
    meeting_id = ndb.IntegerProperty()


