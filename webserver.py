from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Needed to perform CRUD operations with the database:
from database_setup import engine, Base, User, Period, Budget
from sqlalchemy.orm import sessionmaker
# Func is needed for aggregations (sum, avg, max, etc.):
from sqlalchemy.sql import func

# Import flask components:
from flask import Flask, render_template, url_for, request, redirect, flash
# jsonify is a package that allows to format data for JSON end point
from flask import jsonify
# Session is a dictionary where we can store values for the longevity of
# a user's session with our server:
from flask import session as login_session
# Create an instance of class Flask, which will be our WSGI application:
app = Flask(__name__)

# Create engine and connect to DB:
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login/', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		# The request is POST. Get form data from the POST request,
		# stripping any leading and trailing whitespaces,
		# and validate all data:
		name = request.form['name'].strip()
		password = request.form['password'].strip()
		# Check if all fields are non-empty; flash an error otherwise:
		if not name or not password:
			 flash('Please enter all fields')
			 return render_template('login.html')
		# Lookup the user by email and verify the password:
		user = session.query(User).filter_by(name=name).first()
		if user == None:
			flash('Invalid user name or password')
			return render_template('login.html')
		if not user.check_password(password):
			flash('Invalid user name or password')
			return render_template('login.html')
		# Validation passed. Log the user into session:
		login_session['email'] = user.email
		# Redirect to the 'periods' page:
		return redirect(url_for('showPeriods'))

@app.route('/logout/', methods=['GET'])
def logout():
	if 'email' not in login_session:
		flash('Already logged out.')
		return redirect(url_for('login'))
	login_session.pop('email', None)
	flash('Logout successful')
	return redirect(url_for('login'))

@app.route('/')
@app.route('/home/')
def showPeriods():
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		return render_template('home.html', items=periods, username=current_user.name)

@app.route('/register/', methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		# The request is POST. Get form data from the POST request,
		# stripping any leading and trailing whitespaces,
		# and validate all data:
		name = request.form['name'].strip()
		email = request.form['email'].strip()
		password = request.form['password'].strip()
		pwdconfirm = request.form['pwdconfirm'].strip()
		# Check if all fields are non-empty; flash an error otherwise:
		if not name or not email or not password or not pwdconfirm:
			 flash('Please enter all fields')
			 return render_template('register.html')
		# Check if lengths are reasonable (between 2 and 50 chars):
		if len(name)>50 or len(email)>50 or len(password)>50 or len(pwdconfirm)>50:
			flash('Some values appear too long - try to keep things short and sweet')
			return render_template('register.html')
		if len(name)<3 or len(email)<3 or len(password)<3 or len(pwdconfirm)<3:
			flash('Some values appear too short - let\'s be more serious')
			return render_template('register.html')
		# Check if the two password entries match:
		if not password == pwdconfirm:
			flash('Password and confirmation don\'t match')
			return render_template('register.html')
		# Check if the user name already exists:
		user = session.query(User).filter_by(name=name).first()
		if user:
			flash('This user name is already registered')
			return render_template('register.html')
		# Check if the email address already exists:
		user = session.query(User).filter_by(email=email).first()
		if user:
			flash('This email address is already registered')
			return render_template('register.html')
		# Validation passed. Register account and log the user into session:
		newUser = User(name=name, email=email, password=password)
		session.add(newUser)
		session.commit()
		login_session['email'] = newUser.email
		# Redirect to the 'periods' page:
		flash('Thanks for registering! You are logged in and ready to roll.')
		return redirect(url_for('showPeriods'))	

@app.route('/period/new/', methods=['GET','POST'])
def newPeriod():
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		if request.method == 'GET':
			return render_template('period_new.html',periods=periods)
		else:
			# Get data from POST request, stripping any leading/trailing white spaces:
			period_name = request.form['period_name'].strip()
			# Check if value not empty:
			if not period_name:
				flash('Please enter period name')
				return render_template('period_new.html',periods=periods)
			# Check if length is reasonable (between 2 and 25 chars):
			if len(period_name)>25:
				flash('Period name appears too long - try to keep things short and sweet')
				return render_template('period_new.html',periods=periods)
			if len(period_name)<3:
				flash('Period name appears too short - let\'s be more serious')
				return render_template('period_new.html',periods=periods)
			# Validation passed. Add period to the database:
			current_user = session.query(User).filter_by(email=login_session['email']).first()
			newPeriod = Period(name=period_name, user_id=current_user.id) 
			session.add(newPeriod)
			session.commit()
			flash('New period created')
			return redirect(url_for('showBudget',period_id=newPeriod.id))

@app.route('/period/<int:period_id>/budget/', methods=['GET'])
def showBudget(period_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		period = session.query(Period).filter_by(id=period_id).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).\
			order_by(Period.id.desc()).all()
		budgets = session.query(Budget).filter_by(period_id=period_id).order_by(Budget.id).all()
		total_budget = session.query(func.sum(Budget.budget_amount)).\
			filter_by(period_id=period_id)
		total_actual = session.query(func.sum(Budget.actual_amount)).\
			filter_by(period_id=period_id)
		return render_template('budget.html',periods=periods,budgets=budgets,period_id=period_id,\
			total_budget=(0 if total_budget[0][0] is None else total_budget[0][0]),\
			total_actual=(0 if total_actual[0][0] is None else total_actual[0][0]),\
			period=period)
		
@app.route('/period/<int:period_id>/edit/', methods=['GET','POST'])
def editPeriod(period_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		period = session.query(Period).filter_by(id=period_id).one()
		period_name = period.name
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		if request.method == 'GET':
			return render_template('period_edit.html',periods=periods,period_id=period_id,\
				period_name=period_name)
		else:
			# Get data from POST request, stripping any leading/trailing white spaces:
			new_name = request.form['period_name'].strip()
			# Check if value not empty:
			if not new_name:
				flash('Period name cannot be empty')
				return render_template('period_edit.html',periods=periods,period_id=period_id,\
					period_name=period_name)
			# Check if length is reasonable (between 2 and 25 chars):
			if len(new_name)>25:
				flash('Period name appears too long - try to keep things short and sweet')
				return render_template('period_edit.html',periods=periods,period_id=period_id,\
					period_name=period_name)
			if len(new_name)<3:
				flash('Period name appears too short - let\'s be more serious')
				return render_template('period_edit.html',periods=periods,period_id=period_id,\
					period_name=period_name)
			# Validation passed. Update period name in the database:
			period.name = new_name
			session.add(period)
			session.commit()
			flash('Period name was updated')
			return redirect(url_for('showBudget',period_id=period_id))

@app.route('/period/<int:period_id>/delete/', methods=['GET','POST'])
def deletePeriod(period_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		period = session.query(Period).filter_by(id=period_id).one()
		period_name = period.name
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		if request.method == 'GET':
			return render_template('period_delete.html',periods=periods,period_id=period_id,\
				period_name=period_name)
		else:
			# Process the POST request.
			# Delete the period. Note that the associated budget items will be deleted
			# automatically thanks to 'cascade' option we set up in database_setup.py file:
			session.delete(period)
			session.commit()
			flash('Period "%s" was deleted' % period_name)
			return redirect(url_for('showPeriods',period_id=period_id))

@app.route('/period/<int:period_id>/new/', methods=['GET','POST'])
def newBudget(period_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		if request.method == 'GET':
			return render_template('budget_new.html',periods=periods,period_id=period_id)
		else:
			# Get data from the POST request:
			budget_name = request.form['budget_name'].strip()
			budget_amount = request.form['budget_amount']
			actual_amount = request.form['actual_amount']
			# Check if budget name is non-empty:
			if not budget_name:
				flash('Please enter the budget category name')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			# Check if length is reasonable (between 2 and 25 chars):
			if len(budget_name)>25:
				flash('Category name appears too long - try to keep things short and sweet')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			if len(budget_name)<3:
				flash('Category name appears too short - let\'s be more serious')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			# If amounts are null or empty string, set to zero:
			if budget_amount == '' or budget_amount is None:
				budget_amount = 0
			if actual_amount == '' or actual_amount is None:
				actual_amount = 0
			# Convert amounts to type integer or flash the error:
			try:
				budget_amount = int(budget_amount)
				actual_amount = int(actual_amount)
			except:
				flash('Amounts must be whole numbers, not text or decimals')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			# Check if amounts are between 0 and 1,000,000:
			if budget_amount<0 or actual_amount<0:
				flash('Amounts cannot be negative')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			if budget_amount>1000000 or actual_amount>1000000:
				flash('Amount greater than 1,000,000 - are you serious?')
				return render_template('budget_new.html',periods=periods,period_id=period_id)
			# Validation passed. Add budget to the database:
			newBudget = Budget(period_id=period_id,name=budget_name,budget_amount=budget_amount,\
				actual_amount=actual_amount)
			session.add(newBudget)
			session.commit()
			flash('New budget category was added')
			return redirect(url_for('showBudget',period_id=period_id))

@app.route('/period/<int:period_id>/budget/<int:budget_id>/edit', methods=['GET','POST'])
def editBudget(period_id, budget_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		budget = session.query(Budget).filter_by(id=budget_id).first()
		if request.method == 'GET':
			return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
		else:
			# Get data from the POST request:
			budget_name = request.form['budget_name'].strip()
			budget_amount = request.form['budget_amount']
			actual_amount = request.form['actual_amount']
			# Check if budget name is non-empty:
			if not budget_name:
				flash('Please enter the budget category name')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			# Check if length is reasonable (between 2 and 25 chars):
			if len(budget_name)>25:
				flash('Category name appears too long - try to keep things short and sweet')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			if len(budget_name)<3:
				flash('Category name appears too short - let\'s be more serious')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			# If amounts are null or empty string, set to zero:
			if budget_amount == '' or budget_amount is None:
				budget_amount = 0
			if actual_amount == '' or actual_amount is None:
				actual_amount = 0
			# Convert amounts to type integer or flash the error:
			try:
				budget_amount = int(budget_amount)
				actual_amount = int(actual_amount)
			except:
				flash('Amounts must be whole numbers, not text or decimals')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			# Check if amounts are between 0 and 1,000,000:
			if budget_amount<0 or actual_amount<0:
				flash('Amounts cannot be negative')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			if budget_amount>1000000 or actual_amount>1000000:
				flash('Amount greater than 1,000,000 - are you serious?')
				return render_template('budget_edit.html',periods=periods,period_id=period_id,budget=budget)
			# Validation passed. Update budget in the database:
			budget.name = budget_name
			budget.budget_amount = budget_amount
			budget.actual_amount = actual_amount
			session.add(budget)
			session.commit()
			flash('Budget category was updated')
			return redirect(url_for('showBudget',period_id=period_id))		

@app.route('/period/<int:period_id>/budget/<int:budget_id>/delete', methods=['GET','POST'])
def deleteBudget(period_id, budget_id):
	if 'email' not in login_session:
		# User not logged in:
		return render_template('notauthorized.html')
	user = session.query(User).filter_by(email=login_session['email']).first()
	if user is None:
		# For rare cases when user is deleted while still in session:
		return render_template('notregistered.html')
	else:
		current_user = session.query(User).filter_by(email=login_session['email']).first()
		periods = session.query(Period).filter_by(user_id=current_user.id).order_by(Period.id.desc())
		budget = session.query(Budget).filter_by(id=budget_id).first()
		budget_name = budget.name
		if request.method == 'GET':
			return render_template('budget_delete.html',periods=periods,period_id=period_id,\
				budget_id=budget_id,budget_name=budget_name)
		else:
			# Process the POST request:
			session.delete(budget)
			session.commit()
			flash('Category "%s" was deleted' % budget_name)
			return redirect(url_for('showBudget',period_id=period_id))

# Making an API Endpoint (GET Request)
@app.route('/JSON')
def budgetItems():
	items = session.query(Budget).all()
	return jsonify(BudgetItems=[i.serialize for i in items])

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	# secret_key above is for session management
	app.debug = True
	# debug mode allows server to reload automatically after code change
	app.run(host = '0.0.0.0', port = 8000)
	# listening on all public IP, port 8000