CREATE TABLE `siteuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(45) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `is_operator` tinyint(4) DEFAULT NULL,
  `is_teamlead` tinyint(4) DEFAULT NULL,
  `is_controller` tinyint(4) DEFAULT NULL,
  `is_admin` tinyint(4) DEFAULT NULL,
  `phone_teamleader` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;