CREATE DATABASE motion;
CREATE USER 'motion'@'localhost' IDENTIFIED BY 'mypasswordformotion!';
GRANT ALL ON motion.* TO 'motion'@'localhost';
FLUSH PRIVILEDGES;

USE motion;

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
, creation_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
