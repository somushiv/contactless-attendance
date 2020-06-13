# * ---------- IMPORTS --------- *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import mysql.connector
import cv2
import numpy as np
import re
import sys
import datetime, time

# Get the relativ path to this file (we will use it later)
FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# * ---------- Create App --------- *
app = Flask(__name__)
CORS(app, support_credentials=True)

# * ---------- DATABASE CONFIG --------- *
# DATABASE_USER = os.environ['DATABASE_USER']
# DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
# DATABASE_HOST = os.environ['DATABASE_HOST']
# DATABASE_PORT = os.environ['DATABASE_PORT']
# DATABASE_NAME = os.environ['DATABASE_NAME']

DATABASE_USER = "root"
DATABASE_PASSWORD = "root12"
DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = "3306"
DATABASE_NAME = "orangehrms03102020"


def DATABASE_CONNECTION():
    return mysql.connector.connect(user=DATABASE_USER,
                                   password=DATABASE_PASSWORD,
                                   host=DATABASE_HOST,
                                   port=DATABASE_PORT,
                                   database=DATABASE_NAME)


# * --------------------  ROUTES ------------------- *
# * ---------- Get data from the face recognition ---------- *
# * ---------- Add new employee ---------- *
@app.route('/', methods=['GET'])
def home():
    return jsonify("Its Home Ficial")


@app.route('/receive_data', methods=['POST'])
def get_receive_data():
    if request.method == 'POST':
        json_data = request.get_json()
        name = json_data['name']
        employee_id = name[name.find("_") + 1:]
        print(employee_id)
        # Check if the user is already in the DB
        try:
            # Connect to the DB
            connection = DATABASE_CONNECTION()
            cursor = connection.cursor(dictionary=True)

            # Query to check if the user as been saw by the camera today
            user_saw_today_sql_query =\
                f"SELECT * FROM hs_hr_attendance WHERE date_format(punchin_time,'%Y-%m-%d')= '{json_data['date']}' AND employee_id = {employee_id} AND punchout_time is null "
            print(user_saw_today_sql_query)
            cursor.execute(user_saw_today_sql_query)
            result = cursor.fetchone()
            connection.commit()

            # If use is already in the DB for today:
            if result:
                print('user Out')
                # image_path = f"{FILE_PATH}/assets/img/{json_data['date']}/{json_data['name']}/departure.jpg"

                # Save image
                #os.makedirs(
                #    f"{FILE_PATH}/assets/img/{json_data['date']}/{json_data['name']}",
                #    exist_ok=True)
                #cv2.imwrite(image_path, np.array(json_data['picture_array']))
                #json_data['picture_path'] = image_path

                # Update user in the DB
                insert_status = validate_for_facial_insert(
                    employee_id, json_data['date'])
                if insert_status:
                    update_user_querry = f"UPDATE hs_hr_attendance SET punchout_time = '{json_data['date_time']}' WHERE attendance_id = {result['attendance_id']}"
                    print(update_user_querry)
                    cursor.execute(update_user_querry)

            else:
                print("user In")
                # Save image
                #image_path = f"{FILE_PATH}/assets/img/history/{json_data['date']}/{json_data['name']}/arrival.jpg"
                #os.makedirs(
                #    f"{FILE_PATH}/assets/img/history/{json_data['date']}/{json_data['name']}",
                #    exist_ok=True)
                #cv2.imwrite(image_path, np.array(json_data['picture_array']))
                #json_data['picture_path'] = image_path

                # Create a new row for the user today:
                insert_status = validate_for_facial_insert(
                    employee_id, json_data['date'])
                if insert_status:
                    insert_user_querry = f"INSERT INTO hs_hr_attendance (employee_id, punchin_time,timestamp_diff) VALUES ({employee_id}, '{json_data['date_time']}',0)"
                    print(insert_user_querry)
                    cursor.execute(insert_user_querry)

        except mysql.connector.Error as err:
            print("ERROR DB: ", err.errno)
        finally:
            connection.commit()

            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("Mysql connection is closed")

        # Return user's data to the front
        return jsonify(json_data)


def validate_for_facial_insert(employee_id, date):
    connection = DATABASE_CONNECTION()
    cursor = connection.cursor(dictionary=True)
    query_to_validate = f"SELECT * FROM hs_hr_attendance where employee_id={employee_id} AND date_format(punchin_time,'%Y-%m-%d')='{date}' order by attendance_id desc limit 0,1"
    print(query_to_validate)
    cursor.execute(query_to_validate)
    result = cursor.fetchone()
    connection.commit()
    insert_mode = False
    if result:
        #Time Validate

        inserted_time = result['punchin_time']
        current_time = datetime.datetime.now()
        time_difference = str(current_time - inserted_time)
        time_difference = time_difference.split(":")
        print(current_time)
        print(inserted_time)
        print(time_difference)
        if int(time_difference[0]) == 0 and int(time_difference[1]) < 31:
            print("Less then 30min")
            insert_mode = False
        elif int(time_difference[0]) >= 0 and int(time_difference[1]) > 30:
            print("Entry for 2nd time")
            insert_mode = True

    else:
        print("No Entry")
        insert_mode = True
    return insert_mode


# * ---------- Get all the data of an employee ---------- *
@app.route('/get_employee/<string:name>', methods=['GET'])
def get_employee(name):
    answer_to_send = {}
    # Check if the user is already in the DB
    try:
        # Connect to DB
        connection = DATABASE_CONNECTION()
        cursor = connection.cursor()
        # Query the DB to get all the data of a user:
        user_information_sql_query = f"SELECT * FROM users WHERE name = '{name}'"

        cursor.execute(user_information_sql_query)
        result = cursor.fetchall()
        connection.commit()

        # if the user exist in the db:
        if result:
            print('RESULT: ', result)
            # Structure the data and put the dates in string for the front
            for k, v in enumerate(result):
                answer_to_send[k] = {}
                for ko, vo in enumerate(result[k]):
                    answer_to_send[k][ko] = str(vo)
            print('answer_to_send: ', answer_to_send)
        else:
            answer_to_send = {'error': 'User not found...'}

    except mysql.connector.Error as err:
        print("ERROR DB: ", err.errno)
    finally:
        # closing database connection:
        if (connection):
            cursor.close()
            connection.close()

    # Return the user's data to the front
    return jsonify(answer_to_send)


# * --------- Get the 5 last users seen by the camera --------- *
@app.route('/get_5_last_entries', methods=['GET'])
def get_5_last_entries():
    answer_to_send = {}
    # Check if the user is already in the DB
    try:
        # Connect to DB
        connection = DATABASE_CONNECTION()

        cursor = connection.cursor()
        # Query the DB to get all the data of a user:
        lasts_entries_sql_query = f"SELECT * FROM users ORDER BY id DESC LIMIT 5;"

        cursor.execute(lasts_entries_sql_query)
        result = cursor.fetchall()
        connection.commit()

        # if DB is not empty:
        if result:
            # Structure the data and put the dates in string for the front
            for k, v in enumerate(result):
                answer_to_send[k] = {}
                for ko, vo in enumerate(result[k]):
                    answer_to_send[k][ko] = str(vo)
        else:
            answer_to_send = {'error': 'error detect'}

    except mysql.connector.Error as err:
        print("ERROR DB: ", err.errno)
    finally:
        # closing database connection:
        if (connection):
            cursor.close()
            connection.close()

    # Return the user's data to the front
    return jsonify(answer_to_send)


# * ---------- Add new employee ---------- *
@app.route('/add_employee')
@cross_origin(supports_credentials=True)
def add_employee():
    try:
        # Get the picture from the request
        image_file = request.files['image']
        print(request.form['nameOfEmployee'])

        # Store it in the folder of the know faces:
        file_path = os.path.join(
            f"assets/img/users/{request.form['nameOfEmployee']}.jpg")
        image_file.save(file_path)
        answer = 'new employee succesfully added'
    except:
        answer = 'Error while adding new employee. Please try later...'
    return jsonify(answer)


# * ---------- Get employee list ---------- *
@app.route('/get_employee_list', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_employee_list():
    # Connect to Database

    return "hello"


@app.route('/list_employee', methods=['GET'])
@cross_origin(supports_credentials=True)
def list_employee():
    db_conn = DATABASE_CONNECTION()
    db_cursor = db_conn.cursor(dictionary=True)

    db_cursor.execute(
        "SELECT emp_number,concat(emp_firstname,' ',emp_lastname) as emplyeename FROM hs_hr_employee order by emplyeename limit 0,20;",
    )
    db_result = db_cursor.fetchall()
    # Connect to Database
    return jsonify(db_result)


@app.route('/employee_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def employee_data():
    if request.method == 'POST':
        json_data = request.get_json()
        emp_number = json_data['emp_number']
        db_conn = DATABASE_CONNECTION()
        db_cursor = db_conn.cursor(dictionary=True)
        employee_entries_sql_query = f"SELECT emp_number,concat(emp_firstname,' ',emp_lastname) as emplyeename,city_code,emp_work_email FROM hs_hr_employee where emp_number={emp_number};"
        db_cursor.execute(employee_entries_sql_query)
        db_result = db_cursor.fetchone()
    # Connect to Database
    return jsonify(db_result)


# * ---------- Delete employee ---------- *
@app.route('/delete_employee/<string:name>', methods=['GET'])
def delete_employee(name):
    try:
        # Remove the picture of the employee from the user's folder:
        print('name: ', name)
        file_path = os.path.join(f'assets/img/users/{name}.jpg')
        os.remove(file_path)
        answer = 'Employee succesfully removed'
    except:
        answer = 'Error while deleting new employee. Please try later'

    return jsonify(answer)


import base64
from io import BytesIO
from PIL import Image
import datetime


def getFilePath(emp_number=0):
    #path = os.getcwd()

    file_path = os.path.join(f"assets/img/users/staff_{emp_number}")
    checkPath = os.path.isdir(file_path)

    if not checkPath:
        os.mkdir(file_path)

    return file_path


def getFilePath_2(emp_number, emp_name):
    #path = os.getcwd()
    emp_name = emp_name.replace('.', '-')
    emp_name = emp_name.replace(' ', '-')

    filename = emp_name + '_' + str(emp_number)
    file_path = os.path.join(f"assets/img/users/{filename}")
    checkPath = os.path.isdir(file_path)

    if not checkPath:
        os.mkdir(file_path)

    return file_path


# * ------------ Get Video Image --------- *
@app.route('/saveimage', methods=['POST'])
@cross_origin(supports_credentials=True)
def saveimage():
    image_data_object = request.json

    image_data_list = image_data_object['image_data']
    file_path = getFilePath(image_data_object['emp_number'])
    c = 0
    for image_data in image_data_list:
        starter = image_data.find(',')
        image_data = image_data[starter + 1:]

        image_data = bytes(image_data, encoding="ascii")
        im = Image.open(BytesIO(base64.b64decode(image_data)))
        x = datetime.datetime.now()
        file_name = x.strftime(f"emp_{c}")

        im.save(f"{file_path}/{file_name}.jpg")
        c += 1
    #Beta Live Image Locations without dataset
    file_path2 = getFilePath_2(image_data_object['emp_number'],
                               image_data_object['emp_name'])
    image_data = image_data_list[0]
    image_data = image_data[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im.save(f"{file_path2}.jpg")

    # im.save('image.jpg')
    #with open(file_path, 'wb') as f:
    #    f.write(im)

    return jsonify("test")


# * -------------------- RUN SERVER -------------------- *
if __name__ == '__main__':
    # * --- DEBUG MODE: --- *
    app.run(host='127.0.0.1', port=5000, debug=True)
    #  * --- DOCKER PRODUCTION MODE: --- *
    # app.run(host='0.0.0.0', port=os.environ['PORT']) -> DOCKER
