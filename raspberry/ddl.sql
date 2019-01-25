CREATE DATABASE motion;
CREATE USER 'motion'@'localhost' IDENTIFIED BY 'mypasswordformotion!';
GRANT ALL ON motion.* TO 'motion'@'localhost';
FLUSH PRIVILEGES;

USE motion;
--  ToDo most int's could be mediumint unsigned
CREATE TABLE images (
  id int not null primary key auto_increment
, event_id int
, filename varchar(255) not null
, frame_number int
, file_type int
, image_width int
, image_height int
, motion_center_x int
, motion_center_y int
, changed_pixels int
, noise_level int
, motion_area_height int
, motion_area_width int
, threshold int
, camera int
, classification enum('minz', 'dottie', 'mouse', 'unknown')
, score tinyint
, creation_time timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE motion_events (
  event_id int primary key auto_increment
, camera tinyint
, start_time timestamp DEFAULT CURRENT_TIMESTAMP
, end_time timestamp NULL DEFAULT NULL
, number_of_images mediumint unsigned
, changed_pixels_median mediumint unsigned
, classification varchar(255)
);

ALTER TABLE motion_events AUTO_INCREMENT=27;

-- shell commands for timezone support: https://mariadb.com/kb/en/library/mysql_tzinfo_to_sql/
mysql_tzinfo_to_sql  /usr/share/zoneinfo/Europe/Berlin 'Europe/Berlin' | mysql -u root mysql
mysql_tzinfo_to_sql  /usr/share/zoneinfo/UTC 'UTC' | mysql -u root mysql

