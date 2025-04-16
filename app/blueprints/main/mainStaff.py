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
    return render_template('home_airlineStaff.html', username=name, posts=data1)