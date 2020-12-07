/**/;

/* Database Manipulation Queries for Group 98 CS340 Fall 2020*/;

/* NOTE: Query for add a new character functionality with colon : character being used to 
denote the variables that will have data from the backend programming language
(CITATION: CS340 FALL 2020 Project Step 4 Draft Instructions) */

/* SELECT, INSERT for all tables */

-- Doctors Table
-- get all doctors' id, first name, last name, and department for listing all doctors
SELECT * FROM Doctors;

-- search doctors by their first and last name
SELECT Doctors.doctorID FROM Doctors
WHERE Doctors.firstName = :firstNameInput AND Doctors.lastName = :lastNameInput;
--in python/flask
SELECT * FROM Doctors WHERE firstName LIKE :firstNameInput OR lastName LIKE :lastNameInput;

-- add new doctor
INSERT INTO Doctors (lastName, firstName, department)
VALUES (:lastNameInput, :firstNameInput, :departmentInput);

-- Patients Table
--get all patients' first name, last name, and primary doctor's last name for listing all patients
SELECT p.patientID, p.firstName, p.lastName,
CONCAT(d.firstName , ' ' , d.lastName)
FROM Patients p INNER JOIN Doctors d 
ON p.primaryDoctorID = d.doctorID;

-- look up patient by their first and last name
SELECT Patients.patientID FROM Patients
WHERE Patients.firstName = :firstNameInput AND Patients.lastName = :lastNameInput;

-- for python/flask
SELECT p.patientID, p.firstName, p.lastName, d.lastName FROM Patients p
INNER JOIN Doctors d ON p.primaryDoctorID = d.doctorID WHERE p.firstName
LIKE :patientfirstnameInput OR p.lastName LIKE :patientlastnameInput:

-- add a new patient
INSERT INTO Patients (lastName, firstName, primaryDoctorID)
VALUES (:lastNameInput, :firstNameInput, :primaryDoctorIDInput);

-- Staff Table
--get all staff' first name, last name, and type for listing all staff
SELECT * FROM Staff;

-- search staff
SELECT Staff.staffID FROM Staff
WHERE Staff.firstName = :firstNameInput AND Staff.lastName = :lastNameInput;

--python/flask
SELECT firstName, lastName, staffType, staffID
from Staff WHERE firstName LIKE :firstNameInput OR lastName LIKE :lastNameInput;

SELECT firstName, lastName, staffType, staffID from Staff;

SELECT firstName, lastName, staffType, staffID from Staff WHERE firstName
LIKE :firstNameInput OR lastName LIKE :lastNameInput;
-- add a new staff
INSERT INTO Staff (staffType, lastName, firstName)
VALUES (:staffTypeInput, :lastNameInput, :firstNameInput);

-- Orders Table
--get all order's date, time, type, associated patient's, doctor's, and staff's last name (if exists)
SELECT o.orderID, o.date, o.time, o.orderType, p.lastName AS "Patient's Name",
d.lastName AS "Doctor's Name", s.lastName AS "Staff's Name" FROM Orders o 
INNER JOIN Patients p ON o.patientID = p.patientID
INNER JOIN Doctors d ON o.doctorID = d.doctorID
INNER JOIN Staff s ON o.staffID = s.staffID;

-- search Orders
SELECT Orders.orderID FROM Orders
WHERE Orders.orderID = :orderIDInput;

SELECT Orders.orderID, Orders.date, Orders.time, Orders.orderType,
CONCAT(Patients.firstName , ' ' , Patients.lastName) AS Patient,
CONCAT(Doctors.firstName , ' ' , Doctors.lastName) AS Doctor,
CONCAT(Staff.firstName , ' ' , Staff.lastName) AS Staff
FROM Patients JOIN Orders ON Patients.patientID = Orders.patientID 
AND (Patients.firstName LIKE :firstNameInput OR Patients.lastName LIKE :lastNameInput)
LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID
LEFT JOIN Staff ON  Staff.staffID = Orders.staffID;

-- add new order (NOTE: staffID is optional)
INSERT INTO Orders (date, time, orderType, patientID, doctorID, staffID)
VALUES (:dateInput, :timeInput, :orderTypeInput, :patientIDInput, :doctorIDInput, :staffIDInput);

-- Results Table
--get all result's status, date, `accessedByDoctor`, and associated order type
SELECT * FROM Results;

SELECT resultID, status, orderID, date,
CASE WHEN accessedByDoctor = 1 THEN 'YES' ELSE 'NO'
END AS accessedByDoctor FROM Results WHERE Results.accessedByDoctor = :accessInput
AND Results.status LIKE :statusInput;

SELECT Orders.orderID, Orders.orderType, CONCAT(Patients.firstName , ' ' , Patients.lastName)
AS Patient, CONCAT(Doctors.firstName , ' ' , Doctors.lastName)
AS Doctor, CONCAT(Staff.firstName , ' ' , Staff.lastName)
AS Staff, Orders.staffID FROM Patients JOIN Orders ON (Patients.patientID = Orders.patientID 
AND Orders.orderID = %s) LEFT JOIN Doctors ON Orders.doctorID = Doctors.doctorID
LEFT JOIN Staff ON  Staff.staffID = Orders.staffID;

-- get the results of an order
SELECT Results.resultID FROM Results
WHERE Results.orderID = :orderIDInput;

-- insert result into order (though this is mostly handled with update)
INSERT INTO Results (status, orderID, date, accessedByDoctor)
VALUES (:statusInput, :orderIDInput, :dateInput, :accessedByDoctorInput);

-- Staff_Patients Table
-- get all staff-patient relationships, list staff's last name and patient's first/last name
SELECT s.lastName AS "Staff's name", CONCAT(p.firstName, ' ', p.lastName) AS "Patient's Name"
FROM Staff_Patients sp
INNER JOIN Staff s ON s.staffID = sp.staffID
INNER JOIN Patients p ON p.patientID = sp.patientID;

-- insert new relationship between patient and doctor
INSERT INTO Doctors_Patients (doctorID, patientID)
VALUES (:doctorIDInput, :patientIDInput);


/* UPDATE, DELETE For all tables*/

-- update the status of an order
UPDATE Results
SET Results.status = :statusInput
WHERE Results.orderID = :orderIDInput;

-- update the staffID for an order (when staff chooses to work on an order)
UPDATE Orders
SET Orders.staffID = :staffIDInput
WHERE Orders.orderID = :orderIDInput;

-- delete an order
DELETE FROM Orders WHERE Orders.orderID = :orderIDInput;

/*
NOTE: For updating doctors, patients, and staff, only what needs to be changed will be changed. Front-end
should automatically fill in old information into text fields to allow this to happen
*/

--update a doctor(change of department, name, etc.)
UPDATE Doctors
SET firstName = :firstNameInput, lastName = :lastNameInput, department = :departmentInput
WHERE doctorID = :doctorIDInput; 

--update a patient(change of primary doctor, name, etc.)
UPDATE Patients
SET firstName = :firstNameInput, lastName = :lastNameInput, primaryDoctorID = :primaryDoctorIDInput
WHERE patientID = :patientIDInput;

--update a staff(change of type, name, etc.)
UPDATE Staff
SET firstName = :firstNameInput, lastName = :lastNameInput, staffType = :staffTypeInput
WHERE staffID = :staffIDInput;

--delete a doctor(quits job)
DELETE FROM Doctors WHERE doctorID = :doctorIDInput;

--delete a patient(switches hospital)
DELETE FROM Patients WHERE patientID = :patientIDInput;

--delete a staff(quits job)
DELETE FROM Staff WHERE staffID = :staffIDInput;

--delete staff-patient relationship(order is deleted/patient is deleted/staff is deleted from database)
DELETE FROM Staff_Patients WHERE staffID = :staffIDInput AND patientID = :patientIDInput;
