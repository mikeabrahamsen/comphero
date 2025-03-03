from sqlalchemy import desc, asc
from flask_login import UserMixin
from server import db
import json
import hashlib
import datetime
from random import randint

'''
User Class
'''
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '{id} - {name}'.format(id=self.id, name=self.name)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        db.session.add(self)
        db.session.commit()
        return

    @staticmethod
    def exists(email):
        return User.query.filter_by(email=email).first()


'''
Checkpoint Class
'''
class Checkpoint(db.Model):
    __tablename__ = 'checkpoints'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    wcaglevels = db.Column(db.String(20))
    benefits = db.Column(db.String(40))
    regex = db.Column(db.Text())

    def __str__(self):
        return f'{self.id} - {self.name}'
    
    def __init__(self, id, name, wcaglevels, benefits, regex):
        self.id = id
        self.name = name
        self.wcaglevels = wcaglevels
        self.benefits = benefits
        self.regex = regex
        db.session.add(self)
        db.session.commit()
        return

    @staticmethod
    def get(id):
        c = Checkpoint.query.get(id)
        if c:
            checkpoint_object = {
                'id':c.id, 
                'name':c.name,
                'wcaglevels':c.wcaglevels, 
                'benefits':c.benefits,
                'regex':c.regex
                }
            return checkpoint_object
        return None
    
    @staticmethod
    def get_all():
        checkpoints_array = [{
            'id':c.id, 
            'name':c.name,
            'wcaglevels':c.wcaglevels, 
            'benefits':c.benefits,
            'regex':c.regex
            } for c in Checkpoint.query.all()]
        return checkpoints_array


class Report(db.Model):
  __tablename__ = 'reports'

  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.Text())
  results = db.Column(db.Text())
  hashid = db.Column(db.String(200))

  def __init__(self, url):
    self.url = url
    reportstring = f'{url}-{str(datetime.datetime.now())}-{randint(0, 1000)}'
    self.hashid = hashlib.sha256(reportstring.encode('utf-8')).hexdigest()
    return
  
  @staticmethod
  def fetch(reportid):
    return Report.query.filter_by(hashid=reportid).first()
  
  def update_results(self, results):
    self.results = results
    db.session.add(self)
    db.session.commit()
    return self

  def get_json_results(self):
    return json.loads(self.results.replace("'",'"'))