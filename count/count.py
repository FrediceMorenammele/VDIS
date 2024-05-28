import cv2
import numpy as np
from time import sleep
from datetime import datetime
import psycopg2

class PostgreTableManager:
    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to the PostgreSQL database")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def create_table(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS vehicle_counts (
                id SERIAL PRIMARY KEY,
                count INTEGER,
                insert_time TIMESTAMP
            )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while creating table:", error)

    def insert_data(self, count):
        try:
            insert_query = '''
            INSERT INTO vehicle_counts (count, insert_time)
            VALUES (%s, %s)
            '''
            timestamp = datetime.now()
            data = (count, timestamp)
            self.cursor.execute(insert_query, data)
            self.connection.commit()
            print("Data inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting data:", error)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection closed")


class VehicleDetector:
    def __init__(self, video_path, table_manager):
        self.video_path = video_path
        self.table_manager = table_manager

    def detect_vehicles(self):
        cap = cv2.VideoCapture(self.video_path)
        subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
        line_position = 550
        offset = 6
        car_count = 0
        while True:
            ret, frame1 = cap.read()
            if not ret:
                break
            grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (3, 3), 5)
            img_sub = subtracao.apply(blur)
            dilat = cv2.dilate(img_sub, np.ones((5, 5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
            dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cv2.line(frame1, (25, line_position), (1200, line_position), (255, 127, 0), 3)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w >= 80 and h >= 80:
                    cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    center = (x + w // 2, y + h // 2)
                    if center[1] < (line_position + offset) and center[1] > (line_position - offset):
                        car_count += 1
                        print("Car Detected! Count:", car_count)
                        self.update_vehicle_count(car_count)
                        print()
                    cv2.circle(frame1, center, 3, (0, 0, 255), -1)  # Red dot on vehicles

            cv2.putText(frame1, "Vehicle Count: " + str(car_count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            cv2.imshow("dilated", dilated)
            cv2.imshow("Video Original", frame1)
            

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()
        cap.release()

    def update_vehicle_count(self, count):
        self.table_manager.connect()
        self.table_manager.insert_data(count)
        self.table_manager.close_connection()

# Usage example
if __name__ == "__main__":
    # Connect to PostgreSQL and create table
    table_manager = PostgreTableManager(
        username="postgres",
        password="5818",
        host="localhost",
        port="1234",
        database="VDIS"
    )
    table_manager.connect()
    table_manager.create_table()

    # Create the VehicleDetector instance
    detector = VehicleDetector("video.mp4", table_manager)

    # Detect vehicles and update count
    detector.detect_vehicles()
