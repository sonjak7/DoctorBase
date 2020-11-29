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

@webapp.route('/add_doctors', methods=['POST','GET'])
def add_doctors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_doctors.html')

    elif request.method == 'POST':
        print("Adding new doctor")
        fname = request.form['fname']
        lname = request.form['lname']
        department = request.form['department']
        query = 'INSERT INTO Doctors (lastName, firstName, department) VALUES (%s,%s,%s)'
        data = (lname, fname, department)
        execute_query(db_connection, query, data)
        flash('Doctor Added!')
        return render_template('add_doctors.html')

@webapp.route('/search_doctors', methods=['GET', 'POST'])
def search_doctors():
    if request.method == "POST":
        print("Searching for a Doctor")
        search_data = request.form['search_data']
        db_connection = connect_to_database()
        # search by firstName or lastName
        query = "SELECT * FROM Doctors WHERE firstName LIKE %s OR lastName LIKE %s"
        data = (search_data, search_data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Doctors Found!")
        return render_template('browse_doctors.html', rows=result)
    return render_template('search_doctors.html')

@webapp.route('/browse_doctors')
def browse_doctors():
    print("Browsing all Doctors")
    db_connection = connect_to_database()
    query = "SELECT * FROM Doctors"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_doctors.html', rows=result)

@webapp.route('/delete_doctors', methods=['POST'])
 def delete_doctors():
     print("Deleting a Doctor")
     db_connection = connect_to_database()
     doctorID = request.form['doctorID']
     query = "DELETE FROM Doctors WHERE doctorID = %s" % (doctorID)
     execute_query(db_connection, query).fetchall()
     flash('Doctor Deleted!')
     return redirect('/browse_doctors')

 @webapp.route('/update_doctors/<int:doctorID>', methods=['POST','GET'])
 def update_doctors(doctorID):
     if request.method == 'GET':     #gather current doctor's information(to fill into text fields)
         print("Updating Doctor")
         db_connection = connect_to_database()
         query = 'SELECT * FROM Doctors WHERE doctorID = %s' % (doctorID)
         result = execute_query(db_connection, query).fetchall()
         return render_template('update_doctors.html', doctor=result)

     elif request.method == 'POST':  #update doctor and return back to all doctors
         db_connection = connect_to_database()
         doctorID = request.form['doctorID']
         fname = request.form['fname']
         lname = request.form['lname']
         department = request.form['department']
         update_query = 'UPDATE Doctors SET firstName = %s, lastName = %s, department = %s WHERE doctorID = %s'
         data = (fname, lname, department, doctorID)
         execute_query(db_connection, update_query, data).fetchall()
         show_query = 'SELECT * FROM Doctors WHERE doctorID = %s' % doctorID
         result = execute_query(db_connection, show_query).fetchall()
         flash('Doctor Updated!')
         return redirect('/browse_doctors')


@webapp.route('/patients')
def patients():
    return render_template('patients.html')

@webapp.route('/add_patients', methods=['POST','GET'])
def add_patients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_patients.html')

    elif request.method == 'POST':
        print("Adding new patient")
        fname = request.form['fname']
        lname = request.form['lname']
        primaryDocID = request.form['primaryDocID']
        query = 'INSERT INTO Patients (lastName, firstName, primaryDoctorID) VALUES (%s,%s,%s)'
        data = (lname, fname, primaryDocID)
        execute_query(db_connection, query, data)
        flash('Patient Added!')
        return render_template('add_patients.html')

@webapp.route('/search_patients', methods=['GET', 'POST'])
def search_patients():
    if request.method == "POST":
        print("Searching for a Patient")
        search_data = request.form['search_data']
        db_connection = connect_to_database()
        # search by firstName or lastName
        query = "SELECT p.patientID, p.firstName, p.lastName, d.lastName FROM Patients p INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID WHERE p.firstName LIKE %s OR p.lastName LIKE %s"
        data = (search_data, search_data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Patients Found!")
        return render_template('browse_patients.html', rows=result)
    return render_template('search_patients.html')

@webapp.route('/browse_patients')
def browse_patients():
    print("Browsing all Patients")
    db_connection = connect_to_database()
    query = "SELECT p.patientID, p.firstName, p.lastName, d.lastName FROM Patients p INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_patients.html', rows=result)

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

@webapp.route('/update_staff/<int:id>', methods=['POST','GET'])
def update_staff(id):
    print('in the update_staff function')
    db_connection = connect_to_database()

    #display existing data
    if request.method == 'GET':
        staff_query = "SELECT firstName, lastName, staffType, staffID from Staff WHERE staffID = %s" % (id)
        staff_result = execute_query(db_connection, staff_query).fetchone()

        if staff_result == None:
            return "No such Staff found!"

        return render_template('update_staff.html', staff = staff_result)
    elif request.method == 'POST':
        staffID = request.form['staffID']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        staffType = request.form['staffType']

        query = "UPDATE Staff SET firstName = %s, lastName = %s, staffType = %s WHERE staffID = %s"
        data = (firstName, lastName, staffType, staffID)
        result = execute_query(db_connection, query, data)
        flash("Updated! " + " Staff ID #" + str(staffID))

        return redirect('/browse_staff')

@webapp.route('/delete_staff/<int:id>')
def delete_people(id):
    '''deletes a staff with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Staff WHERE staffID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Staff ID #" + str(id))

    return redirect('/browse_staff')


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

@webapp.route('/update_order/<int:id>', methods=['POST','GET'])
def update_order(id):
    print('in the update_order function')
    db_connection = connect_to_database()

    #display existing data
    if request.method == 'GET':
        order_query = "SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff, Orders.staffID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID  AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID"
        data = (id,)
        order_result = execute_query(db_connection, order_query, data).fetchone()

        print(order_result)

        staff_query = "SELECT staffID, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Staff;"
        staff_results = execute_query(db_connection, staff_query).fetchall()

        print(staff_results)

        if order_result == None:
            return "No such Order found!"

        return render_template('update_order.html', staff = staff_results, order = order_result)

    elif request.method == 'POST':
        staffID = request.form['staffID']
        orderID = request.form['orderID']

        query = "UPDATE Orders SET staffID = %s WHERE orderID = %s"
        data = (staffID, orderID)
        result = execute_query(db_connection, query, data)
        flash("Updated! " + " Order ID #" + str(orderID))

        return redirect('/browse_orders')


@webapp.route('/delete_order/<int:id>')
def delete_order(id):
    '''deletes an order with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Orders WHERE orderID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Order ID #" + str(id))

    return redirect('/browse_orders')

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
        orderID = request.form['orderID']
        access = request.form['access']
        status = request.form['status']
        date = request.form['date']

        qo = 'SELECT orderID FROM Results WHERE orderID = %s'
        do = (orderID,)
        ro = execute_query(db_connection, qo, do).fetchall()
        co = len(ro)

        if co > 0:
            flash( "Failed: Result for Order Already Exits! Please Update Result!")
            query = 'SELECT Orders.orderID, Patients.lastName from Orders JOIN Patients ON Orders.patientID = Patients.patientID'
            result = execute_query(db_connection, query).fetchall()
            return render_template('add_results.html', orders = result)
        else:
            query = 'INSERT INTO Results (status, orderID, date, accessedByDoctor) VALUES (%s,%s,%s,%s)'
            data = (status, orderID, date, int(access))
            print(query)
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


@webapp.route('/update_result/<int:id_r>/<int:id_o>', methods=['POST','GET'])
def update_result(id_r, id_o):
    print('in the update_result function')
    db_connection = connect_to_database()

    #display existing data
    if request.method == 'GET':
        result_query = "SELECT resultID, status, date, accessedByDoctor from Results WHERE resultID = %s" % (id_r)
        order_query = "SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff, Orders.staffID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID  AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID"
        order_data = (id_o,)
        result_result = execute_query(db_connection, result_query).fetchone()
        order_result = execute_query(db_connection, order_query, order_data).fetchone()

        if result_result == None:
            return "No such Result found!"

        return render_template('update_result.html', result = result_result, order = order_result)
    elif request.method == 'POST':
        resultID = request.form['resultID']
        status = request.form['status']
        access = request.form['access']
        date = request.form['date']

        query = "UPDATE Results SET status = %s, accessedByDoctor = %s, date = %s WHERE resultID = %s"
        data = (status, int(access), date, resultID)
        result = execute_query(db_connection, query, data)
        flash("Updated! " + " Result ID #" + str(resultID))

        return redirect('/browse_results')



@webapp.route('/delete_result/<int:id>')
def delete_result(id):
    '''deletes a result with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Results WHERE resultID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Result ID #" + str(id))

    return redirect('/browse_results')


@webapp.route('/doctors_patients')
def doctors_patients():
    return render_template('doctors_patients.html')


@webapp.route('/add_doctors_patients', methods=['POST','GET'])
def add_doctors_patients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_doctors_patients.html')
    elif request.method == 'POST':
        print("Adding new doctor-patient relationship")
        doc_id = request.form['doc_id']
        pat_id = request.form['pat_id']
        query = 'INSERT INTO Doctors_Patients (doctorID, patientID) VALUES (%s,%s)'
        data = (doc_id, pat_id)
        execute_query(db_connection, query, data)
        flash('Relationship Added!')
        return render_template('add_doctors_patients.html')

@webapp.route('/browse_doctors_patients')
def browse_doctors_patients():
    print("Browsing all doctor-patient relationships")
    db_connection = connect_to_database()
    query = "SELECT d.doctorID, CONCAT(d.firstName, ' ', d.lastName), p.patientID, CONCAT(p.firstName, ' ', p.lastName) FROM Doctors_Patients dp INNER JOIN Doctors d ON d.doctorID = dp.doctorID INNER JOIN Patients p ON p.patientID = dp.patientID"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_doctors_patients.html', rows=result)
