from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Needed to perform CRUD operations with the database:
from database_setup import engine, Base, User, Period, Budget
from sqlalchemy.orm import sessionmaker

# Import flask components:
from flask import Flask, render_template, url_for, request, redirect, flash
# Create an instance of class Flask, which will be our WSGI application:
app = Flask(__name__)

# Create engine and connect to DB:
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/periods/')
def showPeriods():
	return 'This page will show all my periods.'

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
	app.debug = True
	# debug mode allows server to reload automatically after code change
	app.run(host = '0.0.0.0', port = 8000)
	# listening on all public IP, port 8000