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

# Create engine and connect to DB:
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/login/')
def login():
	login_session['username'] = 'Adilbek'
	return 'This page will be for logging in.'

@app.route('/logout/')
def logout():
	del login_session['username']
	return 'You are logged out.'

@app.route('/periods/')
def showPeriods():
	if 'username' in login_session:
		login_status = 'You are logged in as user %s.<br>' % login_session['username']
	else:
		login_status = 'You are not logged in.<br>'
	return login_status + 'This page will show all my periods.'

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