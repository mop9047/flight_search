from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from .main import protected_staff

main = Blueprint('mainStaff', __name__)

@main.route('/home_staff', methods = ['GET','POST'])
@protected_staff
def home_staff():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT f_name, Airline_name FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    
    for each in data1:
        name = each['f_name']
    
    cursor.close()
    return render_template('staff/home_airlineStaff.html', username=name, posts=data1)

@main.route('/home_airlineStaff_view', methods = ['GET','POST'])
@protected_staff
def home_staff_view():
    if 'username' in session:
        username = session['username']
        if 'data' in session:
            data = session['data']
            if len(data) > 0:
                filters = session['search_filters']
                return render_template('staff/home_airlineStaff_view.html',username=username, flights=data, filters=filters)
            else:
                return render_template('staff/home_airlineStaff_view.html',username=username, error='No Flights Found!')
        else:
            return render_template('staff/home_airlineStaff_view.html',username=username)
    else:
        return render_template('staff/home_airlineStaff_view.html',error='No Session')

@main.route('/home_airlineStaff_create', methods = ['GET','POST'])
@protected_staff
def home_staff_create():
    return render_template('staff/home_airlineStaff_create.html',username=session['username'],usertype=session['usertype'],airline=session['airline'])

@main.route('/home_airlineStaff_airport', methods = ['GET','POST'])
@protected_staff
def home_staff_airport():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        airport_id = request.form.get('Airport_id')
        name = request.form.get('name')
        city = request.form.get('city')
        country = request.form.get('country')
        if not airport_id or not name or not city or not country:
            error = "All fields are required."
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        cursor = current_app.config['db'].cursor()
        query_check = 'SELECT * FROM Airport WHERE airport_id = %s'
        cursor.execute(query_check, (airport_id,))
        existing_airport = cursor.fetchone()
        if existing_airport:
            error = "Airport ID already exists."
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        query_insert = """
            INSERT INTO Airport (airport_id, name, city, country)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query_insert, (airport_id, name, city, country))
            current_app.config['db'].commit()
            success = "Airport added successfully!"
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], success=success)
        except Exception as e:
            current_app.config['db'].rollback()
            error = f"Database error: {e}"
            return render_template('staff/home_airlineStaff_airport.html', username=session['username'], error=error)
        finally:
            cursor.close()
    else:
        return render_template('staff/home_airlineStaff_airport.html', username=session['username'])

@main.route('/home_airlineStaff_airplane', methods = ['GET','POST'])
@protected_staff
def home_staff_airplane():
    return render_template('staff/home_airlineStaff_airplane.html',username=session['username'])

@main.route('/home_airlineStaff_change', methods = ['GET','POST'])
@protected_staff
def home_staff_change():
    print('here')
    username = session['username']
    airline = session['airline']

    success = False #default value
    if 'success' in session:
        success = session['success']
        session.pop('success')

    cursor = current_app.config['db'].cursor();
    query = 'SELECT flight_no,departure_date_and_time,departure_airport_id,arrival_airport_id,arrival_date_and_time,status \
          FROM Flight WHERE Airline_Name = %s AND departure_date_and_time >= NOW()'
    cursor.execute(query, (airline))
    data1 = cursor.fetchall()
    # print("dad",data1)
    cursor.close()
    return render_template('staff/home_airlineStaff_change.html',username=username,flights = data1, success=success)

@main.route('/home_airlineStaff_rating', methods = ['GET','POST'])
@protected_staff
def home_staff_rating():
    return render_template('staff/home_airlineStaff_rating.html',username=session['username'])

@main.route('/home_airlineStaff_report', methods = ['GET','POST'])
@protected_staff
def home_staff_report():
    return render_template('staff/home_airlineStaff_report.html',username=session['username'])

