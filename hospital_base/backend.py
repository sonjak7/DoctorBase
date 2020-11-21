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

        query = 'INSERT INTO staff (firstname, lastname, stafftype) VALUES (%s,%s,%s)'
        data = (fname, lname, type)
        execute_query(db_connection, query, data)
        flash('Staff Added!')
        return render_template('add_staff.html')

#endpoint for search
@webapp.route('/search_staff', methods=['GET', 'POST'])
def search():
    if request.method == "POST":

        search_data = request.form['search_data']

        db_connection = connect_to_database()
        # search by firstName or lastName
        query = "SELECT firstName, lastName, staffType, staffID from staff WHERE firstname LIKE %s OR lastName LIKE %s"
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
    query = "SELECT firstName, lastName, staffType, staffID from staff;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('browse_staff.html', rows=result)

@webapp.route('/orders')
def orders():
    return render_template('orders.html')

@webapp.route('/results')
def results():
    return render_template('results.html')

@webapp.route('/doctors_patients')
def doctors_patients():
    return render_template('doctors_patients.html')

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
