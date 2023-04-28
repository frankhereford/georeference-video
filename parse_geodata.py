#!/usr/bin/env python3

import csv
import argparse
import psycopg2

def parse_csv_file(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

def connect_to_db():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="geovideo",
        user="frank",
        password="frank"
    )
    return connection

def drop_gps_table(connection):
    drop_table_sql = '''
    DROP TABLE IF EXISTS gps;
    '''

    with connection.cursor() as cursor:
        cursor.execute(drop_table_sql)
        connection.commit()

def check_null(value):
    if value == '(null)':
        return None
    else:
        return value

def create_gps_table(connection):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS gps (
        id SERIAL PRIMARY KEY,
        date_gmt TIMESTAMP,
        date_local TIMESTAMP,
        time_sec NUMERIC,
        latitude NUMERIC,
        longitude NUMERIC,
        horizontal_accuracy NUMERIC,
        altitude NUMERIC,
        vertical_accuracy NUMERIC,
        distance NUMERIC,
        speed NUMERIC,
        average_speed NUMERIC,
        course NUMERIC,
        true_heading NUMERIC,
        magnetic_heading NUMERIC,
        heading_accuracy NUMERIC,
        glide_ratio NUMERIC,
        heart_rate INTEGER,
        geom GEOMETRY(POINTZ, 4326)
    );
    '''

    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)
        connection.commit()

def insert_gps_data(connection, data):
    insert_sql = '''
    INSERT INTO gps (
        date_gmt, date_local, time_sec, latitude, longitude,
        horizontal_accuracy, altitude, vertical_accuracy, distance,
        speed, average_speed, course, true_heading, magnetic_heading,
        heading_accuracy, glide_ratio, heart_rate, geom
    ) VALUES (
        %(Date_GMT)s, %(Date_Local)s, %(Time_sec)s, %(Latitude)s, %(Longitude)s,
        %(Horizontal Accuracy_m)s, %(Altitude_m)s, %(Vertical Accuracy_m)s, %(Distance_m)s,
        %(Speed_m_per_s)s, %(Average Speed_m_per_s)s, %(Course_deg)s, %(True Heading_deg)s, %(Magnetic Heading_deg)s,
        %(Heading Accuracy_deg)s, %(Glide Ratio)s, %(Heart Rate _bpm)s,
        ST_SetSRID(ST_MakePoint(%(Longitude)s, %(Latitude)s, %(Altitude_m)s), 4326)
    );
    '''


    with connection.cursor() as cursor:
        for row in data:
            row["Time_sec"] = check_null(row["Time_sec"])
            print(row)
            print(insert_sql)
            print(row)
            cursor.execute(insert_sql, row)
        connection.commit()

def main():
    parser = argparse.ArgumentParser(description='Parse CSV file into a list of dictionaries')
    parser.add_argument('--geodata_csv', type=str, required=True, help='Path to the input CSV file')

    args = parser.parse_args()
    file_path = args.geodata_csv

    parsed_data = parse_csv_file(file_path)

    connection = connect_to_db()
    drop_gps_table(connection)
    create_gps_table(connection)
    insert_gps_data(connection, parsed_data)
    connection.close()

if __name__ == "__main__":
    main()
