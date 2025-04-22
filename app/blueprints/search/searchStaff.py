from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

search = Blueprint('searchStaff', __name__)

@search.route('/searchFlightsStaff', methods = ['GET','POST'])
def search_staff():
    #grabs information from the forms
    username = session['username']
	
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    source = request.form['source']
    destination = request.form['destination']
    status = request.form['status']
	

	#cursor used to send queries
    cursor = current_app.config['db'].cursor()
	#executes query
    # query = "Select Airline_Name AS Airline, \
    #       flight_no AS Flight FROM Flight WHERE 1=1"
    query = "Select Airline_Name AS Airline,\
         flight_no AS Flight, \
            departure_date_and_time AS Departure_Date, \
         departure_airport_id AS Departure, \
             arrival_airport_id AS Arrival, \
                arrival_date_and_time AS Arrival_Date, \
                     status, base_price, \
                         Airplane_airline_name AS AA_name, \
                             Airplane_id FROM Flight WHERE 1=1"
	
    params = []
    filters = ["No Filters"]
        
    if start_date:
        query += " AND departure_date_and_time >= %s"
        params.append(start_date)
        filters.append('From ' + start_date)

    if end_date:
        query += " AND departure_date_and_time <= %s"
        params.append(end_date)
        filters.append('To ' + end_date)

    if source:
        query += " AND departure_airport_id = %s"
        params.append(source)
        filters.append('Departure: ' + source)

    if destination:
        query += " AND arrival_airport_id = %s"
        params.append(destination)
        filters.append('Arrival: ' + destination)

    if status:
        query += " AND `status` = %s"
        params.append(status)
        filters.append('Status: ' + status)
    # query = 'SELECT * FROM Flight WHERE departure_airport_id =%s AND Airline_Name \
	# 	= (SELECT Airline_name FROM Airline_Staff WHERE username=%s)'
    
    if not len(filters) == 1:
        filters = filters[1:]

    cursor.execute(query, params)
	#stores the results in a variable
    data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
	
    if('username' in session):
		#creates a session for the the user
		#session is a built in
        session['data'] = data
        session['search_filters'] = filters
        return redirect(url_for('mainStaff.home_staff_view'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)
    
@search.route('/editFiltersStaff', methods = ['GET','POST'])
def edit_filter_staff():
    session.pop('data')
    return redirect(url_for('mainStaff.home_staff_view'))