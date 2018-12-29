# Welcome to My New Project
The purpose of this project is to analyze the eating habits of our cats.


## Status of the Project
Right now, I'm fine-tuning motion. Motion is responsible for taking 
pictures when something moves in the camera. In reality, I do this in 
MotionEye because it's easier and there's a GUI where I can see.


## Hardware
- Raspberry Pi 3B+
- NightVision Camera
- PIR (not jet in use)

### The Camera:
https://www.ebay.de/itm/183394240431
1. The Raspberry Pi Camera Board Features a 5MP (2592×1944 pixels)
1. Half Size would be 1296x972, or normal mode 1600x1200
1. Omnivision 5647 sensor in a fixed focus module
1. The camera is capable of 2592 x 1944 pixel static images, and also supports 1080 p @ 30 fps, 720 p @ 60 fps and 640 x480 p 60/90 video recording
1. Video: Supports 1080 p @ 30 fps, 720 p @ 60 fps and 640 x480 p 60/90 Recording 7.15-pin MIPI Camera Serial Interface
The CSI bus is capable of extremely high data rates, and it exclusively carries pixel data to the BCM2835 processor


## Some Links For Your Start:
- https://www.modmypi.com/blog/installing-the-raspberry-pi-camera-board
- https://medium.com/@samdownie/epilepsy-me-building-my-own-sleep-lab-dd3775b8a1db
- https://www.bouvet.no/bouvet-deler/utbrudd/building-a-motion-activated-security-camera-with-the-raspberry-pi-zero
- https://www.thingiverse.com/thing:3043649
- https://klenzel.de/1857 (PIR)
- http://www.richardmudhar.com/blog/2015/02/raspberry-pi-camera-and-motion-out-of-the-box-sparrowcam/
- https://asciich.ch/wordpress/raspbian-auf-raspberrypi-ohne-bildschirm-und-tastatur-installieren/
- https://cdn-reichelt.de/documents/datenblatt/C100/10120262.pdf
- https://www.ebay.de/itm/Infrared-Night-Vision-Camera-Module-Board-IR-5MP-For-Raspberry-Pi-2-3-zero/183394240431
- https://motion-project.github.io/motion_config.html
- https://github.com/Motion-Project/motion/releases
- https://github.com/ccrisan/motioneye/wiki/Install-On-Raspbian
- https://github.com/ccrisan/motioneyeos/tree/master/board/raspberrypi3


## First Commands on The Pi
```
sudo su -

# update every installed package and fix if something is broken
apt update
apt upgrade
dpkg --configure -a
apt --fix-broken install
apt upgrade

cd /boot
cp config.txt config.txt.bak
vi config.txt
reboot

# install motionEye and some dependencies
apt install vim ffmpeg v4l-utils libjpeg-dev libssl-dev libcurl4-openssl-dev python-dev nginx
pip install pycurl pytz motioneye sqlalchemy
apt install python-pandas python-mysqldb ipython

mkdir /etc/motioneye
cp /usr/local/share/motioneye/extra/motioneye.conf.sample /etc/motioneye/motioneye.conf
vi /etc/motioneye/motioneye.conf 
mkdir /var/lib/motioneye
cp /usr/local/share/motioneye/extra/motioneye.systemd-unit-local /etc/systemd/system/motioneye.service

# make the cam working:
modprobe bcm2835-v4l2
ls /dev/video0 
vi /etc/modules

# install actual package of motion
wget https://github.com/Motion-Project/motion/releases/download/release-4.2.1/stretch_motion_4.2.1-1_amd64.deb
apt install libmicrohttpd12
dpkg -i ./pi_stretch_motion_4.2.1-1_armhf.deb

systemctl daemon-reload
systemctl enable motioneye
systemctl start motioneye
```


## Motion Mysql Setup

- https://motion-project.github.io/motion_config.html#OptDetail_Database
- https://motion-project.github.io/motion_config.html#conversion_specifiers

### Some DDL to Setup
see file ddl.sql

### MotionEye's "Extra Motion Options" (Additional Configuration For Motion)
```
database_type mysql
database_dbname motion
database_host localhost
database_port 3306
database_user motion
database_password mypasswordformotion

sql_log_picture on

# sql_query_start insert into motion_events(camera) values('%t')
sql_query_start insert into motion_events(camera, start_time) values ('%t', '%Y-%m-%d %T')
sql_query_stop update motion_events set end_time='%Y-%m-%d %T' where event_id=%{dbeventid}
sql_query insert into images (camera, event_id, filename, frame_number, file_type, image_width, image_height, motion_center_x, motion_center_y, changed_pixels, noise_level, motion_area_height, motion_area_width, threshold) values('%t', %{dbeventid}, '%f', %q, %n, %w, %h, %K, %L, %D, %N, %J, %i, %o)
```

First thing what I'm mention is, that the *sql_query_top* is not working.

I filed a bug to: https://github.com/Motion-Project/motion/issues/879

## Entering Debug Loging for Motion and MotionEye
sometimes you need more logging information and this will help:
```
vi /etc/motioneye/motioneye.conf
# set log_level:
log_level debug
```

## Next Steps ML/CV
Not jet implemented!
- https://www.learnopencv.com
- https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/
- https://github.com/tensorflow/tensorflow
- http://www.opencv.org/
- http://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
