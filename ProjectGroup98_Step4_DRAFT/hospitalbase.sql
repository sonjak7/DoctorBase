/**/;

/* Database calls for Group 98 CS340 Fall 2020*/;

/* (a) Database Definition Queries */

/* Create a table for Doctors */

DROP TABLE IF EXISTS `doctors`;

CREATE TABLE `doctors` (
  `doctorid` int(11) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL,
  PRIMARY KEY (`doctorid`)
);

/* Create a table for staff */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staffid` int(11) NOT NULL AUTO_INCREMENT,
  `stafftype` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `primarydoctorid` int(11) NOT NULL,
  PRIMARY KEY (`staffid`)
);

/* Create a table for patients */

DROP TABLE IF EXISTS `patients`;

CREATE TABLE `patients` (
  `patientid` int(11) NOT NULL AUTO_INCREMENT,
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `primarydoctorid` int(11) NOT NULL,
  PRIMARY KEY (`patientid`),
  FOREIGN KEY (`primarydoctorid`) REFERENCES `doctors` (`doctorid`)
);


/* Create a table for orders */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `orderid` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `ordertype` varchar(255) NOT NULL,
  `patientid` int(11) NOT NULL,
  `doctorid` int(11) NOT NULL,
  `staffid` int(11) NOT NULL,
  PRIMARY KEY (`orderid`),
  FOREIGN KEY (`patientid`) REFERENCES `patients` (`patientid`),
  FOREIGN KEY (`doctorid`) REFERENCES `doctors` (`doctorid`),
  FOREIGN KEY (`staffid`) REFERENCES `staff` (`staffid`)
);

/* Create a table for results */

DROP TABLE IF EXISTS `results`;

CREATE TABLE `orders` (
  `resultid` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(255) NOT NULL,
  `orderid` int(11) NOT NULL,
  `date` date NOT NULL,
  `accessedbydoctor` bit(1) DEFAULT b'0',
  PRIMARY KEY (`resultid`),
  FOREIGN KEY (`orderid`) REFERENCES `orders` (`orderid`)
);

/* (b) Sample Data */

/* Insert into doctors --> 5 doctors */

LOCK TABLES `doctors` WRITE;
INSERT INTO `doctors` VALUES
(1,'Carson','Ben', 'Neurology'),
(2,'Mukherjee','Siddharth', 'Oncology'),
(3,'Gawande','Atul', 'Endocrinology'),
(4,'Sacks','Oliver', 'Neurology'),
(5,'of Kos','Hippocrates', 'Internal Medicine');
UNLOCK TABLES;

/* Insert into patients --> 5 patients */

LOCK TABLES `patients` WRITE;
INSERT INTO `patients` VALUES
(1,'Bechdel','Alison', 4),
(2,'McCraney','Tarell', 2),
(3,'Diaz','Junot', 5),
(4,'Patel','Shwetak', 3),
(5,'Duflo','Esther', 1);
UNLOCK TABLES;

/* Insert into staff --> 5 staff */

LOCK TABLES `staff` WRITE;
INSERT INTO `staff` VALUES
(1,'pathology', 'Pasteur','Louis'),
(2,'nursing','Nightingale','Florence'),
(3,'radiology', 'Damadian','Raymond'),
(4,'pharmacy', 'Dauerer','Maria'),
(5,'pharmacy', 'Pankiewicz','Tadeusz');
UNLOCK TABLES;

/* Insert into orders --> 5 orders */

LOCK TABLES `orders` WRITE;
INSERT INTO `orders` VALUES
(1,2020-11-12,08:30:00, 'prescription', 1, 4, 4),
(2,2020-11-12,08:30:00, 'blood tests', 2, 2, 1),
(3,2020-11-12,08:30:00, 'prescription', 3, 5, 5),
(4,2020-11-12,08:30:00, 'x-ray', 4, 3, 3),
(5,2020-11-12,08:30:00, 'vitals', 5, 1, 2);
UNLOCK TABLES;


/* Insert into results --> 5 results */

LOCK TABLES `results` WRITE;
INSERT INTO `results` VALUES
(1,'fulfilled', 1, 2020-11-15, ''),
(2,'pending: patient visit', 2, 2020-11-15, ''),
(3,'pending: order received', 3, 2020-11-15, ''),
(4,'fulfilled', 4, 2020-11-15, ''),
(5,'fulfilled', 5, 2020-11-15, '');
UNLOCK TABLES;