from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    # redirect the home page to home_customer or home_staff
    usertype = session['usertype']
    if usertype == 'staff':
        return redirect(url_for('main.home_staff'))
    elif usertype == 'customer':
        return redirect(url_for('main.home_cust'))

@main.route('/home_customer', methods = ['GET','POST'])
def home_cust():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 
    
    cursor.close()
    return render_template('home_customer.html', username=data['name'], posts=data)

@main.route('/home_staff', methods = ['GET','POST'])
def home_staff():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT f_name FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    
    for each in data1:
        name = each['f_name']
    
    cursor.close()
    return render_template('home_airlineStaff.html', username=name, posts=data1)
     
		
@main.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = current_app.config['db'].cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	current_app.config['db'].commit()
	cursor.close()
	return redirect(url_for('main.home'))

@main.route('/logout')
def logout():
    session.pop('username')
    session.pop('usertype')
    return redirect('/')