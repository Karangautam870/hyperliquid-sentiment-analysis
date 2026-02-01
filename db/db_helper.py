import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class DB:
    def __init__(self):
        # connect to MySQL database
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                database='flights',
                user='root',
                password=os.getenv("MY_SECRET_PASSWORD")
            )

            self.mycursor = self.connection.cursor()
            st.success("Connected to MySQL database")

        except Error as e:
            st.error(f"Error while connecting to MySQL: {e}")

    def fetch_cities(self, cursor=None):
        """Return a list of distinct city names from source and destination columns.

        If `cursor` is provided, it will be used; otherwise `self.mycursor` is used.
        """
        cur = cursor or self.mycursor
        try:
            cur.execute("""
                SELECT DISTINCT(source) FROM flights.flights_dataset
                UNION
                SELECT DISTINCT(destination) FROM flights.flights_dataset
            """)
            cities = [row[0] for row in cur.fetchall()]
            return sorted(cities)
        except Error as e:
            st.error(f"Error fetching cities: {e}")
            return []

    def fetch_flights(self, source, destination, cursor=None):

        cur = cursor or self.mycursor
        try:
            sql = """
                SELECT Airline,Route, Dep_Time, Duration,Price FROM flights.flights_dataset
                WHERE source = %s AND destination = %s
            """
            val = (source, destination)
            cur.execute(sql, val)
            flights = cur.fetchall()
            return flights
        except Error as e:
            st.error(f"Error fetching flights: {e}")
            return []