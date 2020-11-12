from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/')
def home_page():
    return render_template('home.html')

@webapp.route('/delete')
def delete():
    return render_template('delete.html')

@webapp.route('/inquire')
def inquire():
    return render_template('inquire.html')

@webapp.route('/inquire_doctors')
def inquire_doctors():
    return render_template('inquire_doctors.html')

@webapp.route('/inquire_patients')
def inquire_patients():
    return render_template('inquire_patients.html')

@webapp.route('/inquire_orders')
def inquire_orders():
    return render_template('inquire_orders.html')

@webapp.route('/inquire_results')
def inquire_results():
    return render_template('inquire_results.html')

@webapp.route('/inquire_staff')
def inquire_staff():
    return render_template('inquire_staff.html')

@webapp.route('/add')
def add():
    return render_template('add.html')

@webapp.route('/add_doctors')
def add_doctors():
    return render_template('add_doctors.html')

@webapp.route('/add_patients')
def add_patients():
    return render_template('add_patients.html')

@webapp.route('/add_orders')
def add_orders():
    return render_template('add_orders.html')

@webapp.route('/add_staff')
def add_staff():
    return render_template('add_staff.html')

@webapp.route('/add_results')
def add_results():
    return render_template('add_results.html')

@webapp.route('/update')
def update():
    return render_template('update.html')


