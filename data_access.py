__author__ = 'yingbozhan'

from google.appengine.ext import ndb

access_key = ndb.Key('Access', 'default_access')
member_key = ndb.Key('Member', 'default_member')
project_key = ndb.Key('Project', 'default_project')
progress_key = ndb.Key('Progress', 'default_progress')
meeting_key = ndb.Key('Meeting', 'default_meeting')
attendance_key = ndb.Key('Attendance', 'default_attendance')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class Access(ndb.Model):
    member_id = ndb.IntegerProperty()
    password = ndb.StringProperty()

    #the following, 0  self access, 1  all access,
    member_access = ndb.IntegerProperty() # default 0
    project_access = ndb.IntegerProperty() # default 1
    progress_access = ndb.IntegerProperty() # default 0
    meeting_access = ndb.IntegerProperty() # default 1
    attendance_access = ndb.IntegerProperty() # default 0

    @classmethod
    def verify_access(cls, member_id_pass, password_pass):
        return cls.query(Access.member_id == int(member_id_pass), Access.password == password_pass)


class Member(ndb.Model):
    member_id = ndb.IntegerProperty()


class Project(ndb.Model):
    project_id = ndb.IntegerProperty()


class Meeting(ndb.Model):
    meeting_id = ndb.IntegerProperty()

class Attendance(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    member_id = ndb.IntegerProperty()
    appear = ndb.IntegerProperty() # 0 no 1 yes, default 0

class Progress(ndb.Model):
    member_id = ndb.IntegerProperty()
    project_id = ndb.IntegerProperty()
    meeting_id = ndb.IntegerProperty()


