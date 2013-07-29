
import os
import re
import cgi
import time
import webapp2
import jinja2
from google.appengine.ext import db
import hashlib
import urllib2
from xml.dom import minidom

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


class BaseHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))  


class Wiki(db.Model):
  title = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)


class MainPage(BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.render_front()

class Signup(BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.render_front()

class Login(BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.render_front()

class Logout(BaseHandler):
  def render_front(self):
    self.render("index.html")


  def get(self):
    self.render_front()

class EditPage(BaseHandler):

  def render_front(self, subject="", content="", error=""):
    self.render("wiki_form.html", subject=subject, content=content, error=error)
  
  def get(self, wikipage):
    wikis = db.GqlQuery("SELECT * FROM Wiki ORDER BY created DESC")
    for wiki in wikis:
      if wiki.title == wikipage[1:]:
        self.render_front(subject=wiki.title, content=wiki.content)
        break
    else:
        self.render_front(subject=wikipage[1:])

  def post(self, wikipage):
    title_post = self.request.get('subject')
    content_post = self.request.get('content')

    if title_post and content_post:
      w = Wiki(title=title_post, content=content_post)
      w.put()
      self.redirect('/%s' %title_post)
    else:
      self.render_front(self, subject=title_post, content=content_post, error="Please enter some content")

class WikiPage(BaseHandler):

  def render_front(self, subject="", content=""):
    self.render("wiki.html", subject=subject, content=content)
  
  def get(self, wikipage):
    wikis = db.GqlQuery("SELECT * FROM Wiki ORDER BY created DESC")
    for wiki in wikis:
      if wiki.title == wikipage[1:]:
        self.render_front(subject=wiki.title, content=wiki.content)
        break
    else:
        self.redirect('_edit' + wikipage)


class TestPage(BaseHandler):
  def get(self):
    self.response.out.write(self.request.get('title'))




#######################################################################################
###########URL HANDLER#################################################################            
PAGE_RE = '(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([ ('/', MainPage),
                                ('/signup', Signup),
                                ('/login', Login),
                                ('/logout', Logout),
                                ('/test', TestPage),
                                ('/_edit' + PAGE_RE, EditPage),
                                (PAGE_RE, WikiPage),
                                ],
                              debug=True)


















    













