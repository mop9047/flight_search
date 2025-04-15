from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

auth = Blueprint('auth', __name__)

#Define route for login
@auth.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@auth.route('/register')
def register():
	return render_template('register.html')

@auth.route('/register_customer')
def register_customer():
	return render_template('register_customer.html')

@auth.route('/register_staff')
def register_staff():
	return render_template('register_staff.html')

#Authenticates the login
@auth.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = md5(%s)' #md5 to hash password
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('main.home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@auth.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	usertype = request.form['user_type']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = f"SELECT * FROM {usertype} WHERE email = %s"
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO {usertype} VALUES(%s, md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'  #added md5 to hash password
		cursor.execute(ins, (username, password,))
		current_app.config['db'].commit()
		cursor.close()
		return render_template('index.html')
	
#Authenticates the login of Customer
@auth.route('/loginAuthCust', methods=['GET', 'POST'])
def loginAuthCust():
	#grabs information from the forms
	username = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and password = md5(%s)' #md5 to hash password
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('main.home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)
	
#Authenticates the register of Customer
@auth.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCust():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	name = request.form['name']
	buidling_num = request.form['building_num']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_num = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = "SELECT * FROM Customer WHERE email = %s"
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'  #added md5 to hash password
		cursor.execute(ins, (email, password, name,buidling_num,street,city,state,phone_num,passport_number,passport_expiration,passport_country,date_of_birth))
		current_app.config['db'].commit()
		cursor.close()
		return render_template('index.html')