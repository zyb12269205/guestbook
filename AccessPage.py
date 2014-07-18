__author__ = 'yingbozhan'


import cgi
import datetime
import webapp2
from data_access import access_key, Access

class AccessPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    self.response.out.write("""
          <form action="/login" method="post">
            <div>Member ID: <input type="text" name="member_id"></div>
            <div>Password: <input type="text" name="password"></div>
            <div><input type="submit" value="Login"></div>
          </form>
          <form action="/signup" method="post">
            <div>Member ID: <input type="text" name="member_id"></div>
            <div>Password: <input type="text" name="password"></div>
            <div><input type="submit" value="Sign Up"></div>
          </form>
        </body>
      </html>""")

class Login(webapp2.RequestHandler):
  def post(self):
    access = Access(parent=access_key)
    access_detail = access.verify_access(self.request.get('member_id'), self.request.get('password'))
    if access_detail:
        self.redirect('/home')
    else:
        self.redirect('/')


class SignUp(webapp2.RequestHandler):
  def post(self):
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

