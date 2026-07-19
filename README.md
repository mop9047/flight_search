# Flight Search & Booking System

A full-stack web application for searching and booking flights, built with Python (Flask) and MySQL. Supports two distinct user roles — customers and airline staff — each with their own dashboard and feature set.

## Features

### Customer
- Register and log in with session-based authentication
- Search flights by origin, destination, and date (one-way or round-trip)
- Book flights with a simulated payment flow
- Dynamic pricing — ticket price increases 20% when a flight is 60%+ full
- View upcoming and past flights, cancel bookings up to 24 hours before departure
- Rate and review completed flights

### Airline Staff
- View upcoming flights for their airline (next 30 days)
- Create new flights and edit existing ones
- Update flight status (on-time, delayed, cancelled)
- Add airports and airplanes to the system
- Look up the customer manifest for any flight
- View per-flight ratings and passenger reviews
- Generate ticket sales reports with custom date range filters

## Tech Stack

- **Backend:** Python, Flask, Flask Blueprints
- **Database:** MySQL (via PyMySQL)
- **Templating:** Jinja2
- **Frontend:** HTML, CSS

## Setup

### Prerequisites
- Python 3
- [MAMP](https://www.mamp.info/) (or any MySQL server)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mop9047/flight_search.git
   cd flight_search
   ```

2. Install dependencies:
   ```bash
   pip install flask pymysql
   ```

3. Set up the database:
   - Start your MySQL server
   - Create a database named `flights_new`
   - Run the schema file to create all tables:
     ```sql
     source app/create_tables.SQL
     ```

4. Configure the database connection in `app/__init__.py` to match your MySQL host, user, password, and socket path.

5. Run the app:
   ```bash
   python run.py
   ```

6. Open `http://127.0.0.1:8889` in your browser.

## Database Schema

The schema includes 9 tables with proper foreign key relationships:

`Customer` · `Airline` · `Airport` · `Airplane` · `Airline_Staff` · `Flight` · `Ticket` · `Purchases` · `Review`
