CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `phone` int NOT NULL,
  `mail` varchar(45) NOT NULL,
  `is_paid` int NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `bookings` (
  `booking_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `date_of_hire` date NOT NULL,
  `date_of_ret` date NOT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `vehicles` (
  `vehicle_id` int NOT NULL,
  `category` varchar(45) NOT NULL,
  `hiring_price` int NOT NULL,
  `is_available` int NOT NULL,
  PRIMARY KEY (`vehicle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `vehicles`
(`vehicle_id`,
`category`,
`hiring_price`,
`is_available`)
VALUES
(1,
'small car carry up to 4',
100,
1);
INSERT INTO `vehicles`
(`vehicle_id`,
`category`,
`hiring_price`,
`is_available`)
VALUES
(3,
'van',
200,
1);
INSERT INTO `vehicles`
(`vehicle_id`,
`category`,
`hiring_price`,
`is_available`)
VALUES
(2,
'family car carry up to 7',
150,
1);