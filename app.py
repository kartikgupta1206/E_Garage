# Importing essential libraries
from flask import Flask, render_template, request, redirect, url_for
import pickle
import mysql.connector
import numpy as np
import time
from flask import session
app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="E_Garage"
)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mydb.cursor()
        query_user = "SELECT * FROM admin WHERE email_admin = %s AND password_admin = %s"
        data_user = (email, password)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            first_name = "ADMIN"
            cursor.close()
            cursor = mydb.cursor()
            detail_user_query = "SELECT * FROM DETAILSS"
            cursor.execute(detail_user_query, ())
            detail_user = cursor.fetchall()
            if detail_user:
                detail_user_query2 = "SELECT * FROM SERVICE"
                cursor.execute(detail_user_query2, ())
                detail_user2 = cursor.fetchall()
                if detail_user2:
                    return render_template('admin_data.html', first_name=first_name, detail_user=detail_user, detail_user2=detail_user2)

        else:
            error = "ADMIN Credentials not found"
            return render_template('admin.html', error=error)

    return render_template('admin.html', error="")


@app.route('/form1', methods=['GET', 'POST'])
def form1():
    car_model = None
    if request.method == 'POST':
        # Retrieve the email from the session
        email = session.get('email')
        car_model_id = request.form.get('brand')
        # Map the selected value to the corresponding data
        if car_model_id == '1':
            car_model = 'Maruti Suzuki'
        elif car_model_id == '2':
            car_model = 'Hyundai'
        elif car_model_id == '3':
            car_model = 'CNG'
        elif car_model_id == '4':
            car_model = 'Tata'
        elif car_model_id == '5':
            car_model = 'Honda'
        elif car_model_id == '6':
            car_model = 'Toyota'
        elif car_model_id == '7':
            car_model = 'Volkswagen'
        elif car_model_id == '8':
            car_model = 'Kia'
        elif car_model_id == '9':
            car_model = 'Ford'
        elif car_model_id == '10':
            car_model = 'Mahindra'
        elif car_model_id == '11':
            car_model = 'Renault'
        elif car_model_id == '12':
            car_model = 'Nissan'
        elif car_model_id == '13':
            car_model = 'Mercedes-Benz'
        elif car_model_id == '14':
            car_model = 'BMW'
        elif car_model_id == '15':
            car_model = 'Jaguar'
        elif car_model_id == '16':
            car_model = 'Lexus'
        elif car_model_id == '17':
            car_model = 'Audi'
        elif car_model_id == '18':
            car_model = 'Porsche'
        elif car_model_id == '19':
            car_model = 'Aston Martin'
        elif car_model_id == '20':
            car_model = 'Maserati'
        elif car_model_id == '21':
            car_model = 'Bentley'
        elif car_model_id == '22':
            car_model = 'Rolls-Royce'
        elif car_model_id == '23':
            car_model = 'Lamborghini'
        elif car_model_id == '24':
            car_model = 'Ferrari'
        elif car_model_id == '25':
            car_model = 'McLaren'
        elif car_model_id == '26':
            car_model = 'Bugatti'
        elif car_model_id == '27':
            car_model = 'Volvo'
        else:
            car_model = 'Land Rover'

        year = request.form['year']

        KM_driven = float(request.form['km_driven'])

        fuel_type_id = request.form.get('fuelType')
        if fuel_type_id == '1':
            fuel_type = 'Petrol'
        elif fuel_type_id == '2':
            fuel_type = 'Diesel'
        else:
            fuel_type = 'CNG'

        seller_type_id = request.form.get('sellerType')
        if seller_type_id == '1':
            seller_type = 'Individual'
        elif seller_type_id == '2':
            seller_type = 'Dealer'
        else:
            seller_type = 'Trustmark Dealer'

        transmission_type_id = request.form.get('transmission')
        if transmission_type_id == '1':
            transmission_type = 'Manual'
        elif transmission_type_id == '2':
            transmission_type = 'Automatic'
        else:
            transmission_type = 'CVT'

        owner_type_id = request.form.get('owners')
        if owner_type_id == '1':
            owner_type = 'First Owner'
        elif owner_type_id == '2':
            owner_type = 'Second Owner'
        elif owner_type_id == '3':
            owner_type = 'Third Owner'
        elif owner_type_id == '4':
            owner_type = 'Fourth / Above Owner'
        else:
            owner_type = 'Test Drive Car'

        mileage = float(request.form['mileage'])
        engine = float(request.form['engine_size'])
        power = float(request.form['horsepower'])
        weight = float(request.form['Weight'])
        seats = int(request.form['seat'])

        drive_mode_id = request.form.get('drive')
        if drive_mode_id == '1':
            drive_mode = 'FWD'
        elif drive_mode_id == '2':
            drive_mode = 'RWD'
        elif drive_mode_id == '3':
            drive_mode = '4WD'
        else:
            drive_mode = 'AWD'

        engine_oil = int(request.form['engineOil'])
        break_pad = int(request.form['breakPad'])
        transmission_fuild = int(request.form['transmissionFuel'])
        spark_plug = int(request.form['sparkPlug'])
        tire_rotation = int(request.form['tireRotation'])
        last_service = request.form.get('last_service')
        type_road_id = request.form.get('type_road')
        if type_road_id == '1':
            type_road = 'Highway'
        else:
            type_road = 'City'
        drive_style_id = request.form.get('driving')
        if drive_style_id == '1':
            drive_style = 'Normal'
        else:
            drive_style = 'City'
        cursor = mydb.cursor()

        # SQL query to insert the form data into the detailss table
        insert_query = """
            INSERT INTO detailss (email,car_model, year, KM_driven, fuel_type, seller_type, transmission_type, owner_type,
                         mileage, engine, power, seats, weight , drive_mode, engine_oil, break_pad, transmission_fuild,
                         spark_plug, tire_rotation,last_service,type_road,drive_style)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
            """

        data = (email, car_model, year, KM_driven, fuel_type, seller_type, transmission_type, owner_type,
                mileage, engine, power, seats, weight, drive_mode, engine_oil, break_pad, transmission_fuild,
                spark_plug, tire_rotation, last_service, type_road, drive_style)

        try:
            # Execute the insert query
            cursor.execute(insert_query, data)
            # Commit the transaction
            mydb.commit()
            # Close the cursor
            cursor.close()

            # Redirect to a success page or render a success template
            return render_template("form1.html", email=email,  registration_success1=True)
        except Exception as e:
            # Rollback the transaction if an error occurs
            mydb.rollback()
            # Render an error template or handle the error accordingly
            return render_template("form1.html", email=email,  error=str(e))
    return render_template("form1.html", email="")


@app.route('/assign', methods=['GET', 'POST'])
def assign():

    if request.method == 'POST':
        # Retrieve the email from the session
        service_id = request.form.get('service_center')
        # Map the selected value to the corresponding data
        if service_id == '1':
            service_ids = 'abc@gmail.com'
        elif service_id == '2':
            service_ids = 'kar@gmail.com'
        elif service_id == '3':
            service_ids = 'shash@gmail.com'
        else:
            service_ids = 'NIT@gmail.com'

        Users = request.form.get('user_email')
        if Users == '1':
            Userss = 'kartik002002@gmail.com'
        else:
            Userss = 'mnb@gmail.com'

        last_service = request.form.get('last_service')
        curr_year = request.form['year']

        cursor = mydb.cursor()

        # SQL query to insert the form data into the detailss table
        insert_query = """
            INSERT INTO admin_service (SERVICE_EMAIL, USER_EMAIL ,last_service,curr_service)
                        VALUES (%s, %s, %s, %s)
            """

        data = (service_ids, Userss, last_service, curr_year)

        try:
            # Execute the insert query
            cursor.execute(insert_query, data)
            # Commit the transaction
            mydb.commit()
            # Close the cursor
            cursor.close()

            # Redirect to a success page or render a success template
            return render_template("assign.html",  registration_success1=True)
        except Exception as e:
            # Rollback the transaction if an error occurs
            mydb.rollback()
            # Render an error template or handle the error accordingly
            return render_template("assign.html",  error=str(e))
    return render_template("assign.html", email="")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        session['email'] = email
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s AND password = %s"
        data_user = (email, password)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            full_name = user[1]
            phone_no = user[4]
            email = user[2]
            detail_user_query = "SELECT * FROM detailss WHERE email = %s"
            cursor.execute(detail_user_query, (email,))
            detail_user = cursor.fetchone()
            if detail_user:
                car_model = detail_user[1]
                year_of_purchase = detail_user[2]
                KM_driven = detail_user[3]
                last_service = detail_user[19]
                fuel_type = detail_user[4]
                seller_type = detail_user[5]
                transmission_type = detail_user[6]
                owner_type = detail_user[7]
                mileage = detail_user[8]
                engine = detail_user[9]
                power = detail_user[10]
                seat = detail_user[11]
                weight = detail_user[12]
                drive_mode = detail_user[13]
                engine_oil = detail_user[14]
                break_pad = detail_user[15]
                tranmission_fuild = detail_user[16]
                spark_plug = detail_user[17]
                tire_rotation = detail_user[18]
                type_road = detail_user[20]
                drive_style = detail_user[21]

                detail_user_query2 = "SELECT car_model FROM detailss WHERE email = %s"
                cursor.execute(detail_user_query2, (email,))
                car_model = cursor.fetchone()

                if car_model:
                    car_model = car_model[0]
                    # Define a dictionary mapping car models to image file paths or URLs
                    car_images = {
                        'Maruti Suzuki': 'static/maruti.jpeg',
                        'Hyundai': 'static/hyundai.jpg',
                        'CNG': 'static/CNG.png',
                        'Tata': 'static/tata.webp',
                        'Honda': 'static/honda.jpeg',
                        'Toyota': 'static/Toyota.jpg',
                        'Volkswagen': 'static/Volkswagen.jpeg',
                        'Kia': 'static/Kia.jpeg',
                        'Ford': 'static/Ford.jpg',
                        'Mahindra': 'static/Mahindra.jpg',
                        'Renault': 'static/Renault.jpg',
                        'Nissan': 'static/Nissan.png',
                        'Mercedes-Benz': 'static/Mercedes-Benz.jpg',
                        'BMW': 'static/BMW.jpg',
                        'Jaguar': 'static/BJaguar.webp',
                        'Lexus': 'static/Lexus.jpeg',
                        'Audi': 'static/Audi.jpg',
                        'Porsche': 'static/Porsche.jpg',
                        'Aston Martin': 'static/Aston_Martin.jpeg',
                        'Maserati': 'static/Maserati.png',
                        'Bentley': 'static/Bentley.png',
                        'Rolls-Royce': 'static/Rolls-Royce.webp',
                        'Lamborghini': 'static/Lamborghini.jpg',
                        'Ferrari': 'static/Ferrari.png',
                        'McLaren': 'static/McLaren.png',
                        'Bugatti': 'static/Bugatti.jpg',
                        'Volvo': 'static/Volvo.jpg',
                        'Land Rover': 'static/Land_Rover.jpeg'
                    }

                    # Check if the selected car model exists in the dictionary
                    if car_model in car_images:
                        image_path = car_images[car_model]
                       # If user exists in the database, redirect to a success page
                        return render_template('user_profile.html', full_name=full_name, phone_no=phone_no, email=email, car_model=car_model,
                                               year_of_purchase=year_of_purchase, KM_driven=KM_driven, last_service=last_service, fuel_type=fuel_type,
                                               seller_type=seller_type, transmission_type=transmission_type, owner_type=owner_type, mileage=mileage, engine=engine,
                                               power=power, seat=seat, weight=weight, drive_mode=drive_mode, engine_oil=engine_oil, break_pad=break_pad,
                                               tranmission_fuild=tranmission_fuild, spark_plug=spark_plug, tire_rotation=tire_rotation, image_path=image_path, drive_style=drive_style, type_road=type_road)
                    else:
                        error = "Image not found for car brand: " + car_model
                        return render_template('login.html', error=error)
            else:
                # If user detailss not found, handle the situation accordingly
                error = "User details not found"
                return render_template('login.html', error=error)
        else:
            # If user doesn't exist or credentials are incorrect, show an error on the login page
            error = "Invalid Email or password"
            return render_template('login.html', error=error)

        cursor.close()

    # Render the login form for GET requests
    return render_template('login.html', error="")


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            # If user exists, update their password
            update_query = "UPDATE CURR_USERS SET password = %s WHERE email = %s"
            data_update = (new_password, email)
            cursor.execute(update_query, data_update)
            mydb.commit()
            cursor.close()
            message = "Password update sucessfully"
            return render_template('forgot.html', message=message)

        else:
            # If email doesn't exist, show an error message
            error = "Email not found. Please enter a valid email."
            return render_template('forgot.html', error=error)

    # Render the forgot password form for GET requests
    return render_template('forgot.html', error=None, message=None)


app.secret_key = 'kartik'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the registration form
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        phone_no = request.form['phone_no']
        session['email'] = email

        # Check if the email already exists in the database
        cursor = mydb.cursor()
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        existing_user = cursor.fetchone()

        if existing_user:
            # If the email already exists, show an error message
            error = "Email already exists. Please use a different email address."
            return render_template('register.html', error=error)

        else:
            # Insert the new user data into the database
            insert_query = "INSERT INTO CURR_USERS (full_name, email, password, phone_no) VALUES (%s, %s, %s, %s)"
            data_insert = (full_name, email, password, phone_no)
            cursor.execute(insert_query, data_insert)
            mydb.commit()
            cursor.close()

            # Set registration_success to True to trigger the alert in the template
            return render_template('register.html', email=email, registration_success=True)

    # Render the registration form for GET requests
    return render_template('register.html', error=None)


@app.route('/update_name', methods=['GET', 'POST'])
def update_name():
    if request.method == 'POST':
        email = session.get('email')
        new_name = request.form['name']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            # If user exists, update their password
            email1 = user[1]
            update_query = "UPDATE CURR_USERS SET full_name = %s WHERE email = %s"
            data_update = (new_name, email)
            cursor.execute(update_query, data_update)
            mydb.commit()
            cursor.close()
            message = "Name update sucessfully"
            return render_template('update_name.html', registration_success=True, message=message, email1=email1)

        else:
            # If email doesn't exist, show an error message
            error = "Email not found. Please enter a valid email."
            return render_template('update_name.html', error=error, email1=email1)

    # Render the form for GET requests
    return render_template('update_name.html', error=None, message=None)


@app.route('/update_phone', methods=['GET', 'POST'])
def update_phone():
    if request.method == 'POST':
        email = session.get('email')
        new_phone = request.form['phone']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            # If user exists, update their password
            email1 = user[1]
            update_query = "UPDATE CURR_USERS SET phone_no = %s WHERE email = %s"
            data_update = (new_phone, email)
            cursor.execute(update_query, data_update)
            mydb.commit()
            cursor.close()
            message = "Phone Number update sucessfully"
            return render_template('update_phone.html', registration_success=True, email1=email1, message=message)

        else:
            # If email doesn't exist, show an error message
            error = "Email not found. Please enter a valid email."
            return render_template('update_phone.html', error=error)

    # Render the form for GET requests
    return render_template('update_phone.html', error=None, message=None)


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        email = session.get('email')
        message = request.form['mes']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            # If user exists, update their password
            update_query = "INSERT INTO MESSAGE(EMAIL,MESSAGE) VALUES (%s, %s)"
            data_update = (email, message)
            cursor.execute(update_query, data_update)
            mydb.commit()
            cursor.close()
            message1 = "Information submitted sucessfully"
            return render_template('messsage.html', registration_success=True, message=message1)

        else:
            # If email doesn't exist, show an error message
            error = "Email not found. Please enter a valid email."
            return render_template('messsage.html',  error=error)

    # Render the form for GET requests
    return render_template('messsage.html',  error=None, message=None)


@app.route('/update_pass', methods=['GET', 'POST'])
def update_pass():
    if request.method == 'POST':
        email = session.get('email')

        new_pass = request.form['password']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (email,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            # If user exists, update their password
            email1 = user[1]
            update_query = "UPDATE CURR_USERS SET password = %s WHERE email = %s"
            data_update = (new_pass, email)
            cursor.execute(update_query, data_update)
            mydb.commit()
            cursor.close()
            message = "Password update sucessfully"
            return render_template('update_pass.html', registration_success=True, email1=email1, message=message)

        else:
            # If email doesn't exist, show an error message
            error = "Email not found. Please enter a valid email."
            return render_template('update_pass.html',  error=error)

    # Render the password form for GET requests
    return render_template('update_pass.html',  error=None, message=None)


@app.route('/car_price')
def car_price():
    return render_template("priceprediction.html")


@app.route('/car_price_predict', methods=['GET', 'POST'])
def predict():
    filename = 'car_price_final.pkl'
    car_mileage = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':
        model = request.form.get('model')
        year = int(request.form['year'])
        kilometers = float(request.form['kilometers'])
        fuelType = request.form.get('fuelType')
        sellerType = request.form.get('sellerType')
        transmission = request.form.get('transmission')
        owners = request.form.get('owners')
        mileage = float(request.form['mileage'])
        engine = float(request.form['engine'])
        power = float(request.form['power'])
        seat = int(request.form['seat'])

        data = np.array(
            [[model, year, kilometers, fuelType, sellerType, transmission,
              owners, mileage, engine, power, seat]], dtype=np.float64)
        my_prediction = car_mileage.predict(data)
        my_prediction_reshaped = my_prediction.reshape(-1, 1)
        output = np.around(my_prediction_reshaped, decimals=2)

        if output > 0:
            return render_template('priceprediction.html', prediction_text="You can sell your car at Rs.{}lac".format(output))

        else:
            return render_template('priceprediction.html', prediction_text="Sorry you cannot sell this car")

    else:
        return render_template('priceprediction.html')


@app.route('/price_email', methods=['GET', 'POST'])
def price_email():
    filename = 'car_price_final.pkl'
    car_mileage = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':

        name = request.form['name']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (name,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            detail_user_query = "SELECT * FROM detailss WHERE email = %s"
            cursor.execute(detail_user_query, (name,))
            detail_user = cursor.fetchone()
            if detail_user:
                car_model_id = detail_user[1]

                if car_model_id == 'Maruti Suzuki':
                    model = 1
                elif car_model_id == 'Hyundai':
                    model = 2
                elif car_model_id == 'CNG':
                    model = 3
                elif car_model_id == 'Tata':
                    model = 4
                elif car_model_id == 'Honda':
                    model = 5
                elif car_model_id == 'Toyota':
                    model = 6
                elif car_model_id == 'Volkswagen':
                    model = 7
                elif car_model_id == 'Kia':
                    model = 8
                elif car_model_id == 'Ford':
                    model = 9
                elif car_model_id == 'Mahindra':
                    model = 10
                elif car_model_id == 'Renault':
                    model = 11
                elif car_model_id == 'Nissan':
                    model = 12
                elif car_model_id == 'Mercedes-Benz':
                    model = 13
                elif car_model_id == 'BMW':
                    model = 14
                elif car_model_id == 'Jaguar':
                    model = 15
                elif car_model_id == 'Lexus':
                    model = 16
                elif car_model_id == 'Audi':
                    model = 17
                elif car_model_id == 'Porsche':
                    model = 18
                elif car_model_id == 'Aston Martin':
                    model = 19
                elif car_model_id == 'Maserati':
                    model = 20
                elif car_model_id == 'Bentley':
                    model = 21
                elif car_model_id == 'Rolls-Royce':
                    model = 22
                elif car_model_id == 'Lamborghini':
                    model = 23
                elif car_model_id == 'Ferrari':
                    model = 24
                elif car_model_id == 'McLaren':
                    model = 25
                elif car_model_id == 'Bugatti':
                    model = 26
                elif car_model_id == 'Volvo':
                    model = 27
                else:
                    model = 28

                fuel_type_id = detail_user[4]
                if fuel_type_id == 'Petrol':
                    fuelType = 1
                elif fuel_type_id == 'Diesel':
                    fuelType = 2
                else:
                    fuelType = 3

                seller_type_id = detail_user[5]
                if seller_type_id == 'Individual':
                    sellerType = 1
                elif seller_type_id == 'Dealer':
                    sellerType = 2
                else:
                    sellerType = 3

                transmission_type_id = detail_user[6]
                if transmission_type_id == 'Manual':
                    transmission = 1
                elif transmission_type_id == 'Automatic':
                    transmission = 2
                else:
                    transmission = 3

                owner_type_id = detail_user[7]
                if owner_type_id == 'First Owner':
                    owners = 1
                elif owner_type_id == 'Second Owner':
                    owners = 2
                elif owner_type_id == 'Third Owner':
                    owners = 3
                elif owner_type_id == 'Fourth / Above Owner':
                    owners = 4
                else:
                    owners = 5

                kilometers = detail_user[3]
                mileage = detail_user[8]
                engine = detail_user[9]
                power = detail_user[10]
                seat = detail_user[11]

                detail_user_query1 = "SELECT YEAR(year) FROM detailss WHERE email = %s"
                cursor.execute(detail_user_query1, (name,))
                year = cursor.fetchone()[0]

                data = np.array(
                    [[model, year, kilometers, fuelType, sellerType, transmission,
                      owners, mileage, engine, power, seat]], dtype=np.float64)
                my_prediction = car_mileage.predict(data)
                my_prediction_reshaped = my_prediction.reshape(-1, 1)
                output = np.around(my_prediction_reshaped, decimals=2)

                if output > 0:
                    return render_template('price_email.html', prediction_text="You can sell your car at Rs.{}lac".format(output))

                else:
                    return render_template('price_email.html', prediction_text="Sorry you cannot sell this car")

            else:
                # If email doesn't exist, show an error message
                error = "Email not found. Please enter a valid email."
                return render_template('price_email.html', error=error)

    # Render the password form for GET requests
    return render_template('price_email.html', error=None, message=None)


@app.route('/mil_email', methods=['GET', 'POST'])
def mil_email():
    filename = 'car_mileage1.pkl'
    car_mileage = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':

        name = request.form['name']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (name,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            detail_user_query = "SELECT * FROM detailss WHERE email = %s"
            cursor.execute(detail_user_query, (name,))
            detail_user = cursor.fetchone()
            if detail_user:
                car_model_id = detail_user[1]

                if car_model_id == 'Maruti Suzuki':
                    model = 1
                elif car_model_id == 'Hyundai':
                    model = 2
                elif car_model_id == 'CNG':
                    model = 3
                elif car_model_id == 'Tata':
                    model = 4
                elif car_model_id == 'Honda':
                    model = 5
                elif car_model_id == 'Toyota':
                    model = 6
                elif car_model_id == 'Volkswagen':
                    model = 7
                elif car_model_id == 'Kia':
                    model = 8
                elif car_model_id == 'Ford':
                    model = 9
                elif car_model_id == 'Mahindra':
                    model = 10
                elif car_model_id == 'Renault':
                    model = 11
                elif car_model_id == 'Nissan':
                    model = 12
                elif car_model_id == 'Mercedes-Benz':
                    model = 13
                elif car_model_id == 'BMW':
                    model = 14
                elif car_model_id == 'Jaguar':
                    model = 15
                elif car_model_id == 'Lexus':
                    model = 16
                elif car_model_id == 'Audi':
                    model = 17
                elif car_model_id == 'Porsche':
                    model = 18
                elif car_model_id == 'Aston Martin':
                    model = 19
                elif car_model_id == 'Maserati':
                    model = 20
                elif car_model_id == 'Bentley':
                    model = 21
                elif car_model_id == 'Rolls-Royce':
                    model = 22
                elif car_model_id == 'Lamborghini':
                    model = 23
                elif car_model_id == 'Ferrari':
                    model = 24
                elif car_model_id == 'McLaren':
                    model = 25
                elif car_model_id == 'Bugatti':
                    model = 26
                elif car_model_id == 'Volvo':
                    model = 27
                else:
                    model = 28

                fuel_type_id = detail_user[4]
                if fuel_type_id == 'Petrol':
                    fuelType = 1
                elif fuel_type_id == 'Diesel':
                    fuelType = 2
                else:
                    fuelType = 3

                seller_type_id = detail_user[5]
                if seller_type_id == 'Individual':
                    sellerType = 1
                elif seller_type_id == 'Dealer':
                    sellerType = 2
                else:
                    sellerType = 3

                transmission_type_id = detail_user[6]
                if transmission_type_id == 'Manual':
                    transmission = 1
                elif transmission_type_id == 'Automatic':
                    transmission = 2
                else:
                    transmission = 3

                owner_type_id = detail_user[7]
                if owner_type_id == 'First Owner':
                    owners = 1
                elif owner_type_id == 'Second Owner':
                    owners = 2
                elif owner_type_id == 'Third Owner':
                    owners = 3
                elif owner_type_id == 'Fourth / Above Owner':
                    owners = 4
                else:
                    owners = 5

                kilometers = detail_user[3]
                engine = detail_user[9]
                power = detail_user[10]
                weight = detail_user[12]
                drive_mode_id = detail_user[13]
                if drive_mode_id == 'FWD':
                    drive_mode = 1
                elif drive_mode_id == 'RWD':
                    drive_mode = 2
                elif drive_mode_id == '4WD':
                    drive_mode = 3
                else:
                    drive_mode = 4

                drive_style_id = detail_user[21]
                if drive_style_id == 'Normal':
                    drive_style = 1
                else:
                    drive_style = 2

                tyep_road_id = detail_user[20]
                if tyep_road_id == 'Highway':
                    type_road = 1
                else:
                    type_road = 2

                detail_user_query1 = "SELECT YEAR(year) FROM detailss WHERE email = %s"
                cursor.execute(detail_user_query1, (name,))
                year = cursor.fetchone()[0]

                data = np.array(
                    [[model, year, engine, power,
                      weight, fuelType, transmission, drive_mode, type_road, drive_style]], dtype=np.float64)
                my_prediction = car_mileage.predict(data)
                my_prediction_reshaped = my_prediction.reshape(-1, 1)
                output = np.around(my_prediction_reshaped, decimals=2)

                if output > 0:
                    return render_template('mil_email.html', prediction_text="Your car mileage is {}KPL/KPKG".format(output))

                else:
                    return render_template('mil_email.html', prediction_text="Sorry your car mileage can't be detected")

            else:
                # If email doesn't exist, show an error message
                error = "Email not found. Please enter a valid email."
                return render_template('mil_email.html', error=error)

    # Render the password form for GET requests
    return render_template('mil_email.html', error=None, message=None)


@app.route('/main_email', methods=['GET', 'POST'])
def main_email():
    filename = 'all.pkl'
    car_main = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':

        name = request.form['name']
        cursor = mydb.cursor()
        # Check if the email exists in the database
        query_user = "SELECT * FROM CURR_USERS WHERE email = %s"
        data_user = (name,)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            detail_user_query = "SELECT * FROM detailss WHERE email = %s"
            cursor.execute(detail_user_query, (name,))
            detail_user = cursor.fetchone()
            if detail_user:

                # detail_user_query1 = "SELECT YEAR(year) FROM detailss WHERE email = %s"
                # cursor.execute(detail_user_query1, (name,))
                # year = cursor.fetchone()[0]
                # Year = 2023-int(year)
                Year = 3
                km_driven = detail_user[2]
                engine_oil = detail_user[14]
                break_pad = detail_user[15]
                tranmission_fuild = detail_user[16]
                spark_plug = detail_user[17]
                tire_rotation = detail_user[18]
                data = np.array(
                    [[km_driven, engine_oil, break_pad, tranmission_fuild,
                      tire_rotation, spark_plug, Year]], dtype=np.float64)
                my_prediction = car_main.predict(data)

                return render_template('car_main_result.html', prediction=my_prediction)
            else:
                # If email doesn't exist, show an error message
                error = "Email not found. Please enter a valid email."
                return render_template('main_email.html', error=error)

    # Render the password form for GET requests
    return render_template('main_email.html', error=None, message=None)


@app.route('/car_mileage')
def car_mileage():
    return render_template("mileage.html")


@app.route('/car_mileage_predict', methods=['GET', 'POST'])
def milpredict():
    filename = 'car_mileage1.pkl'
    car_price = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':
        brand = request.form.get('brand')
        year = int(request.form['year'])
        engine_size = int(request.form['engine_size'])
        horsepower = float(request.form['horsepower'])
        Weight = float(request.form['Weight'])
        fuelType = request.form.get('fuelType')
        transmission = request.form.get('transmission')
        drive = request.form.get('drive')

        data = np.array(
            [[brand, year, engine_size, horsepower,
              Weight, fuelType, transmission, drive]], dtype=np.float64)
        my_prediction = car_price.predict(data)
        my_prediction_reshaped = my_prediction.reshape(-1, 1)
        output = np.around(my_prediction_reshaped, decimals=2)

        if output > 0:
            return render_template('mileage.html', prediction_text="Your car mileage is {}KPL/KPKG".format(output))

        else:
            return render_template('mileage.html', prediction_text="Sorry your car mileage can't be detected")

    else:
        return render_template('mileage.html')


@app.route('/404')
def error():
    return render_template("404.html")


@app.route('/fuel_cost')
def fuel_cost():
    return render_template("fuel_cost.html")


@app.route('/car_maintenance')
def maintenance():
    return render_template("maintenanceprediction.html")


@app.route('/car_maintenance_option')
def maintenance_option():
    return render_template("maintenanceyesorno.html")


@app.route('/car_main_predict', methods=['GET', 'POST'])
def mainpredict():
    filename = 'all.pkl'
    car_main = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':
        year = int(request.form['year'])
        engineOil = int(request.form['engineOil'])
        kilometers = int(request.form['kilometers'])
        breakPad = int(request.form['breakPad'])
        transmissionFuel = int(request.form['transmissionFuel'])
        sparkPlug = int(request.form['sparkPlug'])
        tireRotation = int(request.form['tireRotation'])
        Year = 2023-year
        data = np.array(
            [[kilometers, engineOil, breakPad, transmissionFuel,
              tireRotation, sparkPlug, Year]], dtype=np.float64)
        my_prediction = car_main.predict(data)

        return render_template('car_main_result.html', prediction=my_prediction)


@app.route('/car_main_predict', methods=['GET', 'POST'])
def mainpredictyes():
    filename = 'yes_no_main_tree.pkl'
    car_main = pickle.load(open(filename, 'rb'))
    if request.method == 'POST':
        year = int(request.form['year'])
        engineOil = request.form.get('engineOil')
        kilometers = int(request.form['kilometers'])
        breakPad = request.form.get['breakPad']
        transmissionFuel = request.form.get['transmissionFuel']
        sparkPlug = request.form.get['sparkPlug']
        tireRotation = request.form.get['tireRotation']

        data = np.array(
            [[year, engineOil, kilometers, breakPad, transmissionFuel,
              sparkPlug, tireRotation]], dtype=np.float64)
        my_prediction = car_main.predict(data)

        return render_template('car_main_result.html', prediction=my_prediction)


@app.route('/enterprise', methods=['POST', 'GET'])
def enterprise():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        # session['email'] = email
        query_user = "SELECT * FROM SERVICE WHERE email = %s AND password = %s"
        data_user = (email, password)
        cursor.execute(query_user, data_user)
        user = cursor.fetchone()

        if user:
            full_name = user[1]
            phone_no = user[5]
            email = user[3]
            detail_user_query = "SELECT * FROM SERVICE WHERE email = %s"
            cursor.execute(detail_user_query, (email,))
            service_user = cursor.fetchone()

            # if service_user:
            detail_user_query1 = "SELECT * FROM DETAILSS WHERE email IN (SELECT USER_EMAIL FROM ADMIN_SERVICE WHERE SERVICE_EMAIL = %s)"
            cursor.execute(detail_user_query1, (email,))
            service_user1 = cursor.fetchall()
            if service_user1:
                # if service_user1:
                detail_user_query2 = "SELECT * FROM MESSAGE WHERE email IN (SELECT USER_EMAIL FROM ADMIN_SERVICE WHERE SERVICE_EMAIL = %s)"
                cursor.execute(detail_user_query2, (email,))
                service_user2 = cursor.fetchall()

                if service_user2:
                    detail_user_query3 = "SELECT COUNT(*) AS count FROM ADMIN_SERVICE WHERE service_email = %s"
                    cursor.execute(detail_user_query3, (email,))
                    service_user3 = cursor.fetchall()
                    return render_template('enterprise_data.html', full_name=full_name, phone_no=phone_no, email=email, service_user=service_user, service_user1=service_user1, service_user2=service_user2, service_user3=service_user3)
                cursor.close()
        else:
            # If user doesn't exist or credentials are incorrect, show an error on the login page
            error = "Invalid Email or password"
            return render_template('enterprise.html', error=error)
        cursor.close()

    # Render the login form for GET requests
    return render_template('enterprise.html', error="")


if __name__ == '__main__':
    app.run(debug=True)
