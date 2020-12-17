from flask import Flask, render_template
from flask import request,redirect
from flask import flash
from flask_mysqldb import MySQL
from db_credentials import host, user, password, db_name

#create the web application
webapp = Flask(__name__)
webapp.secret_key = 'secretkey'

webapp.config['MYSQL_HOST'] = host
webapp.config['MYSQL_USER'] = user
webapp.config['MYSQL_PASSWORD'] = password
webapp.config['MYSQL_DB'] = db_name

mysql = MySQL(webapp)

#provide a route where requests on the web application can be addressed
@webapp.route('/')
def home_page():
    return render_template('home.html')


# renders the interface to the doctor page
@webapp.route('/doctors')
def doctors():
    return render_template('doctors.html')


# allows user to add doctors
@webapp.route('/add_doctors', methods=['POST','GET'])
def add_doctors():
    # db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_doctors.html')

    # once add doctor form has been submitted
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        fname = request.form['fname']
        lname = request.form['lname']
        department = request.form['department']
        cur.execute("INSERT INTO Doctors(lastName, firstName, department) VALUES (%s, %s, %s)", (lname, fname, department))
        mysql.connection.commit()
        cur.close()
        flash('Doctor Added!')
        return render_template('add_doctors.html')


# allows user to search doctors
@webapp.route('/search_doctors', methods=['GET', 'POST'])
def search_doctors():
    if request.method == "POST":
        print("Searching for a Doctor")
        search_data = request.form['search_data']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctors WHERE firstName LIKE %s OR lastName LIKE %s", (search_data, search_data))
        result = cur.fetchall()
        cur.close()
        count = len(result)
        flash(str(count) + " Doctors Found!")
        return render_template('browse_doctors.html', rows=result)
    return render_template('search_doctors.html')


# displays all the doctors in the database
@webapp.route('/browse_doctors')
def browse_doctors():
    print("Browsing all Doctors")
    cur = mysql.connection.cursor()
    query = "SELECT * FROM Doctors"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return render_template('browse_doctors.html', rows=result)

# deletes a doctor from the database
@webapp.route('/delete_doctors', methods=['POST'])
def delete_doctors():
    print("Deleting a Doctor")
    cur = mysql.connection.cursor()
    doctorID = request.form['doctorID']
    cur.execute("DELETE FROM Doctors WHERE doctorID = %s" % (doctorID))
    mysql.connection.commit()
    cur.close()
    flash('Doctor Deleted!')
    return redirect('/browse_doctors')


# the doctor Id update is passed in the url
@webapp.route('/update_doctors/<int:doctorID>', methods=['POST','GET'])
def update_doctors(doctorID):
    # pre-fill a form with information about doctor
     if request.method == 'GET':     #gather current doctor's information(to fill into text fields)
        print("Updating Doctor")
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Doctors WHERE doctorID = %s' % (doctorID))
        result = cur.fetchall()
        cur.close()

        return render_template('update_doctors.html', doctor=result[0])

     elif request.method == 'POST':  #update doctor and return back to all doctors
        cur = mysql.connection.cursor()
        doctorID = request.form['doctorID']
        fname = request.form['fname']
        lname = request.form['lname']
        department = request.form['department']
        cur.execute('UPDATE Doctors SET firstName = %s, lastName = %s, department = %s WHERE doctorID = %s', (fname, lname, department, doctorID))
        mysql.connection.commit()
        cur.close()

        flash('Doctor Updated!') # show message to user when successful
        return redirect('/browse_doctors')


# displays the main interface for patient handling
@webapp.route('/patients')
def patients():
    return render_template('patients.html')

# adds a patient to database
@webapp.route('/add_patients', methods=['POST','GET'])
def add_patients():
    # db_connection = connect_to_database()
    if request.method == 'GET':
        # to create a dropdown list of doctors

        cur = mysql.connection.cursor()
        query = 'SELECT doctorID, firstName, lastName FROM Doctors'
        cur.execute(query)
        result = cur.fetchall()
        cur.close()

        return render_template('add_patients.html', doctors=result)
    # submitting new patient to Patients table
    elif request.method == 'POST':
        print("Adding new patient")
        cur = mysql.connection.cursor()
        fname = request.form['fname']
        lname = request.form['lname']
        primaryDocID = request.form['primaryDocID']
        cur.execute('INSERT INTO Patients (lastName, firstName, primaryDoctorID) VALUES (%s,%s,%s)', (lname, fname, primaryDocID))
        mysql.connection.commit()
        cur.close()

        flash('Patient Added!') # show message to user
        return redirect('/add_patients')


# seach a patient by either their first or last name
@webapp.route('/search_patients', methods=['GET', 'POST'])
def search_patients():
    if request.method == "POST":
        print("Searching for a Patient")
        search_data = request.form['search_data']
        cur = mysql.connection.cursor()
        cur.execute("SELECT p.patientID, p.firstName, p.lastName, d.lastName FROM Patients p INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID WHERE p.firstName LIKE %s OR p.lastName LIKE %s", (search_data, search_data))
        result = cur.fetchall()
        cur.close()

        count = len(result)
        flash(str(count) + " Patients Found!")
        return render_template('browse_patients.html', rows=result)
    return render_template('search_patients.html')


# display attributes about all patients in the database
@webapp.route('/browse_patients')
def browse_patients():
    print("Browsing all Patients")
    cur = mysql.connection.cursor()
    query = "SELECT p.patientID, p.firstName, p.lastName, CONCAT(d.firstName , ' ' , d.lastName) FROM Patients p INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    return render_template('browse_patients.html', rows=result)


# deleted patient from the Patients entity
@webapp.route('/delete_patients', methods=['POST'])
def delete_patients():
    print("Deleting a Patient")
    cur = mysql.connection.cursor()
    patientID = request.form['patientID']
    query = "DELETE FROM Patients WHERE patientID = %s" % (patientID)    
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

    flash('Patient Deleted!')
    return redirect('/browse_patients')
    

# update patient in the database
@webapp.route('/update_patients/<int:patientID>', methods=['POST','GET'])
def update_patients(patientID):
     if request.method == 'GET':     #gather current patients's information(to fill into text fields)
        print("Updating Patient")
        cur = mysql.connection.cursor()
        patient_query = 'SELECT * FROM Patients WHERE patientID = %s' % (patientID)
        cur.execute(patient_query)
        patient_result = cur.fetchall()
        doctor_query = 'SELECT doctorID, firstName, lastName FROM Doctors'
        cur.execute(doctor_query)
        doctor_result = cur.fetchall()
        cur.close()

        return render_template('update_patients.html', patient=patient_result[0], doctors=doctor_result)

     elif request.method == 'POST':  #update patient and return back to all patients
        cur = mysql.connection.cursor()
        patientID = request.form['patientID']
        fname = request.form['fname']
        lname = request.form['lname']
        primary = request.form['primary']
        cur.execute('UPDATE Patients SET firstName = %s, lastName = %s, primaryDoctorID = %s WHERE patientID = %s', (fname, lname, primary, patientID))
        mysql.connection.commit()
        cur.close()
         
        flash('Patient Updated!')
        return redirect('/browse_patients')


# get the interface to add/browse/update/delete staff
@webapp.route('/staff')
def staff():
    return render_template('staff.html')


# adds a new row to staff table
@webapp.route('/add_staff', methods=['POST','GET'])
def add_staff():
    # db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_staff.html')
    elif request.method == 'POST':
        print("Add new people!")
        cur = mysql.connection.cursor()
        fname = request.form['fname']
        lname = request.form['lname']
        type = request.form['type']
        cur.execute('INSERT INTO Staff (firstName, lastName, staffType) VALUES (%s,%s,%s)', (fname, lname, type))
        mysql.connection.commit()
        cur.close()

        flash('Staff Added!')
        return render_template('add_staff.html')


# search a staff by their first name or last name
@webapp.route('/search_staff', methods=['GET', 'POST'])
def search_staff():
    if request.method == "POST":
        search_data = request.form['search_data']
        cur = mysql.connection.cursor()
        cur.execute("SELECT firstName, lastName, staffType, staffID from Staff WHERE firstName LIKE %s OR lastName LIKE %s", (search_data, search_data))
        result = cur.fetchall()
        cur.close()
        count = len(result)
        flash(str(count) + " Staff Found!")
        return render_template('browse_staff.html', rows=result)
    return render_template('search_staff.html')


# display all the attributes for each row in the staff table
@webapp.route('/browse_staff')
def browse_staff():
    print("Fetching and rendering Staff web page")
    cur = mysql.connection.cursor()
    query = "SELECT firstName, lastName, staffType, staffID from Staff;"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    return render_template('browse_staff.html', rows=result)


# update the staff with id passed in the url
@webapp.route('/update_staff/<int:id>', methods=['POST','GET'])
def update_staff(id):
    #display existing data about a staff
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        staff_query = "SELECT firstName, lastName, staffType, staffID from Staff WHERE staffID = %s" % (id)
        cur.execute(staff_query)
        staff_result = cur.fetchall()
        cur.close()

        # when staff is not part of Staff table
        if staff_result == None:
            return "No such Staff found!"

        return render_template('update_staff.html', staff = staff_result[0])
    # update staff and show the change in the browse staff page
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        staffID = request.form['staffID']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        staffType = request.form['staffType']
        cur.execute("UPDATE Staff SET firstName = %s, lastName = %s, staffType = %s WHERE staffID = %s", (firstName, lastName, staffType, staffID))
        mysql.connection.commit()
        cur.close()
        flash("Updated! " + " Staff ID #" + str(staffID))
        return redirect('/browse_staff')


# delete a staff from the staff entity
@webapp.route('/delete_staff/<int:id>')
def delete_people(id):
    '''deletes a staff with the given id'''
    cur = mysql.connection.cursor()
    query = "DELETE FROM Staff WHERE staffID = %s" % (id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

    flash("Deleted! " + " Staff ID #" + str(id))

    return redirect('/browse_staff')

# page to display interface for orders
@webapp.route('/orders')
def orders():
    return render_template('orders.html')


# allows users to add orders
@webapp.route('/add_orders', methods=['POST','GET'])
def add_orders():
    cur = mysql.connection.cursor()
    query_patients = "SELECT Patients.patientID, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient FROM Patients"
    query_doc = "SELECT Doctors.doctorID, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor FROM Doctors"
    cur.execute(query_patients)
    result_patients = cur.fetchall()
    cur.execute(query_doc)
    result_doc = cur.fetchall()
    cur.close()

    # pre-fills the dropdown menu with doctor and patient name
    if request.method == 'GET':
        return render_template('add_orders.html', patients = result_patients, doctors = result_doc)
    elif request.method == 'POST':
        print("Add new order!")
        patientID = request.form['patientID']
        doctorID = request.form['doctorID']
        ordertype = request.form['orderType']
        date = request.form['date']
        time = request.form['time']

        # get patient from database
        cur = mysql.connection.cursor()
        qp = "SELECT patientID, primaryDoctorID from Patients WHERE patientID = %s" % (patientID)
        cur.execute(qp)
        rp = cur.fetchall()
        cur.close()

        # get doctor from database
        cur = mysql.connection.cursor()
        qd = "SELECT doctorID from Doctors WHERE doctorID = %s" % (doctorID)
        cur.execute(qd)
        rd = cur.fetchall()
        cur.close()

        # order can only be added if doctor is patient's primary physician
        if rp[0][1] != rd[0][0]:
            flash( "Failed: Doctor is not Patient's Primary Physician!")
            return render_template('add_orders.html', patients = result_patients, doctors = result_doc)
        else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Orders (date, time, orderType, patientID, doctorID) VALUES (%s,%s,%s,%s,%s)', (date, time, ordertype, rp[0][0], rd[0][0]))
            mysql.connection.commit()
            cur.close()

            flash('Success: Order Added!')
            return render_template('add_orders.html', patients = result_patients, doctors = result_doc)


# search orders by patient's name
@webapp.route('/search_orders', methods=['GET', 'POST'])
def search_orders():
    if request.method == "POST":
        search_data = request.form['search_data']
        cur = mysql.connection.cursor()
        cur.execute("SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Patients JOIN Orders ON Patients.patientID = Orders.patientID  AND (Patients.firstName LIKE %s OR Patients.lastName LIKE %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID", (search_data, search_data))
        result = cur.fetchall()
        cur.close()
        count = len(result)
        flash(str(count) + " Orders Found!")
        return render_template('browse_orders.html', rows=result)
    return render_template('search_orders.html')

@webapp.route('/browse_orders')
def browse_orders():
    print("Fetching and rendering Orders web page")
    cur = mysql.connection.cursor()
    query = "SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Orders LEFT JOIN Patients ON Orders.patientID = Patients.patientID LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON Orders.staffID = Staff.staffID;"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    return render_template('browse_orders.html', rows=result)

# allows user to update one order at a time
@webapp.route('/update_order/<int:id>', methods=['POST','GET'])
def update_order(id):
    #display existing data about an order
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        order_query = "SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff, Orders.staffID, Orders.patientID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID  AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID" % (id)
        cur.execute(order_query)
        order_result = cur.fetchall()
        cur.close()
        cur = mysql.connection.cursor()
        staff_query = "SELECT staffID, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Staff;"
        cur.execute(staff_query)
        staff_results = cur.fetchall()
        cur.close()

        return render_template('update_order.html', staff = staff_results, order = order_result[0])

    elif request.method == 'POST':
        staffID = request.form['staffID']
        oldstaffID = request.form['oldstaffID']
        orderID = request.form['orderID']
        patientID = request.form['patientID']

        # update orders table
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Orders SET staffID = %s WHERE orderID = %s", (staffID, orderID))
        mysql.connection.commit()
        cur.close()

        # check if relation is old and update if it is
        cur = mysql.connection.cursor()
        cur.execute('SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s', (oldstaffID, patientID))
        rold = cur.fetchall()
        cur.close()

        # update staff_patients table if relation already exits
        if rold is not None:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE Staff_Patients SET staffID = %s WHERE staffID = %s AND patientID = %s', (staffID, oldstaffID, patientID))
            mysql.connection.commit()
            cur.close()

        # add new relation to staff_patients table if relation is new
        else:
            # check if new relation already exits, add if it doesn't
            cur = mysql.connection.cursor()
            cur.execute('SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s', (staffID, patientID))
            rnew = cur.fetchall()
            cur.close()

            # add new relation
            if rnew is None:
                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO Staff_Patients (staffID, patientID) VALUES (%s,%s)', (staffID, patientID))
                mysql.connection.commit()
                cur.close()

        flash("Updated! " + " Order ID #" + str(orderID))

        return redirect('/browse_orders')


# delete an order based on its id
@webapp.route('/delete_order/<int:id>')
def delete_order(id):
    '''deletes an order with the given id'''
    cur = mysql.connection.cursor()
    query = "DELETE FROM Orders WHERE orderID = %s" % (id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

    flash("Deleted! " + " Order ID #" + str(id))

    return redirect('/browse_orders')

# display the interface to handle results
@webapp.route('/results')
def results():
    return render_template('results.html')

# allows user to add a result for an order in database
@webapp.route('/add_results', methods=['POST','GET'])
def add_results():
    cur = mysql.connection.cursor()
    q1 = 'SELECT Orders.orderID, Patients.lastName, Orders.orderType from Orders JOIN Patients ON Orders.patientID = Patients.patientID'
    cur.execute(q1)
    r1 = cur.fetchall()
    cur.close()

    # pre-fill form with order details
    if request.method == 'GET':
        return render_template('add_results.html', orders = r1)

    elif request.method == 'POST':
        print("Add new Result!")
        orderID = request.form['orderID']
        access = request.form['access']
        status = request.form['status']
        date = request.form['date']

        # check if order already has a result
        cur = mysql.connection.cursor()
        qo = 'SELECT orderID FROM Results WHERE orderID = %s' % (orderID)
        cur.execute(qo)
        ro = cur.fetchall()
        cur.close()
        co = len(ro)

        # cannot add result to order that already has a result (one result per order)
        if co > 0:
            flash( "Failed: Result for Order Already Exits! Please Update Result!")
            return render_template('add_results.html', orders = r1)
        else:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Results (status, orderID, date, accessedByDoctor) VALUES (%s,%s,%s,%s)', (status, orderID, date, int(access)))
            mysql.connection.commit()
            cur.close()

            flash('Result Added!')
            return render_template('add_results.html', orders = r1)


#allows user to filter results by two required category
@webapp.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == "POST":

        filter_status = request.form['filter_status']
        doc_access = int(request.form['doc_access'])
        filter_status_mod = "%"+filter_status+"%"

        # filter by access and status
        cur = mysql.connection.cursor()
        cur.execute("SELECT resultID, status, Results.orderID, Results.date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor, orderType, Patients.lastName FROM Results JOIN Orders ON Results.orderID = Orders.orderID AND Results.accessedByDoctor = %s AND Results.status LIKE %s JOIN Patients ON Orders.patientID = Patients.patientID", (doc_access, filter_status_mod))
        result = cur.fetchall()
        cur.close()

        count = len(result)
        flash(str(count) + " Results Found!")
        return render_template('browse_results.html', rows=result)
    return render_template('search_results.html')


# displays all the results in the database
@webapp.route('/browse_results')
def browse_results():
    cur = mysql.connection.cursor()
    query = "SELECT resultID, status, Results.orderID, Results.date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor, orderType, Patients.lastName FROM Results JOIN Orders ON Results.orderID = Orders.orderID JOIN Patients ON Orders.patientID = Patients.patientID;"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    return render_template('browse_results.html', rows=result)


# updates access and status of result
@webapp.route('/update_result/<int:id_r>/<int:id_o>', methods=['POST','GET'])
def update_result(id_r, id_o):
    #display existing data
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        result_query = "SELECT resultID, status, date, accessedByDoctor from Results WHERE resultID = %s" % (id_r)
        cur.execute(result_query)
        result_result = cur.fetchall()
        order_query = "SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff, Orders.staffID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID  AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID" % (id_o)
        cur.execute(order_query)
        order_result = cur.fetchall() 
        cur.close()

        radio = int.from_bytes(result_result[0][3], "big")
        print(radio)

        if result_result == None:
            return "No such Result found!"

        return render_template('update_result.html', result = result_result[0], order = order_result[0], rad = radio)
    elif request.method == 'POST':
        resultID = request.form['resultID']
        status = request.form['status']
        access = request.form['access']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Results SET status = %s, accessedByDoctor = %s, date = %s WHERE resultID = %s", (status, int(access), date, resultID))
        mysql.connection.commit()
        cur.close()

        flash("Updated! " + " Result ID #" + str(resultID))

        return redirect('/browse_results')


# deleted a result from the result table
@webapp.route('/delete_result/<int:id>')
def delete_result(id):
    '''deletes a result with the given id'''
    cur = mysql.connection.cursor()
    query = "DELETE FROM Results WHERE resultID = %s" % (id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

    flash("Deleted! " + " Result ID #" + str(id))

    return redirect('/browse_results')

# interface for staff_patients relationship
@webapp.route('/staff_patients')
def staff_patients():
    return render_template('staff_patients.html')


# allows user to add new relationship
@webapp.route('/add_staff_patients', methods=['POST','GET'])
def add_staff_patients():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        patient_query = 'SELECT patientID, firstName, lastName FROM Patients'
        cur.execute(patient_query)
        patient_result = cur.fetchall()
        staff_query = 'SELECT staffID, firstName, lastName FROM Staff'
        cur.execute(staff_query)
        staff_result = cur.fetchall() 
        cur.close()

        return render_template('add_staff_patients.html', staff=staff_result, patients=patient_result)

    elif request.method == 'POST':
        print("Adding new staff-patient relationship")
        staf_id = request.form['staf_id']
        pat_id = request.form['pat_id']

        # check if relation already exists
        cur = mysql.connection.cursor()
        cur.execute('SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s', (staf_id, pat_id))
        ro = cur.fetchall()
        cur.close()

        if ro == ():
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Staff_Patients (staffID, patientID) VALUES (%s,%s)', (staf_id, pat_id))
            mysql.connection.commit()
            cur.close()

            flash('Relationship Added!')
        else:
            flash('Error Relation Already Exits!')
        return redirect('add_staff_patients')


# displays all staff patient relation in database
@webapp.route('/browse_staff_patients')
def browse_staff_patients():
    print("Browsing all staff-patient relationships")
    cur = mysql.connection.cursor()
    query = "SELECT d.staffID, CONCAT(d.firstName, ' ', d.lastName), p.patientID, CONCAT(p.firstName, ' ', p.lastName) FROM Staff_Patients dp INNER JOIN Staff d ON d.staffID = dp.staffID INNER JOIN Patients p ON p.patientID = dp.patientID"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    return render_template('browse_staff_patients.html', rows=result)


# remove a staff patient relation from table
@webapp.route('/delete_staff_patients', methods=['POST'])
def delete_staff_patients():
    print("Deleting a Relationship")
    staffID = request.form['staffID']
    patientID = request.form['patientID']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Staff_Patients WHERE staffID = %s AND patientID = %s", (staffID, patientID))
    mysql.connection.commit()
    cur.close()

    flash('Relationship Deleted!')
    return redirect('/browse_staff_patients')


# updates a staff patient relation in staff_patients table
@webapp.route('/update_staff_patients/<int:staffID><int:patientID>', methods=['POST','GET'])
def update_staff_patients(staffID, patientID):
    if request.method == 'GET':     #gather current patients's information(to fill into text fields)
        print("Updating Relationship")
        cur = mysql.connection.cursor()
        patient_query = 'SELECT patientID, firstName, lastName FROM Patients'
        cur.execute(patient_query)
        patient_result = cur.fetchall()
        staff_query = 'SELECT staffID, firstName, lastName FROM Staff'
        cur.execute(staff_query)
        staff_result = cur.fetchall()
        cur.close()

        return render_template('update_staff_patients.html', staffID=staffID, patientID=patientID, staff=staff_result, patients=patient_result)

    elif request.method == 'POST':  #update relationship and return back to all relationships
        oldStaffID = request.form['oldStaffID']
        oldPatientID = request.form['oldPatientID']
        staffID = request.form['staffID']
        patientID = request.form['patientID']
        cur = mysql.connection.cursor()
        cur.execute('SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s', (staffID, patientID))
        ro = cur.fetchall()
        cur.close()

        if ro == ():
            cur = mysql.connection.cursor()
            cur.execute('UPDATE Staff_Patients SET staffID = %s, patientID = %s WHERE staffID = %s AND patientID = %s', (staffID, patientID, oldStaffID, oldPatientID))
            mysql.connection.commit()
            cur.close()

            flash('Relationship Updated!')
            return redirect('/browse_staff_patients')
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Staff_Patients WHERE staffID = %s AND patientID = %s", (oldStaffID, oldPatientID))
        mysql.connection.commit()
        cur.close()

        flash('Relation Already Exits So Relationship Deleted!')
        return redirect('/browse_staff_patients')