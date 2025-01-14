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


# renders the interface to the doctor page
@webapp.route('/doctors')
def doctors():
    return render_template('doctors.html')


# allows user to add doctors
@webapp.route('/add_doctors', methods=['POST','GET'])
def add_doctors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('add_doctors.html')

    # once add doctor form has been submitted
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


# allows user to search doctors
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


# displays all the doctors in the database
@webapp.route('/browse_doctors')
def browse_doctors():
    print("Browsing all Doctors")
    db_connection = connect_to_database()
    query = "SELECT * FROM Doctors"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_doctors.html', rows=result)



# deletes a doctor from the database
@webapp.route('/delete_doctors', methods=['POST'])
def delete_doctors():
     print("Deleting a Doctor")
     db_connection = connect_to_database()
     doctorID = request.form['doctorID']
     query = "DELETE FROM Doctors WHERE doctorID = %s" % (doctorID)
     execute_query(db_connection, query).fetchall()
     flash('Doctor Deleted!')
     return redirect('/browse_doctors')


# the doctor Id update is passed in the url
@webapp.route('/update_doctors/<int:doctorID>', methods=['POST','GET'])
def update_doctors(doctorID):
    # pre-fill a form with information about doctor
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
         query = 'UPDATE Doctors SET firstName = %s, lastName = %s, department = %s WHERE doctorID = %s'
         data = (fname, lname, department, doctorID)
         execute_query(db_connection, query, data).fetchall()
         flash('Doctor Updated!') # show message to user when successful
         return redirect('/browse_doctors')


# displays the main interface for patient handling
@webapp.route('/patients')
def patients():
    return render_template('patients.html')

# adds a patient to database
@webapp.route('/add_patients', methods=['POST','GET'])
def add_patients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        # to create a dropdown list of doctors
        query = 'SELECT doctorID, firstName, lastName FROM Doctors'
        result = execute_query(db_connection, query)
        return render_template('add_patients.html', doctors=result)
    # submitting new patient to Patients table
    elif request.method == 'POST':
        print("Adding new patient")
        fname = request.form['fname']
        lname = request.form['lname']
        primaryDocID = request.form['primaryDocID']
        query = 'INSERT INTO Patients (lastName, firstName, primaryDoctorID) VALUES (%s,%s,%s)'
        data = (lname, fname, primaryDocID)
        execute_query(db_connection, query, data)
        flash('Patient Added!') # show message to user
        return redirect('/add_patients')


# seach a patient by either their first or last name
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


# display attributes about all patients in the database
@webapp.route('/browse_patients')
def browse_patients():
    print("Browsing all Patients")
    db_connection = connect_to_database()
    query = "SELECT p.patientID, p.firstName, p.lastName, CONCAT(d.firstName , ' ' , d.lastName) FROM Patients p INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_patients.html', rows=result)


# deleted patient from the Patients entity
@webapp.route('/delete_patients', methods=['POST'])
def delete_patients():
     print("Deleting a Patient")
     db_connection = connect_to_database()
     patientID = request.form['patientID']
     query = "DELETE FROM Patients WHERE patientID = %s" % (patientID)
     execute_query(db_connection, query).fetchall()
     flash('Patient Deleted!')
     return redirect('/browse_patients')


# update patient in the database
@webapp.route('/update_patients/<int:patientID>', methods=['POST','GET'])
def update_patients(patientID):
     if request.method == 'GET':     #gather current patients's information(to fill into text fields)
         print("Updating Patient")
         db_connection = connect_to_database()
         patient_query = 'SELECT * FROM Patients WHERE patientID = %s' % (patientID)
         patient_result = execute_query(db_connection, patient_query).fetchall()
         doctor_query = 'SELECT doctorID, firstName, lastName FROM Doctors'
         doctor_result = execute_query(db_connection, doctor_query).fetchall()
         return render_template('update_patients.html', patient=patient_result, doctors=doctor_result)

     elif request.method == 'POST':  #update patient and return back to all patients
         db_connection = connect_to_database()
         patientID = request.form['patientID']
         fname = request.form['fname']
         lname = request.form['lname']
         primary = request.form['primary']
         query = 'UPDATE Patients SET firstName = %s, lastName = %s, primaryDoctorID = %s WHERE patientID = %s'
         data = (fname, lname, primary, patientID)
         execute_query(db_connection, query, data).fetchall()
         flash('Patient Updated!')
         return redirect('/browse_patients')


# get the interface to add/browse/update/delete staff
@webapp.route('/staff')
def staff():
    return render_template('staff.html')


# adds a new row to staff table
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



# search a staff by their first name or last name
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



# display all the attributes for each row in the staff table
@webapp.route('/browse_staff')
def browse_staff():
    print("Fetching and rendering Staff web page")
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, staffType, staffID from Staff;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_staff.html', rows=result)


# update the staff with id passed in the url
@webapp.route('/update_staff/<int:id>', methods=['POST','GET'])
def update_staff(id):
    print('in the update_staff function')
    db_connection = connect_to_database()

    #display existing data about a staff
    if request.method == 'GET':
        staff_query = "SELECT firstName, lastName, staffType, staffID from Staff WHERE staffID = %s" % (id)
        staff_result = execute_query(db_connection, staff_query).fetchone()

        # when staff is not part of Staff table
        if staff_result == None:
            return "No such Staff found!"

        return render_template('update_staff.html', staff = staff_result)
    # update staff and show the change in the browse staff page
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


# delete a staff from the staff entity
@webapp.route('/delete_staff/<int:id>')
def delete_people(id):
    '''deletes a staff with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Staff WHERE staffID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Staff ID #" + str(id))

    return redirect('/browse_staff')

# page to display interface for orders
@webapp.route('/orders')
def orders():
    return render_template('orders.html')


# allows users to add orders
@webapp.route('/add_orders', methods=['POST','GET'])
def add_orders():
    db_connection = connect_to_database()
    query_patients = "SELECT Patients.patientID, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient FROM Patients"
    query_doc = "SELECT Doctors.doctorID, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor FROM Doctors"
    result_patients = execute_query(db_connection, query_patients).fetchall()
    result_doc = execute_query(db_connection, query_doc).fetchall()

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
        qp = "SELECT patientID, primaryDoctorID from Patients WHERE patientID = %s"
        dp = (patientID,)
        rp = execute_query(db_connection, qp, dp).fetchall()
        cp = len(rp)

        # get doctor from database
        qd = "SELECT doctorID from Doctors WHERE doctorID = %s"
        dd = (doctorID,)
        rd = execute_query(db_connection, qd, dd).fetchall()
        cd = len(rd)

        # order can only be added if doctor is patient's primary physician
        if rp[0][1] != rd[0][0]:
            flash( "Failed: Doctor is not Patient's Primary Physician!")
            return render_template('add_orders.html', patients = result_patients, doctors = result_doc)
        else:
            qo = 'INSERT INTO Orders (date, time, orderType, patientID, doctorID) VALUES (%s,%s,%s,%s,%s)'
            do = (date, time, ordertype, rp[0][0], rd[0][0])
            execute_query(db_connection, qo, do)
            flash('Success: Order Added!')
            return render_template('add_orders.html', patients = result_patients, doctors = result_doc)


# search orders by patient's name
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
def browse_orders():
    print("Fetching and rendering Orders web page")
    db_connection = connect_to_database()
    query = "SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Orders LEFT JOIN Patients ON Orders.patientID = Patients.patientID LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON Orders.staffID = Staff.staffID;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_orders.html', rows=result)

# allows user to update one order at a time
@webapp.route('/update_order/<int:id>', methods=['POST','GET'])
def update_order(id):
    print('in the update_order function')
    db_connection = connect_to_database()

    #display existing data about an order
    if request.method == 'GET':
        order_query = "SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff, Orders.staffID, Orders.patientID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID  AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID LEFT JOIN Staff ON  Staff.staffID = Orders.staffID"
        data = (id,)
        order_result = execute_query(db_connection, order_query, data).fetchone()


        staff_query = "SELECT staffID, CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff FROM Staff;"
        staff_results = execute_query(db_connection, staff_query).fetchall()


        if order_result == None:
            return "No such Order found!"

        return render_template('update_order.html', staff = staff_results, order = order_result)

    elif request.method == 'POST':
        staffID = request.form['staffID']
        oldstaffID = request.form['oldstaffID']
        orderID = request.form['orderID']
        patientID = request.form['patientID']

        print("LOOK HERE")
        print(staffID == 'None')
        print(staffID)

        if staffID == oldstaffID:
            flash("NOTHING Update! " )
            return redirect('/browse_orders')
        elif staffID == 'None':
            # update orders table
            query = "UPDATE Orders SET staffID = NULL WHERE orderID = %s"
            data = (orderID, )
            result = execute_query(db_connection, query, data)

            # check if relation is old and update if it is
            qold = 'SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s'
            dold = (oldstaffID, patientID)
            rold = execute_query(db_connection, qold, dold).fetchone()

            # delete previous relation from  staff_patients table
            if rold is not None:
                qupd = 'DELETE FROM Staff_Patients WHERE staffID = %s AND patientID = %s'
                dupd = (oldstaffID, patientID)
                execute_query(db_connection, qupd, dupd)

            flash("Updated! " + " Order ID #" + str(orderID))

            return redirect('/browse_orders')
        else:
            # update orders table
            query = "UPDATE Orders SET staffID = %s WHERE orderID = %s"
            data = (staffID, orderID)
            result = execute_query(db_connection, query, data)

            # check if relation is old and update if it is
            qold = 'SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s'
            dold = (oldstaffID, patientID)
            rold = execute_query(db_connection, qold, dold).fetchone()

            # update staff_patients table if relation already exits
            if rold is not None:
                qupd = 'UPDATE Staff_Patients SET staffID = %s WHERE staffID = %s AND patientID = %s'
                dupd = (staffID, oldstaffID, patientID)
                execute_query(db_connection, qupd, dupd)
            # add new relation to staff_patients table if relation is new
            else:
                # check if new relation already exits, add if it doesn't
                qnew = 'SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s'
                dnew = (staffID, patientID)
                rnew = execute_query(db_connection, qnew, dnew).fetchone()

                # add new relation
                if rnew is None:
                    query2 = 'INSERT INTO Staff_Patients (staffID, patientID) VALUES (%s,%s)'
                    data2 = (staffID, patientID)
                    execute_query(db_connection, query2, data2)

            flash("Updated! " + " Order ID #" + str(orderID))

            return redirect('/browse_orders')





# delete an order based on its id
@webapp.route('/delete_order/<int:id>')
def delete_order(id):
    '''deletes an order with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Orders WHERE orderID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Order ID #" + str(id))

    return redirect('/browse_orders')

# display the interface to handle results
@webapp.route('/results')
def results():
    return render_template('results.html')


# allows user to add a result for an order in database
@webapp.route('/add_results', methods=['POST','GET'])
def add_results():
    db_connection = connect_to_database()
    q1 = 'SELECT Orders.orderID, Patients.lastName, Orders.orderType from Orders JOIN Patients ON Orders.patientID = Patients.patientID'
    r1 = execute_query(db_connection, q1).fetchall()
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
        qo = 'SELECT orderID FROM Results WHERE orderID = %s'
        do = (orderID,)
        ro = execute_query(db_connection, qo, do).fetchall()
        co = len(ro)
        # cannot add result to order that already has a result (one result per order)
        if co > 0:
            flash( "Failed: Result for Order Already Exits! Please Update Result!")
            return render_template('add_results.html', orders = r1)
        else:
            query = 'INSERT INTO Results (status, orderID, date, accessedByDoctor) VALUES (%s,%s,%s,%s)'
            data = (status, orderID, date, int(access))
            execute_query(db_connection, query, data)
            flash('Result Added!')
            return render_template('add_results.html', orders = r1)


#allows user to filter results by two required category
@webapp.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == "POST":

        filter_status = request.form['filter_status']
        doc_access = int(request.form['doc_access'])
        filter_status_mod = "%"+filter_status+"%"
        db_connection = connect_to_database()

        # filter by access and status
        query = "SELECT resultID, status, Results.orderID, Results.date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor, orderType, Patients.lastName FROM Results JOIN Orders ON Results.orderID = Orders.orderID AND Results.accessedByDoctor = %s AND Results.status LIKE %s JOIN Patients ON Orders.patientID = Patients.patientID"
        data = (doc_access, filter_status_mod)
        print(data)
        result = execute_query(db_connection, query, data).fetchall()
        count = len(result)
        flash(str(count) + " Results Found!")
        return render_template('browse_results.html', rows=result)
    return render_template('search_results.html')


# displays all the results in the database
@webapp.route('/browse_results')
def browse_results():
    db_connection = connect_to_database()
    query = "SELECT resultID, status, Results.orderID, Results.date, CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO' END AS accessedByDoctor, orderType, Patients.lastName FROM Results JOIN Orders ON Results.orderID = Orders.orderID JOIN Patients ON Orders.patientID = Patients.patientID;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_results.html', rows=result)


# updates access and status of result
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

        print("LOOK HERE")
        radio = int.from_bytes(result_result[3], "big")
        print(radio)


        if result_result == None:
            return "No such Result found!"

        return render_template('update_result.html', result = result_result, order = order_result, rad = radio)
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


# deleted a result from the result table
@webapp.route('/delete_result/<int:id>')
def delete_result(id):
    '''deletes a result with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Results WHERE resultID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    flash("Deleted! " + " Result ID #" + str(id))

    return redirect('/browse_results')


# interface for staff_patients relationship
@webapp.route('/staff_patients')
def staff_patients():
    return render_template('staff_patients.html')


# allows user to add new relationship
@webapp.route('/add_staff_patients', methods=['POST','GET'])
def add_staff_patients():
    db_connection = connect_to_database()
    if request.method == 'GET':
        patient_query = 'SELECT patientID, firstName, lastName FROM Patients'
        patient_result = execute_query(db_connection, patient_query)
        staff_query = 'SELECT staffID, firstName, lastName FROM Staff'
        staff_result = execute_query(db_connection, staff_query)
        return render_template('add_staff_patients.html', staff=staff_result, patients=patient_result)

    elif request.method == 'POST':
        print("Adding new staff-patient relationship")
        staf_id = request.form['staf_id']
        pat_id = request.form['pat_id']

        # check if relation already exists
        qo = 'SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s'
        do = (staf_id, pat_id)
        ro = execute_query(db_connection, qo, do).fetchone()

        if ro is None:
            query = 'INSERT INTO Staff_Patients (staffID, patientID) VALUES (%s,%s)'
            data = (staf_id, pat_id)
            execute_query(db_connection, query, data)
            flash('Relationship Added!')
        else:
            flash('Error Relation Already Exits!')
        return redirect('add_staff_patients')


# displays all staff patient relation in database
@webapp.route('/browse_staff_patients')
def browse_staff_patients():
    print("Browsing all staff-patient relationships")
    db_connection = connect_to_database()
    query = "SELECT d.staffID, CONCAT(d.firstName, ' ', d.lastName), p.patientID, CONCAT(p.firstName, ' ', p.lastName) FROM Staff_Patients dp INNER JOIN Staff d ON d.staffID = dp.staffID INNER JOIN Patients p ON p.patientID = dp.patientID"
    result = execute_query(db_connection, query).fetchall()
    return render_template('browse_staff_patients.html', rows=result)


# remove a staff patient relation from table
@webapp.route('/delete_staff_patients', methods=['POST'])
def delete_staff_patients():
    print("Deleting a Relationship")
    db_connection = connect_to_database()
    staffID = request.form['staffID']
    patientID = request.form['patientID']
    query = "DELETE FROM Staff_Patients WHERE staffID = %s AND patientID = %s"
    data = (staffID, patientID)
    execute_query(db_connection, query, data).fetchall()
    flash('Relationship Deleted!')
    return redirect('/browse_staff_patients')


# updates a staff patient relation in staff_patients table
@webapp.route('/update_staff_patients/<int:staffID><int:patientID>', methods=['POST','GET'])
def update_staff_patients(staffID, patientID):
    if request.method == 'GET':     #gather current patients's information(to fill into text fields)
        print("Updating Relationship")
        db_connection = connect_to_database()
        patient_query = 'SELECT patientID, firstName, lastName FROM Patients'
        patient_result = execute_query(db_connection, patient_query)
        staff_query = 'SELECT staffID, firstName, lastName FROM Staff'
        staff_result = execute_query(db_connection, staff_query)
        return render_template('update_staff_patients.html', staffID=staffID, patientID=patientID, staff=staff_result, patients=patient_result)

    elif request.method == 'POST':  #update relationship and return back to all relationships
        db_connection = connect_to_database()
        oldStaffID = request.form['oldStaffID']
        oldPatientID = request.form['oldPatientID']
        staffID = request.form['staffID']
        patientID = request.form['patientID']

        qo = 'SELECT staffID, patientID FROM Staff_Patients WHERE staffID = %s and patientID = %s'
        do = (staffID, patientID)
        ro = execute_query(db_connection, qo, do).fetchone()

        if ro is None:
            query = 'UPDATE Staff_Patients SET staffID = %s, patientID = %s WHERE staffID = %s AND patientID = %s'
            data = (staffID, patientID, oldStaffID, oldPatientID)
            execute_query(db_connection, query, data).fetchall()
            flash('Relationship Updated!')
            return redirect('/browse_staff_patients')

        query = "DELETE FROM Staff_Patients WHERE staffID = %s AND patientID = %s"
        data = (oldStaffID, oldPatientID)
        execute_query(db_connection, query, data).fetchall()
        flash('Relation Already Exits So Relationship Deleted!')
        return redirect('/browse_staff_patients')
