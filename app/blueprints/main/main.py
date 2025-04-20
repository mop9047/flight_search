from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    # redirect the home page to home_customer or home_staff
    usertype = session['usertype']
    if usertype == 'customer':
        return redirect(url_for('mainCust.home_cust'))
    elif usertype == 'staff':
        return redirect(url_for('mainStaff.home_staff'))

@main.route('/logout')
def logout():
    session.pop('username')
    session.pop('usertype')
    if 'data' in session:
        session.pop('data')
    return redirect('/')