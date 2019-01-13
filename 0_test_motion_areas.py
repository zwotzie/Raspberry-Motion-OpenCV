# https://imagemagick.org/Usage/draw/
# http://imagemagick.org/discourse-server/viewtopic.php?t=19591


import os
import glob
# import pandas as pd
import subprocess

# module level variables ##############################################################################################
# train and test directories
# ToDo refactor with input parameter
TEST_IMAGES_DIR = os.getcwd() + "/test_images/"
MOTION_TEST_DIR = os.getcwd() + "/test_images_motion_area/"

#######################################################################################################################
def main():

    # convert test xml data to a single .csv file
    print("draw yellow transparent box on motion area . . .")
    testCsvResults = path_to_testimages(TEST_IMAGES_DIR)
    print("done")

# end main


#######################################################################################################################
def path_to_testimages(path):
    attribute_list = []
    for file in glob.glob(path + '/*/*.jpg'):
        basepath, basename = os.path.split(file)
        basepath, classification = os.path.split(basepath)

        # https://motion-project.github.io/motion_config.html#conversion_specifiers
        # %w	width of the image
        # %h	height of the image
        # %i	width of motion area
        # %J	height of motion area
        # %K	X coordinates of motion center
        # %L	Y coordinates of motion center
        # expect filename like: 'Camera1_10-51-53.02.192.132.178.582.815.jpg' (%Y-%m-%d/%{dbeventid}/%H-%M-%S.%q.%{dbeventid}.%i.%J.%K.%L)
        # 10-59-20.02.231.1124.810.424.793.jpg
        # 0        1  2   3    4   5   6
        # => ,1600,1200,mouse,-138,231,986,1355
        splits = basename.split('.')

        # hour     = int(splits[0])
        # frame    = int(splits[1])
        # event_id = int(splits[2])

        area_width = int(splits[3])
        area_height = int(splits[4])
        center_x = int(splits[5])
        center_y = int(splits[6])

        xmin = int(center_x - area_width / 2)
        xmax = int(center_x + area_width / 2)

        ymin = int(center_y - area_height / 2)
        ymax = int(center_y + area_height / 2)

        file_output = os.path.join(MOTION_TEST_DIR, basename)
        cmd = 'convert %s -strokewidth 0 -fill "rgba( 255, 215, 0 , 0.3 )" -draw "rectangle %d,%d %d,%d " %s' % (file, xmin, ymin, xmax, ymax, file_output)

        subprocess.call(cmd, shell=True)

# end function

#######################################################################################################################
if __name__ == "__main__":
    main()