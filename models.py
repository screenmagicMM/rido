import dateutil.parser

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
        

class Task(Base):
    """
        Takes Tasks so that requsts can work async
        We can track the status
            Status: NOTSTART
                    STARTED
                    PROCESSING
    """
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    status = Column(String(50))

    def __init__(self, name=None):
        self.name = name
        self.status = 'NOTSTART'

    def __repr__(self):
        return '<Task %r>' % (self.name)

class AdminUser(object):
    """
    User Object Gives Info to Flask-adminLTE User Info.
    """
    full_name = "Sandip More"
    avatar = "/static/img/avatar.png"
    created_at = dateutil.parser.parse("November 28, 2016")

            
