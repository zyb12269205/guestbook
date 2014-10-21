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

    def project_name_dict(self):
        projects = self.get_all()
        project_dict = {}
        for project in projects:
            project_dict[project.project_id] = project.project_name
        return project_dict


class Meeting(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    meeting_time = ndb.StringProperty()


    def get_all(cls):
        list_meetings = []
        for meeting in cls.query().fetch():
            if meeting.meeting_id is not None and int(meeting.meeting_id) > 0:
                list_meetings.append(meeting)
        return list_meetings

    def meeting_dict(self):
        meeting_dict = {}
        for meeting in self.query().fetch():
            if meeting.meeting_id is not None and int(meeting.meeting_id) > 0:
                meeting_dict[int(meeting.meeting_id)] = meeting.meeting_time
        return meeting_dict

class Attendance(ndb.Model):
    meeting_id = ndb.IntegerProperty()
    member_id = ndb.IntegerProperty()
    attend = ndb.IntegerProperty()

    def get_all(self):
        list_attendance = []
        member_dict = Member(parent=member_key).member_name_dict()
        meeting_dict = Meeting(parent=meeting_key).meeting_dict()
        attendance_dict = {}
        for meeting_id in meeting_dict.keys():
            for member_id in member_dict.keys():
                id = str(member_id)+'$'+str(meeting_id)
                attendance_dict[id] = {
                    'meeting_id': meeting_id,
                    'member_id': member_id,
                    'member_name': member_dict[member_id],
                    'meeting_time': meeting_dict[meeting_id],
                    'attend': 0,
                    'row_id': id,
                }
        for attendance in self.query().fetch():
            id = str(attendance.member_id)+'$'+str(attendance.meeting_id)
            attendance_dict[id]['attend'] = attendance.attend

        for value in attendance_dict.values():
            list_attendance.append(value)
        return list_attendance

    def update_all(self, request):
        ids = set()
        member_dict = Member(parent=member_key).member_name_dict()
        meeting_dict = Meeting(parent=meeting_key).meeting_dict()
        for attendance in self.query().fetch():
            id = str(attendance.member_id)+'$'+str(attendance.meeting_id)
            if id in ids: continue
            ids.add(id)
            if request.get(id, None) is None: continue
            attendance.attend = 1 - int(attendance.attend)
            attendance.put()

        for member_id in member_dict.keys():
            for meeting_id in meeting_dict.keys():
                id = str(member_id)+'$'+str(meeting_id)
                if id in ids: continue
                attendance_select = Attendance(parent=attendance_key)
                attendance_select.member_id = member_id
                attendance_select.meeting_id = meeting_id
                attendance_select.attend = 0
                attendance_select.put()
                ids.add(id)
        return ids


class Progress(ndb.Model):
    member_id = ndb.IntegerProperty()
    project_id = ndb.IntegerProperty()
    meeting_id = ndb.IntegerProperty()
    complete = ndb.IntegerProperty()

    def get_all(self):
        list_progress = []
        member_dict = Member(parent=member_key).member_name_dict()
        project_dict = Project(parent=project_key).project_name_dict()
        progress_dict = {}
        for member_id in member_dict.keys():
            for project_id in project_dict.keys():
                progress_dict[str(member_id)+'$'+str(project_id)] = {
                    'member_id': member_id,
                    'project_id': project_id,
                    'member_name': member_dict[member_id],
                    'project_name': project_dict[project_id],
                    'complete': 0,
                    'row_id': str(member_id)+'$'+str(project_id)
                }

        for progress in self.query().fetch():
            id = str(progress.member_id)+'$'+str(progress.project_id)
            if id in progress_dict.keys():
                progress_dict[id]['complete'] = progress.complete

        for value in progress_dict.values():
                list_progress.append(value)

        return list_progress

    def update_all(self, request):
        ids = set()
        member_dict = Member(parent=member_key).member_name_dict()
        project_dict = Project(parent=project_key).project_name_dict()
        for progress in self.query().fetch():
            id = str(progress.member_id)+'$'+str(progress.project_id)
            if id in ids: continue
            ids.add(id)
            if request.get(id, None) is None: continue
            progress.complete = 1 - int(progress.complete)
            progress.put()


        for member_id in member_dict.keys():
            for project_id in project_dict.keys():
                id = str(member_id)+'$'+str(project_id)
                if id in ids:continue
                progress_select = Progress(parent=progress_key)
                progress_select.member_id = member_id
                progress_select.project_id = project_id
                progress_select.complete = 0
                progress_select.put()
                ids.add(id)

        return
