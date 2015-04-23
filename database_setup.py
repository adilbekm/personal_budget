
# IMPORT LIBRARIES # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# Creating the base class - to be used to define any number of
# mapped classes (tables):
Base = declarative_base()

# MAP DATABASE OBJECTS TO PYTHON CLASSES # # # # # # # # # # # # # #
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	password = Column(String(20))
	email = Column(String(100), nullable=False)
	# This attribute is needed for flask-login:
	authenticated = Column(Boolean, default=False)
	# This method is needed for flask-login:
	def is_active(self):
		return True
	# This method is needed for flask-login:
	def get_id(self):
		return self.id
	# This method is needed for flask-login:
	def is_authenticated(self):
		return self.authenticated
	# This method is needed for flask-login:
	def is_anonymous(self):
		return False

class Period(Base):
	__tablename__ = 'period'
	id = Column(Integer, primary_key=True) 
	user_id = Column(Integer, ForeignKey('user.id'))
	name = Column(String(50), nullable=False)
	user = relationship(User)

class Budget(Base):
	__tablename__ = 'budget'
	id = Column(Integer, primary_key=True)
	period_id = Column(Integer, ForeignKey('period.id'))
	user_id = Column(Integer, ForeignKey('user.id'))
	budget_amount = Column(Integer)
	actual_amount = Column(Integer)
	period = relationship(Period)
	user = relationship(User)

# CONFIGURATION # # # # # # # # # # # # # # # # # # # # # # # # # #
# To establish lazy connection to the database:
engine = create_engine('postgresql:///personalbudget')
# To create tables in the database if they don't exist yet:
Base.metadata.create_all(engine)
