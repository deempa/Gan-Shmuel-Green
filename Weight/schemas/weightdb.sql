--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--
CREATE TABLE IF NOT EXISTS `container_in_transaction` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `container_id` varchar(50) DEFAULT NULL,
  `transaction_id_in` varchar(50) DEFAULT NULL,
  `transaction_id_out` varchar(50) DEFAULT NULL,
  `transaction_id_none` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`container_id`) REFERENCES `containers_registered` (`container_id`),
  FOREIGN KEY (`transaction_id_in`) REFERENCES `transactions` (`id`),
  FOREIGN KEY (`transaction_id_out`) REFERENCES `transactions` (`id`),
  FOREIGN KEY (`transaction_id_none`) REFERENCES `transactions` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001;


CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  -- `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
