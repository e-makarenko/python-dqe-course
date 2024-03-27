import sqlite3
from geopy.distance import geodesic


class DistanceCalculator:
    def __init__(self):
        self.conn = sqlite3.connect('cities.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cities (city_name text, lat float, long float)")
        self.conn.commit()

    def get_coordinates(self, city_name):
        self.cursor.execute(f"SELECT lat, long FROM cities WHERE city_name = '{city_name}'")
        coordinates = self.cursor.fetchone()
        if coordinates is None:
            # format passed input to float to be able to use it later in geodesic function
            lat = float(input(f"Enter the latitude for {city_name}: "))
            long = float(input(f"Enter the longitude for {city_name}: "))
            coordinates = (lat, long)
            self.cursor.execute(f"INSERT INTO cities VALUES ('{city_name}', {coordinates[0]}, {coordinates[1]})")
            self.cursor.connection.commit()
        return coordinates

    def get_distance(self):
        first_city_name = input("Enter first city: ")
        first_city_coordinates = self.get_coordinates(first_city_name)

        second_city_name = input("Enter second city: ")
        second_city_coordinates = self.get_coordinates(second_city_name)
        # use geodesic function from geopy to calculate distance based on geo coordinates
        distance = geodesic(first_city_coordinates, second_city_coordinates).km
        return round(distance, 2)

    def close(self):
        self.conn.close()


calculator = DistanceCalculator()
print("Distance:", calculator.get_distance(), "km")
calculator.close()
