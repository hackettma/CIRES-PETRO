import os
import re
import cgi
import time
import webapp2
import jinja2
from google.appengine.ext import db
import hashlib
import hmac
import urllib2
import random
from string import letters
from xml.dom import minidom

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
secret = 'asdfkjIOJKNNDdkajdaskjov23e89172389fnuynjkdkjh'

def valid_username(user_name):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    if USER_RE.match(user_name):
        return True
    else:
        return False

def valid_pwd(pwd):
    PWD_RE = re.compile(r"^.{3,20}$")
    if PWD_RE.match(pwd):
        return True
    else:
        return False

def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    if email == "":
      return True
    elif EMAIL_RE.match(email):
        return True
    else:
        return False

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    params['user'] = self.user
    return render_str(template, **params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))  

  def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

  def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

  def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

  def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

  def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u




class Signup(BaseHandler):
  def get(self, user_name="", err_usr="", err_pwd="", err_cnfrm="", err_eml=""):
    self.render("user_form.html", user_name=user_name, err_usr=err_usr, err_pwd=err_pwd, err_cnfrm=err_cnfrm, err_eml=err_eml)

  def post(self):
      user_name_in = self.request.get('username')
      user_pwd = self.request.get('password')
      user_cnfrm_pwd = self.request.get('verify')
      user_email = self.request.get('email')

      error_usr_txt = "Invalid Username"
      error_pwd_txt = "Invalid Password"
      error_cnfrm_txt = "Password does not match"
      error_email_txt = "Invalid email address"
      out_params = {}
      out_params['username'] = user_name_in


      user = User.by_name(user_name_in)

      if valid_username(user_name_in) and not user:
        if valid_pwd(user_pwd):
          if user_pwd == user_cnfrm_pwd:
            if valid_email(user_email):
              user = User.register(user_name_in, user_pwd, user_email)
              user.put()
              self.login(user)
              self.redirect("/")
            else:
              out_params['err_eml'] = error_email_txt
              self.render('user_form.html', **out_params)    
          else:
            out_params['err_cnfrm'] = error_cnfrm_txt
            self.render('user_form.html', **out_params)
        else:
          out_params['err_pwd'] = error_pwd_txt
          out_params['err_usr'] = error_usr_txt
          self.render('user_form.html', **out_params)
      else:
        out_params['err_usr'] = error_usr_txt
        self.render('user_form.html', **out_params)

class Login(BaseHandler):

  def get(self, user_name="", err_usr="", err_pwd=""):
    self.render("login_form.html", user_name=user_name, err_usr=err_usr, err_pwd=err_pwd)

  def post(self):
    username = self.request.get('username')
    pwd = self.request.get('password')

    user = User.login(username, pwd)
    if user:
      self.login(user)
      self.redirect('/')
    else:
      params = {'user_name': username, 'err_usr':"Username invalid", 'err_pwd': "Password Invalid"}
      self.render("login_form.html",**params)


class Logout(BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.logout()
    self.redirect('/')


class Project(db.Model):
    proj_name = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    notes = db.TextProperty()

    @classmethod
    def by_id(cls, pid, uid):
        return Project.get_by_id(pid, parent = uid)

    @classmethod
    def by_name(cls, name):
        p = Project.all().filter('name =', name).get()
        return p

class MainPage (BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.render_front()

class ShowProjects(BaseHandler):
  def render_front(self, projects=""):
    self.render("projects.html", projects=projects)


  def get(self):
    p = Project.all().ancestor(self.user)
    z = p.get()
    if z:
      self.render_front(p)
    else:
      self.redirect('/projects/create')
    
class CreateProject(BaseHandler):
  def render_front(self):
    self.render("create_project.html")


  def get(self):
    self.render_front()

  def post(self):
    proj_name = self.request.get("proj_name")
    author = self.request.get("Author")
    notes = self.request.get("Notes")
    

    p = Project(parent=self.user, proj_name=proj_name, author=author, notes=notes)
    p.put()
    self.redirect('/projects')

class Record(db.Model):
    UWI = db.StringProperty(required = True)
    Lease_name = db.StringProperty(required = True)
    notes = db.TextProperty()

    @classmethod
    def by_id(cls, pid, uid):
        return Project.get_by_id(pid, parent = uid)

    @classmethod
    def by_name(cls, name):
        p = Project.all().filter('name =', name).get()
        return p

#######################################################################################
###########URL HANDLER#################################################################  
PAGE_RE = '(/(?:[a-zA-Z0-9_-]+/?)*)'          
app = webapp2.WSGIApplication([ ('/', MainPage),
                                ('/signup', Signup),
                                ('/login', Login),
                                ('/logout', Logout),
                                ('/projects', ShowProjects),
                                ('/projects/create', CreateProject),
                                #('/projects/import', ImportProject),
                                ('/projects/'+ PAGE_RE, ShowProjectRecords),
                                ('/projects/records/edit', EditProjectRecords)
                                ],
                              debug=True)







