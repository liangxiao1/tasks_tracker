from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship
import datetime
from flask import g

def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

class TaskType(Model):
    '''
    general use: table for specify task types, eg. bug_verify, bug_update, mail_new, mail_reply
    meeting_traing, meeting_attender, meeting_orgnizer,meeting_presenter
    '''
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)

    def __repr__(self):
        return self.name

class TaskStatus(Model):
    '''
    general use: table for specify failure status, like CLOSED, OPEN, PENDING, DEFERRED, INPROGRESS
    '''
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)

    def __repr__(self):
        return self.name

def get_user():
    return g.user.username

class TaskRecord(Model):
    '''
    table for storing tasks
    '''
    task_id = Column(Integer, primary_key=True)
    user_name = Column(String(50),default=get_user)
    taskstatus_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    task_status = relationship("TaskStatus")
    task_type_id = Column(Integer, ForeignKey("task_type.id"), nullable=False)
    task_type = relationship("TaskType")
    task_subject = Column(String(200))
    task_describtion = Column(String(200))
    create_date = Column(Date, default=today, nullable=False)
    update_date = Column(Date, default=today, nullable=False)
    comments = Column(String)

class Client(User):
    __tablename__ = "ab_user"
    extra = Column(String(50), unique=True, nullable=False)
