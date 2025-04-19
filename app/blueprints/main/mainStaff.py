from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
<<<<<<< HEAD
=======
from datetime import datetime
>>>>>>> search_func_And_cust_func

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

<<<<<<< HEAD
@main.route('/home_airlineStaff_change', methods = ['GET','POST'])
def home_staff_change():
    return render_template('staff/home_airlineStaff_change.html',username=session['username'])

=======
>>>>>>> search_func_And_cust_func
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
<<<<<<< HEAD
    return render_template('staff/home_airlineStaff_view.html',username=session['username'])
=======
    return render_template('staff/home_airlineStaff_view.html',username=session['username'])

@main.route('/staff_search_flights', methods=['POST'])
def staff_search_flights():
    # Get the staff's airline
    username = session['username']
    cursor = current_app.config['db'].cursor()
    query = 'SELECT Airline_name FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, (username,))  # Fixed: Add comma to make it a tuple
    staff_airline = cursor.fetchone()['Airline_name']
    
    # Get search parameters from form
    flight_number = request.form.get('flight_number', '')
    departure_date = request.form.get('departure_date', '')
    departure_airport = request.form.get('departure_airport', '')
    arrival_airport = request.form.get('arrival_airport', '')
    
    # Base query - Modified to include the airline condition
    query = '''
    SELECT f.Airline_Name, f.flight_no, f.departure_date_and_time, f.arrival_date_and_time, 
        a1.name as departure_airport, a2.name as arrival_airport, 
        a1.city as departure_city, a2.city as arrival_city, f.base_price, f.status
    FROM Flight f 
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE (a1.Airport_id = %s ) 
    AND (a2.Airport_id = %s )
    AND (f.flight_no= %s)
    AND DATE(f.departure_date_and_time) = %s
    '''
    
    # List to store query parameters
    params = [staff_airline]

    
    # Execute query
    # Execute query for outbound flights
    cursor.execute(query, (departure_airport, arrival_airport, flight_number,departure_date))
    flights = cursor.fetchall()
    
    return render_template('staff/home_staff_search.html', username=session['username'], flights=flights)

@main.route('/edit_flight/<airline>/<flight_no>/<departure_time>', methods=['GET', 'POST'])
def edit_flight(airline, flight_no, departure_time):
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('auth.login'))
        
    # Get the flight details from the database
    cursor = conn.cursor()
    query = '''SELECT * FROM flight 
               WHERE airline_name = %s 
               AND flight_num = %s 
               AND departure_date_and_time = %s'''
    cursor.execute(query, (airline, flight_no, departure_time))
    flight = cursor.fetchone()
    
    if request.method == 'POST':
        # Get form data
        status = request.form.get('status')
        # Add other fields you want to be editable
        
        # Update flight in the database
        update_query = '''UPDATE flight 
                          SET status = %s
                          WHERE airline_name = %s 
                          AND flight_num = %s 
                          AND departure_date_and_time = %s'''
        cursor.execute(update_query, (status, airline, flight_no, departure_time))
        conn.commit()
        
        # Redirect back to the search flights page with a success message
        flash('Flight updated successfully!', 'success')
        return redirect(url_for('mainStaff.staff_search_flights'))
    
    # Render the edit flight template with the flight details
    return render_template('staff/home_airlineStaff_edit_flight.html', 
                          username=session['username'], 
                          flight=flight)
>>>>>>> search_func_And_cust_func
