from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from datetime import datetime, timedelta

main = Blueprint('mainCust', __name__)

@main.route('/home_customer', methods = ['GET','POST'])
def home_cust():
    username = session['username']

    cursor = current_app.config['db'].cursor();
    query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(query, username)  
    data = cursor.fetchone() 
    
    cursor.close()
    return render_template('customer/home_customer.html', username=data['name'], posts=data)




@main.route('/home_customer_search', methods = ['GET','POST'])
def home_cust_search():
    return render_template('customer/home_customer_search.html', username=session['username'])

@main.route('/customer_search_flights', methods = ['POST'])
def customer_search_flights():
    # Get search parameters from form
    source = request.form.get('source', '')
    destination = request.form.get('destination', '')
    departure_date = request.form.get('departure_date', '')
    return_date = request.form.get('return_date', '')
    
    # Debug log to verify form data
    print(f"Search params - Source: {source}, Destination: {destination}, Departure: {departure_date}, Return: {return_date}")
    
    # Validate form inputs
    if not source or not destination or not departure_date:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="All search fields are required except return date")
    
    # Cursor for database queries
    cursor = current_app.config['db'].cursor()
    
    # Check if airports/cities exist
    check_query = '''
    SELECT COUNT(*) as count FROM Airport 
    WHERE Airport_id = %s OR city = %s
    '''
    cursor.execute(check_query, (source, source))
    source_exists = cursor.fetchone()['count'] > 0
    
    cursor.execute(check_query, (destination, destination))
    destination_exists = cursor.fetchone()['count'] > 0
    
    if not source_exists:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="Departure airport or city not found")
    
    if not destination_exists:
        return render_template('customer/home_customer_search.html', 
                             username=session['username'],
                             error="Arrival airport or city not found")
    
    # Base query for outbound flights
    query = '''
    SELECT f.Airline_Name, f.flight_no, f.departure_date_and_time, f.arrival_date_and_time, 
        a1.name as departure_airport, a2.name as arrival_airport, 
        a1.city as departure_city, a2.city as arrival_city, f.base_price, f.status
    FROM Flight f 
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE (a1.city = %s OR a1.name = %s) 
    AND (a2.city = %s OR a2.name = %s)
    AND DATE(f.departure_date_and_time) = %s
    '''
    
    # Execute query for outbound flights
    cursor.execute(query, (source, source, destination, destination, departure_date))
    flights = cursor.fetchall()
    
    # If return date is provided, search for return flights
    return_flights = None
    if return_date:
        cursor.execute(query, (destination, destination, source, source, return_date))
        return_flights = cursor.fetchall()
    
    cursor.close()
    
    # Debug log to verify results
    print(f"Found {len(flights)} outbound flights and {len(return_flights) if return_flights else 0} return flights")
    
    return render_template('customer/home_customer_search.html', 
                          username=session['username'], 
                          flights=flights,
                          return_flights=return_flights)

@main.route('/home_customer_rate', methods = ['GET','POST'])
def home_cust_rate():
    return render_template('customer/home_customer_rate.html', username=session['username'])

@main.route('/book_flight', methods=['POST'])
def book_flight():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Get flight details from form
    airline = request.form.get('airline')
    flight_no = request.form.get('flight_no')
    departure_time = request.form.get('departure_time')
    
    # Get the base price from the flight
    cursor = current_app.config['db'].cursor()
    query = 'SELECT base_price FROM Flight WHERE Airline_Name = %s AND flight_no = %s AND departure_date_and_time = %s'
    cursor.execute(query, (airline, flight_no, departure_time))
    flight_data = cursor.fetchone()
    cursor.close()
    
    if not flight_data:
        # Flight not found
        return redirect(url_for('mainCust.home_cust_search'))
    
    base_price = flight_data['base_price']
    
    # To do: Calculate the sold price based on other factors 
    sold_price = base_price
    
    # Store flight booking details in session for payment page
    session['booking'] = {
        'airline': airline,
        'flight_no': flight_no,
        'departure_time': departure_time,
        'sold_price': sold_price
    }
    
    # Redirect to payment page
    return redirect(url_for('mainCust.payment_page'))

@main.route('/payment_page', methods=['GET'])
def payment_page():
    if 'username' not in session or 'booking' not in session:
        return redirect(url_for('auth.login'))
    
    booking = session['booking']
    return render_template('customer/payment_page.html', 
                          username=session['username'],
                          booking=booking)

@main.route('/process_payment', methods=['POST'])
def process_payment():
    if 'username' not in session or 'booking' not in session:
        return redirect(url_for('auth.login'))
    
    # Get booking details from session
    booking = session['booking']
    airline = booking['airline']
    flight_no = booking['flight_no']
    departure_time = booking['departure_time']
    sold_price = booking['sold_price']
    customer_email = session['username']
    
    # Get payment details from form
    card_type = request.form.get('card_type')
    card_num = request.form.get('card_num')
    name_on_card = request.form.get('name_on_card')
    card_expiry_date = request.form.get('card_expiry_date')
    
    # Validate payment details
    if not card_type or not card_num or not name_on_card or not card_expiry_date:
        return render_template('customer/payment_page.html', 
                             username=session['username'],
                             booking=booking,
                             error="All payment fields are required")
    
    # Generate a ticket ID
    import uuid
    ticket_id = str(uuid.uuid4())[:20]
    
    # Insert ticket record with payment details
    cursor = current_app.config['db'].cursor()
    try:
        # Start a transaction
        current_app.config['db'].begin()
        
        # Insert into Ticket table with payment details
        ticket_query = '''
        INSERT INTO Ticket (ticket_id, sold_price, card_type, card_num, name_on_card, card_expiry_date, 
                          Airline_name, flight_no, departure_date_and_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(ticket_query, (
            ticket_id, sold_price, card_type, card_num, name_on_card, card_expiry_date,
            airline, flight_no, departure_time
        ))
        
        # Insert into Purchases table
        purchase_query = '''
        INSERT INTO Purchases (ticket_id, email, date_and_time)
        VALUES (%s, %s, %s)
        '''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(purchase_query, (ticket_id, customer_email, current_time))
        
        # Commit the transaction
        current_app.config['db'].commit()
        
        # Clear booking data from session
        session.pop('booking', None)
        
        # Redirect to booking confirmation page
        return redirect(url_for('mainCust.booking_confirmation', ticket_id=ticket_id))
        
    except Exception as e:
        # If there's an error, rollback the transaction
        current_app.config['db'].rollback()
        print(f"Error processing payment: {e}")
        return render_template('customer/payment_page.html', 
                             username=session['username'],
                             booking=booking,
                             error=f"Payment processing error: {e}")
    
    finally:
        cursor.close()

@main.route('/booking_confirmation/<ticket_id>', methods=['GET'])
def booking_confirmation(ticket_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Get ticket details from database
    cursor = current_app.config['db'].cursor()
    query = '''
    SELECT t.ticket_id, t.sold_price, t.Airline_name, t.flight_no, t.departure_date_and_time,
           f.arrival_date_and_time, a1.name as departure_airport, a2.name as arrival_airport
    FROM Ticket t
    JOIN Flight f ON t.Airline_name = f.Airline_Name AND t.flight_no = f.flight_no 
                  AND t.departure_date_and_time = f.departure_date_and_time
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE t.ticket_id = %s
    '''
    
    cursor.execute(query, (ticket_id,))
    ticket_data = cursor.fetchone()
    cursor.close()
    
    if not ticket_data:
        return redirect(url_for('mainCust.home_cust_flight'))
    
    return render_template('customer/booking_confirmation.html', 
                          username=session['username'],
                          ticket=ticket_data)
@main.route('/home_customer_flight', methods = ['GET','POST'])
def home_cust_flight():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    customer_email = session['username']
    
    # Get customer name
    cursor = current_app.config['db'].cursor()
    name_query = 'SELECT name FROM Customer WHERE email = %s'
    cursor.execute(name_query, (customer_email,))
    customer_data = cursor.fetchone()
    
    # Get all flights booked by this customer
    flights_query = '''
    SELECT t.ticket_id, t.sold_price, t.Airline_name, t.flight_no, 
           t.departure_date_and_time, f.arrival_date_and_time, 
           a1.name as departure_airport, a2.name as arrival_airport,
           a1.city as departure_city, a2.city as arrival_city,
           p.date_and_time as booking_date, f.status
    FROM Purchases p
    JOIN Ticket t ON p.ticket_id = t.ticket_id
    JOIN Flight f ON t.Airline_name = f.Airline_Name 
                 AND t.flight_no = f.flight_no 
                 AND t.departure_date_and_time = f.departure_date_and_time
    JOIN Airport a1 ON f.departure_airport_id = a1.Airport_id
    JOIN Airport a2 ON f.arrival_airport_id = a2.Airport_id
    WHERE p.email = %s
    ORDER BY t.departure_date_and_time
    '''
    
    cursor.execute(flights_query, (customer_email,))
    flights = cursor.fetchall()
    
    # Separate upcoming and past flights
    current_time = datetime.now()
    upcoming_flights = []
    past_flights = []
    
    for flight in flights:
        departure_time = flight['departure_date_and_time']
        if isinstance(departure_time, str):
            departure_time = datetime.strptime(departure_time, '%Y-%m-%d %H:%M:%S')
        
        if departure_time > current_time:
            upcoming_flights.append(flight)
        else:
            past_flights.append(flight)
    
    cursor.close()
    
    return render_template('customer/home_customer_flight.html', 
                          username=customer_data['name'] if customer_data else customer_email,
                          upcoming_flights=upcoming_flights,
                          past_flights=past_flights)