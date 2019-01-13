import os
import glob
import pandas as pd


# module level variables ##############################################################################################
# train and test directories
TRAINING_IMAGES_DIR = os.getcwd() + "/training_images/"
TEST_IMAGES_DIR = os.getcwd() + "/test_images/"

MIN_NUM_IMAGES_REQUIRED_FOR_TRAINING = 10
MIN_NUM_IMAGES_SUGGESTED_FOR_TRAINING = 100

MIN_NUM_IMAGES_REQUIRED_FOR_TESTING = 3

# output .csv file names/locations
TRAINING_DATA_DIR = os.getcwd() + "/" + "training_data"
TRAIN_CSV_FILE = "train_labels-%s.csv"
EVAL_CSV_FILE = "eval_labels-%s.csv"

#######################################################################################################################
def main():

#    for path in glob.glob('/home/ralf/git/github.com/zwotzie/Raspberry-Motion-OpenCV/training_images/*'):
#        classifiction = path.split('/')[-1]

    # convert training xml data to a single .csv file
    print("converting xml training data . . .")
    path_to_csv(TRAINING_IMAGES_DIR, TRAIN_CSV_FILE)
    print("training xml to .csv conversion successful, saved result to " + TRAINING_DATA_DIR)

    # convert test xml data to a single .csv file
    print("converting xml test data . . .")
    path_to_csv(TEST_IMAGES_DIR, EVAL_CSV_FILE)
    print("test xml to .csv conversion successful, saved result to " + TRAINING_DATA_DIR)

# end main


#######################################################################################################################
def path_to_csv(path, to_csv_pattern):
    column_name = ['classification', 'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
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

        # motion sometimes produces negative values:
        if xmin < 0:
            xmin = 0

        if xmax < 0:
            xmax = 0

        if ymin < 0:
            ymin = 0

        if ymax < 0:
            ymax = 0

        # fix setting...
        width = 1600
        height = 1200

        attribute_list.append((classification, classification+'/'+basename, width, height, classification, xmin, ymin, xmax, ymax))

        # end for

    pre_file_df = pd.DataFrame(attribute_list, columns=column_name)

    for classification in pre_file_df.classification.unique():
        print("CLASS=%s" % classification)
        file_df = pre_file_df.loc[pre_file_df['classification'] == classification]
        file_df = file_df.drop(['classification'], axis=1)
        csv_filename = to_csv_pattern % classification
        csv_filename = os.path.join(TRAINING_DATA_DIR, csv_filename)
        file_df.to_csv(csv_filename, index=None)

# end function

#######################################################################################################################
if __name__ == "__main__":
    main()