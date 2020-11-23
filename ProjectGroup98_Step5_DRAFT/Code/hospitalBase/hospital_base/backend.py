from flask import Flask, render_template
from flask import request,redirect
from flask import flash
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
webapp.secret_key = 'secretkey'
#provide a route where requests on the web application can be addressed
@webapp.route('/')
def home_page():
    return render_template('home.html')

@webapp.route('/doctors')
def doctors():
    return render_template('doctors.html')


@webapp.route('/patients')
def patients():
    return render_template('patients.html')

@webapp.route('/staff')
def staff():
    return render_template('staff.html')

@webapp.route('/add_staff', methods=['POST','GET'])
def add_staff():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_staff.html')
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fname']
        lname = request.form['lname']
        type = request.form['type']

        query = 'INSERT INTO Staff (firstName, lastName, staffType) VALUES (%s,%s,%s)'
        data = (fname, lname, type)
        execute_query(db_connection, query, data)
        flash('Staff Added!')
        return render_template('add_staff.html')

#endpoint for search
@webapp.route('/search_staff', methods=['GET', 'POST'])
def search_staff():
    if request.method == "POST":

        search_data = request.form['search_data']

        db_connection = connect_to_database()
        # search by firstName or lastName
        query = "SELECT firstName, lastName, staffType, staffID from Staff WHERE firstName LIKE %s OR lastName LIKE %s"
        data = (search_data, search_data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Staff Found!")
        return render_template('browse_staff.html', rows=result)
    return render_template('search_staff.html')

@webapp.route('/browse_staff')
#the name of this function is just a cosmetic thing
def browse_staff():
    print("Fetching and rendering Staff web page")
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, staffType, staffID from Staff;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_staff.html', rows=result)

@webapp.route('/orders')
def orders():
    return render_template('orders.html')

@webapp.route('/add_orders', methods=['POST','GET'])
def add_orders():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_orders.html')
    elif request.method == 'POST':
        print("Add new order!")
        pfname = request.form['pfname']
        plname = request.form['plname']
        dfname = request.form['dfname']
        dlname = request.form['dlname']
        ordertype = request.form['orderType']
        date = request.form['date']
        time = request.form['time']

        # get patient from database
        qp = "SELECT patientID, primaryDoctorID from Patients WHERE firstName LIKE %s AND lastName LIKE %s"
        dp = (pfname, plname)
        rp = execute_query(db_connection, qp, dp).fetchall()
        cp = len(rp)

        # get doctor from database
        qd = "SELECT doctorID from Doctors WHERE firstName LIKE %s AND lastName LIKE %s"
        dd = (dfname, dlname)
        rd = execute_query(db_connection, qd, dd).fetchall()
        cd = len(rd)

        if cp == 0:
            flash( "Failed: Patient Not Found!")
            return render_template('add_orders.html')
        elif cd == 0:
            flash( "Failed: Doctor Not Found!")
            return render_template('add_orders.html')
        elif rp[0][1] != rd[0][0]:
            flash( "Failed: Doctor is not Patient's Primary Physician!")
            return render_template('add_orders.html')
        else:
            qo = 'INSERT INTO Orders (date, time, orderType, patientID, doctorID) VALUES (%s,%s,%s,%s,%s)'
            do = (date, time, ordertype, rp[0][0], rd[0][0])
            execute_query(db_connection, qo, do)
            flash('Success: Order Added!')
            return render_template('add_orders.html')

@webapp.route('/search_orders', methods=['GET', 'POST'])
def search_orders():
    if request.method == "POST":

        search_data = request.form['search_data']

        db_connection = connect_to_database()
        # search by firstName or lastName
        query = "SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Patients JOIN Orders ON Patients.patientID = Orders.patientID  AND (Patients.firstName LIKE %s OR Patients.lastName LIKE %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID"
        data = (search_data, search_data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Orders Found!")
        return render_template('browse_orders.html', rows=result)
    return render_template('search_orders.html')

@webapp.route('/browse_orders')
#the name of this function is just a cosmetic thing
def browse_orders():
    print("Fetching and rendering Orders web page")
    db_connection = connect_to_database()
    query = "SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Orders LEFT JOIN Patients ON Orders.patientID = Patients.patientID LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON Orders.staffID = Staff.staffID;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_orders.html', rows=result)

@webapp.route('/results')
def results():
    return render_template('results.html')

@webapp.route('/add_results', methods=['POST','GET'])
def add_results():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT Orders.orderID, Patients.lastName from Orders JOIN Patients ON Orders.patientID = Patients.patientID'
        result = execute_query(db_connection, query).fetchall()
        return render_template('add_results.html', orders = result)
    elif request.method == 'POST':
        print("Add new Result!")
        orderid = request.form['orderID']
        access = request.form['access']
        status = request.form['status']
        date = request.form['date']

        query = 'INSERT INTO Results (status, orderID, date, accessedByDoctor) VALUES (%s,%s,%s,%s)'
        data = (status, orderid, date, access)
        execute_query(db_connection, query, data)
        flash('Result Added!')
        return render_template('add_results.html')

@webapp.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == "POST":

        filter_status = request.form['filter_status']
        doc_access = int(request.form['doc_access'])
        filter_status_mod = "%"+filter_status+"%"
        db_connection = connect_to_database()

        # filter by access and status
        query = "SELECT resultID, status, orderID, date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor FROM Results WHERE Results.accessedByDoctor = %s AND Results.status LIKE %s"
        data = (doc_access, filter_status_mod)
        print(data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Results Found!")
        return render_template('browse_results.html', rows=result)
    return render_template('search_results.html')

@webapp.route('/browse_results')
#the name of this function is just a cosmetic thing
def browse_results():
    print("Fetching and rendering Result web page")
    db_connection = connect_to_database()
    query = "SELECT resultID, status, orderID, date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor FROM Results;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_results.html', rows=result)

@webapp.route('/browse_doctors_patients')
def browse_doctors_patients():
    print("Fetching and rendering Doctor-Patient web page")
    db_connection = connect_to_database()
    query = "SELECT CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor FROM Patients LEFT JOIN Doctors ON Patients.primaryDoctorID = Doctors.doctorID;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_doctors_patients.html', rows=result)

# @webapp.route('/delete')
# def delete():
#     return render_template('delete.html')

# @webapp.route('/inquire')
# def inquire():
#     return render_template('inquire.html')

# @webapp.route('/inquire_doctors')
# def inquire_doctors():
#     return render_template('inquire_doctors.html')

# @webapp.route('/inquire_patients')
# def inquire_patients():
#     return render_template('inquire_patients.html')

# @webapp.route('/inquire_orders')
# def inquire_orders():
#     return render_template('inquire_orders.html')

# @webapp.route('/inquire_results')
# def inquire_results():
#     return render_template('inquire_results.html')

# @webapp.route('/add')
# def add():
#     return render_template('add.html')

# @webapp.route('/add_doctors')
# def add_doctors():
#     return render_template('add_doctors.html')

# @webapp.route('/add_patients')
# def add_patients():
#     return render_template('add_patients.html')

# @webapp.route('/add_orders')
# def add_orders():
#     return render_template('add_orders.html')


# @webapp.route('/add_results')
# def add_results():
#     return render_template('add_results.html')

# @webapp.route('/update')
# def update():
#     return render_template('update.html')
