from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Needed to perform CRUD operations with the database:
from database_setup import engine, Base, User, Period, Budget
from sqlalchemy.orm import sessionmaker

# Import flask components:
from flask import Flask, render_template, url_for, request, redirect, flash
# Session is a dictionary where we can store values for the longevity of
# a user's session with our server:
from flask import session as login_session
# Create an instance of class Flask, which will be our WSGI application:
app = Flask(__name__)

# Import Flask-Login extension needed for user management:
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
# Create instance of LoginManager class:
# (The login manager contains the code that lets your application and 
#  Flask-Login work together, such as how to load a user from an ID, 
#  where to send users when they need to log in, and the like.)
login_manager = LoginManager()
login_manager.init_app(app)

# Create engine and connect to DB:
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

@login_manager.user_loader
def load_user(user_id):
	'''
	Given user_id, return the corresponding user object if exists.
	If doesn't exist, return 'None' (don't raise an exception).
	'''
	userObject = db_session.query(User).filter_by(id=user_id).one()
	if userObject != []:
		return userObject
	return None

@app.route('/login/', methods=['GET','POST'])
def login():
	'''
	For GET requests, display the login form. For POST requests, 
	login the current user by processing the form. 
	'''
	user = db_session.query(User).filter_by(id=1).one()
	user.authenticated = True
	db_session.add(user)
	db_session.commit()
	login_user(user)
	return redirect(url_for('showPeriods'))

@app.route('/logout/')
@login_required
def logout():
	user = current_user
	user.authenticated = False
	db_session.add(user)
	db_session.commit()
	logout_user()
	return 'You are logged out.'

@app.route('/periods/')
@login_required
def showPeriods():
	return 'You are logged in.<br>This page will show all my periods.'

@app.route('/period/new/')
def newPeriod():
	return 'This page will be for adding a new period.'

@app.route('/period/<int:period_id>/budget/')
def showBudget(period_id):
	return 'This page will be for showing the budget for period %s' % period_id

@app.route('/period/<int:period_id>/edit/')
def editPeriod(period_id):
	return 'This page will be for editing period %s' % period_id

@app.route('/period/<int:period_id>/delete/')
def deletePeriod(period_id):
	return 'This page will be for deleting period %s' % period_id

@app.route('/period/<int:period_id>/new/')
def newBudget(period_id):
	return 'This page will be for adding a new budget for period %s' % period_id

@app.route('/period/<int:period_id>/budget/<int:budget_id>/edit')
def editBudget(period_id, budget_id):
	return 'This page will be for editing budget %s for period %s' % (budget_id, period_id)

@app.route('/period/<int:period_id>/budget/<int:budget_id>/delete')
def deleteBudget(period_id, budget_id):
	return 'This page will be for deleting budget %s for period %s' % (budget_id, period_id)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	# secret_key above is for session management
	app.debug = True
	# debug mode allows server to reload automatically after code change
	app.run(host = '0.0.0.0', port = 8000)
	# listening on all public IP, port 8000