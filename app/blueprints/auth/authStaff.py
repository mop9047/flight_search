from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

auth = Blueprint('authStaff', __name__)

#Authenticates the login of Staff
@auth.route('/loginAuthAirlineStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE username = %s and password = md5(%s)' #md5 to hash password
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
		session['usertype'] = "staff"
		return redirect(url_for('main.home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register of Staff
@auth.route('/registerAuthAirlineStaff', methods=['GET', 'POST'])
def registerAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	f_name = request.form['f_name']
	l_name = request.form['l_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']


	#cursor used to send queries
	cursor = current_app.config['db'].cursor()
	#executes query
	query = "SELECT * FROM Airline_Staff WHERE username = %s"
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
		ins = 'INSERT INTO Airline_Staff VALUES(%s, md5(%s),%s,%s,%s,%s)'  #added md5 to hash password
		cursor.execute(ins, (username, password, f_name,l_name,date_of_birth,airline_name))
		current_app.config['db'].commit()
		cursor.close()
		return render_template('index.html')