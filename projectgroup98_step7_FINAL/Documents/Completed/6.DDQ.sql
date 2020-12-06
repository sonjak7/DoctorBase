/**/;

/* Database calls for Group 98 CS340 Fall 2020*/;

/* (a) Database Definition Queries */

/* Create a table for Doctors */

DROP TABLE IF EXISTS `Doctors`;

CREATE TABLE `Doctors` (
  `doctorID` int(11) NOT NULL AUTO_INCREMENT,
  `lastName` varchar(255) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL,
  PRIMARY KEY (`doctorID`)
);

/* Create a table for Staff */

DROP TABLE IF EXISTS `Staff`;

CREATE TABLE `Staff` (
  `staffID` int(11) NOT NULL AUTO_INCREMENT,
  `staffType` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  PRIMARY KEY (`staffID`)
);

/* Create a table for Patients */

DROP TABLE IF EXISTS `Patients`;

CREATE TABLE `Patients` (
  `patientID` int(11) NOT NULL AUTO_INCREMENT,
  `lastName` varchar(255) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `primaryDoctorID` int(11) NOT NULL,
  PRIMARY KEY (`patientID`),
  FOREIGN KEY (`primaryDoctorID`) REFERENCES `Doctors` (`doctorID`)
  ON DELETE CASCADE
);


/* Create a table for Orders */

DROP TABLE IF EXISTS `Orders`;

CREATE TABLE `Orders` (
  `orderID` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `orderType` varchar(255) NOT NULL,
  `patientID` int(11) NOT NULL,
  `doctorID` int(11) NOT NULL,
  `staffID` int(11),
  PRIMARY KEY (`orderID`),
  FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`)
  ON DELETE CASCADE,
  FOREIGN KEY (`doctorID`) REFERENCES `Doctors` (`doctorID`)
  ON DELETE CASCADE,
  FOREIGN KEY (`staffID`) REFERENCES `Staff` (`staffID`)
  ON DELETE CASCADE
);

/* Create a table for Results */

DROP TABLE IF EXISTS `Results`;

CREATE TABLE `Results` (
  `resultID` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) NOT NULL,
  `orderID` int(11) NOT NULL,
  `date` date,
  `accessedByDoctor` bit(1) DEFAULT b'0',
  PRIMARY KEY (`resultID`),
  FOREIGN KEY (`orderID`) REFERENCES `Orders` (`orderID`)
  ON DELETE CASCADE
);

/* Create a table for Staff_Patients relationship */

DROP TABLE IF EXISTS `Staff_Patients`;

CREATE TABLE `Staff_Patients` (
  `staffID` int(11) NOT NULL,
  `patientID` int(11) NOT NULL,
  PRIMARY KEY (`staffID`, `patientID`),
  FOREIGN KEY (`staffID`) REFERENCES `Staff` (`staffID`)
  ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`patientID`) REFERENCES `Patients` (`patientID`)
  ON UPDATE CASCADE ON DELETE CASCADE
);

/* (b) Sample Data */

/* Insert into Doctors --> 5 doctors */

LOCK TABLES `Doctors` WRITE;
INSERT INTO `Doctors` VALUES
(1,'Carson','Ben', 'Neurology'),
(2,'Mukherjee','Siddharth', 'Oncology'),
(3,'Gawande','Atul', 'Endocrinology'),
(4,'Sacks','Oliver', 'Neurology'),
(5,'of Kos','Hippocrates', 'Internal Medicine');
UNLOCK TABLES;

/* Insert into Patients --> 5 patients */

LOCK TABLES `Patients` WRITE;
INSERT INTO `Patients` VALUES
(1,'Bechdel','Alison', 4),
(2,'McCraney','Tarell', 2),
(3,'Diaz','Junot', 5),
(4,'Patel','Shwetak', 3),
(5,'Duflo','Esther', 1);
UNLOCK TABLES;

/* Insert into Staff --> 5 staff */

LOCK TABLES `Staff` WRITE;
INSERT INTO `Staff` VALUES
(1,'pathology', 'Pasteur','Louis'),
(2,'nursing','Nightingale','Florence'),
(3,'radiology', 'Damadian','Raymond'),
(4,'pharmacy', 'Dauerer','Maria'),
(5,'pharmacy', 'Pankiewicz','Tadeusz');
UNLOCK TABLES;

/* Insert into Orders --> 5 orders */

LOCK TABLES `Orders` WRITE;
INSERT INTO `Orders` VALUES
(1,'2020-11-12','08:30:00', 'prescription', 1, 4, 4),
(2,'2020-11-12','08:30:00', 'blood tests', 2, 2, 1),
(3,'2020-11-12','08:30:00', 'prescription', 3, 5, 5),
(4,'2020-11-12','08:30:00', 'x-ray', 4, 3, 3),
(5,'2020-11-12','08:30:00', 'vitals', 5, 1, 2);
UNLOCK TABLES;


/* Insert into Results --> 5 results */

LOCK TABLES `Results` WRITE;
INSERT INTO `Results` VALUES
(1,'fulfilled', 1, '2020-11-15', ''),
(2,'pending: patient visit', 2, '2020-11-15', ''),
(3,'pending: order received', 3, '2020-11-15', ''),
(4,'fulfilled', 4, '2020-11-15', ''),
(5,'fulfilled', 5, '2020-11-15', '');
UNLOCK TABLES;

/*Insert into Staff_Patients --> 5 relations*/

LOCK TABLES `Staff_Patients` WRITE;
INSERT INTO `Staff_Patients` VALUES
(4, 1), (1, 2), (5, 3), (3, 4), (2, 5);
UNLOCK TABLES;