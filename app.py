import streamlit as st
import mysql.connector
import datetime
import random
import os
import time
import requests

# MySQL Connection details (use environment variables for security)
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Aman@955'
MYSQL_DATABASE = 'Railway_Management_System'

# API URL for fetching train schedules (example API)
API_BASE_URL = "https://indianrailapi.com/api/v2/"

# Defining per/km charge for each class
sleeper_charge = 1.5
third_ac_charge = 2
second_ac_charge = 3
first_ac_charge = 4

# Getting current date and max booking date (4 months ahead)
current_date = datetime.date.today()
max_date = current_date + datetime.timedelta(days=120)

# MySQL connection function
def connect_to_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


# Function to fetch real-time train schedules from API
def fetch_train_schedule(source_station, destination_station, journey_date):
    url = f"{API_BASE_URL}train_schedule"
    params = {
        'source': source_station,
        'destination': destination_station,
        'date': journey_date
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None


# AvailableTrains Function (Updated)
def available_trains(start_opt, final_opt, date_user):
    # Fetch train schedules from API instead of DB for availability
    train_data = fetch_train_schedule(start_opt, final_opt, date_user)

    if train_data and train_data.get("train_list"):
        return train_data["train_list"]
    else:
        return None


# CheckFare Function (Updated)
def check_fare(start_opt, final_opt):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT Train_No, Distance
        FROM train_info
        WHERE Source_Station_Code = "{start_opt}" AND Destination_Station_Code = "{final_opt}";
    """)
    result = cursor.fetchall()
    connection.close()

    fare_details = []
    for row in result:
        distance = row[1]
        fare_details.append({
            'Train_No': row[0],
            'Sleeper': distance * sleeper_charge,
            'Third_AC': distance * third_ac_charge,
            'Second_AC': distance * second_ac_charge,
            'First_AC': distance * first_ac_charge
        })
    return fare_details


# ShowBookings Function
def show_bookings(mobile_no):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT * FROM bookings WHERE Mobile_No = "{mobile_no}";
    """)
    result = cursor.fetchall()
    connection.close()

    if result:
        return result
    else:
        return None


# BookTrain Function
def book_train(train_no, name, mobile, adhaar, date, class_type):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Generating a unique Booking ID
    booking_id = random.randint(1, 10000)
    cursor.execute("SELECT Booking_ID FROM bookings")
    used_ids = [row[0] for row in cursor.fetchall()]
    while booking_id in used_ids:
        booking_id = random.randint(1, 10000)

    query = f"""
        INSERT INTO bookings (Train_No, Passenger_Name, Mobile_No, Passenger_Adhaar, Time_Of_Booking, Booking_ID, Class)
        VALUES ({train_no}, "{name}", "{mobile}", "{adhaar}", "{date}", {booking_id}, "{class_type}");
    """
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
        return booking_id
    except Exception as e:
        connection.close()
        return None


# CancelBooking Function
def cancel_booking(booking_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM bookings WHERE Booking_ID = {booking_id}")
    result = cursor.fetchall()

    if result:
        cursor.execute(f"DELETE FROM bookings WHERE Booking_ID = {booking_id}")
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


# Streamlit Frontend
def main():
    st.title("Railway Management System")

    # Operations List
    operations = ["Available Trains", "Check Fare", "Show Bookings", "Book a Train", "Cancel Booking"]
    operation = st.sidebar.selectbox("Select Operation", operations)

    # Operation: Available Trains
    if operation == "Available Trains":
        start_station = st.text_input("From (Station Code)")
        end_station = st.text_input("To (Station Code)")
        travel_date = st.date_input("Travel Date", min_value=current_date, max_value=max_date)

        if st.button("Search Trains"):
            if start_station and end_station:
                result = available_trains(start_station, end_station, travel_date)
                if result:
                    st.write("Available Trains:")
                    for train in result:
                        st.write(f"Train No: {train['train_no']} | {train['source_station_name']} to {train['destination_station_name']} | Arrival: {train['arrival_time']} | Departure: {train['departure_time']}")
                else:
                    st.error("No trains found for the given stations.")
            else:
                st.error("Please enter both start and end station codes.")

    # Operation: Check Fare
    elif operation == "Check Fare":
        start_station = st.text_input("From (Station Code)")
        end_station = st.text_input("To (Station Code)")

        if st.button("Check Fare"):
            if start_station and end_station:
                fares = check_fare(start_station, end_station)
                if fares:
                    st.write("Fare Details:")
                    for fare in fares:
                        st.write(f"Train No: {fare['Train_No']} | Sleeper: ₹{fare['Sleeper']} | AC-1: ₹{fare['First_AC']} | AC-2: ₹{fare['Second_AC']} | AC-3: ₹{fare['Third_AC']}")
                else:
                    st.error("No fare information found.")
            else:
                st.error("Please enter both start and end station codes.")

    # Operation: Show Bookings
    elif operation == "Show Bookings":
        mobile_no = st.text_input("Enter your Mobile Number")

        if st.button("Show My Bookings"):
            if mobile_no:
                bookings = show_bookings(mobile_no)
                if bookings:
                    st.write("Your Bookings:")
                    for booking in bookings:
                        st.write(f"Train No: {booking[0]} | Name: {booking[1]} | Booking ID: {booking[5]} | Class: {booking[6]}")
                else:
                    st.error("No bookings found.")
            else:
                st.error("Please enter your mobile number.")

    # Operation: Book a Train
    elif operation == "Book a Train":
        train_no = st.number_input("Train No.", min_value=1)
        name = st.text_input("Your Name")
        mobile = st.text_input("Mobile No.")
        adhaar = st.text_input("Adhaar No.")
        class_type = st.selectbox("Class", ["Sleeper", "AC-1", "AC-2", "AC-3"])
        date = datetime.datetime.now().date()

        if st.button("Book Now"):
            if name and mobile and adhaar:
                booking_id = book_train(train_no, name, mobile, adhaar, date, class_type)
                if booking_id:
                    st.success(f"Booking Successful! Your Booking ID is {booking_id}.")
                else:
                    st.error("Booking Failed. Please try again.")
            else:
                st.error("Please fill in all the details.")

    # Operation: Cancel Booking
    elif operation == "Cancel Booking":
        booking_id = st.number_input("Enter Booking ID", min_value=1)

        if st.button("Cancel Booking"):
            if booking_id:
                success = cancel_booking(booking_id)
                if success:
                    st.success(f"Booking with ID {booking_id} has been cancelled.")
                else:
                    st.error(f"No booking found with ID {booking_id}.")
            else:
                st.error("Please enter a valid booking ID.")


if __name__ == '__main__':
    main()
