from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

main = Blueprint('mainCust', __name__)

@main.route('/home_customer', methods = ['GET','POST'])
def home_cust():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone() 
    
    cursor.close()
    return render_template('customer/home_customer.html', username=data['name'], posts=data)

@main.route('/home_customer_flight', methods = ['GET','POST'])
def home_cust_flight():
    return render_template('customer/home_customer_flight.html',username=session['username'])

@main.route('/home_customer_search', methods = ['GET','POST'])
def home_cust_search():
    return render_template('customer/home_customer_search.html',username=session['username'])

@main.route('/home_customer_rate', methods = ['GET','POST'])
def home_cust_rate():
    return render_template('customer/home_customer_rate.html',username=session['username'])