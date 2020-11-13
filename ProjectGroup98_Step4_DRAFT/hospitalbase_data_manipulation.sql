/**/;

/* Database Manipulation Queries for Group 98 CS340 Fall 2020*/;

/* NOTE: Query for add a new character functionality with colon : character being used to 
denote the variables that will have data from the backend programming language
(CITATION: CS340 FALL 2020 Project Step 4 Draft Instructions) */

/* SELECT, INSERT for all tables */

-- Doctors Table
-- search doctors by their first and last name
SELECT doctors.doctorid FROM doctors
WHERE doctors.firstname = :firstnameInput AND doctors.lastname = :lastnameInput;

-- add new doctor
INSERT INTO doctors (lastname, firstname, department)
VALUES (:lastnameInput, :firstnameInput, :departmentInput);

-- Patients Table
-- look up patient by their first and last name
SELECT patients.patientid FROM patients
WHERE patients.firstname = :firstnameInput AND patients.lastname = :lastnameInput;

-- add a new patient
INSERT INTO patients (lastname, firstname, primarydoctorid)
VALUES (:lastnameInput, :firstnameInput, :primarydoctoridInput);

-- Staff Table
-- search staff by their first and last name
SELECT staff.staffid FROM staff
WHERE staff.firstname = :firstnameInput AND staff.lastname = :lastnameInput;

-- add a new staff
INSERT INTO staff (stafftype, lastname, firstname)
VALUES (:stafftypeInput, :lastnameInput, :firstnameInput);

-- Orders Table
-- seach orders by orderid
SELECT orders.orderid FROM orders
WHERE orders.orderid = :orderidInput;

-- add new order (NOTE: staffid is optional)
INSERT INTO orders (date, time, ordertype, patientid, doctorid, staffid)
VALUES (:dateInput, :timeInput, :ordertypeInput, :patientidInput, :doctoridInput, :staffidInput);

-- Results Table
-- get the results of an order
SELECT results.resultid FROM results
WHERE results.orderid = :orderidInput;

-- insert result into order (though this is mostly handled with update)
INSERT INTO results (status, orderid, date, accessedbydoctor)
VALUES (:statusInput, :orderidInput, :dateInput, :accessedbydoctorInput);


/* UPDATE, DELETE For Orders and Results*/

-- update the status of an order
UPDATE results
SET results.status = :statusInput
WHERE results.orderid = :orderidInput;

-- update the staffid for an order (when staff chooses to work on an order)
UPDATE orders
SET orders.staffid = :staffid
WHERE orders.orderid = :orderidInput;

-- delete an order
DELETE FROM torders WHERE orders.orderid = :orderidInput;