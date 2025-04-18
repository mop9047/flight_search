from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

main = Blueprint('mainStaff', __name__)

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
    return render_template('staff/home_airlineStaff.html', username=name, posts=data1)

@main.route('/home_airlineStaff_airport', methods = ['GET','POST'])
def home_staff_airport():
    return render_template('staff/home_airlineStaff_airport.html',username=session['username'])

@main.route('/home_airlineStaff_airplane', methods = ['GET','POST'])
def home_staff_airplane():
    return render_template('staff/home_airlineStaff_airplane.html',username=session['username'])

@main.route('/home_airlineStaff_change', methods = ['GET','POST'])
def home_staff_change():
    return render_template('staff/home_airlineStaff_change.html',username=session['username'])

@main.route('/home_airlineStaff_create', methods = ['GET','POST'])
def home_staff_create():
    return render_template('staff/home_airlineStaff_create.html',username=session['username'])

@main.route('/home_airlineStaff_rating', methods = ['GET','POST'])
def home_staff_rating():
    return render_template('staff/home_airlineStaff_rating.html',username=session['username'])

@main.route('/home_airlineStaff_report', methods = ['GET','POST'])
def home_staff_report():
    return render_template('staff/home_airlineStaff_report.html',username=session['username'])

@main.route('/home_airlineStaff_view', methods = ['GET','POST'])
def home_staff_view():
    return render_template('staff/home_airlineStaff_view.html',username=session['username'])