/**/;

/* Database calls for Group 98 CS340 Fall 2020*/;

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