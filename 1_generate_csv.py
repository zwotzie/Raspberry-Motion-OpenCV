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
TRAIN_CSV_FILE_LOC = TRAINING_DATA_DIR + "/" + "train_labels.csv"
EVAL_CSV_FILE_LOC = TRAINING_DATA_DIR + "/" + "eval_labels.csv"

#######################################################################################################################
def main():

#    for path in glob.glob('/home/ralf/git/github.com/zwotzie/Raspberry-Motion-OpenCV/training_images/*'):
#        classifiction = path.split('/')[-1]

    # convert training xml data to a single .csv file
    print("converting xml training data . . .")
    trainCsvResults = path_to_csv(TRAINING_IMAGES_DIR)
    trainCsvResults.to_csv(TRAIN_CSV_FILE_LOC, index=None)
    print("training xml to .csv conversion successful, saved result to " + TRAIN_CSV_FILE_LOC)

    # convert test xml data to a single .csv file
    print("converting xml test data . . .")
    testCsvResults = path_to_csv(TEST_IMAGES_DIR)
    testCsvResults.to_csv(EVAL_CSV_FILE_LOC, index=None)
    print("test xml to .csv conversion successful, saved result to " + EVAL_CSV_FILE_LOC)

# end main


#######################################################################################################################
def path_to_csv(path):
    attribute_list = []
    for file in glob.glob(path + '/*.jpg'):
        basepath, basename = os.path.split(file)
        basepath, classification = os.path.split(basepath)

        # expect filename like: 'Camera1_10-51-53.02.192.132.178.582.815.jpg' (%Y-%m-%d/%{dbeventid}/%H-%M-%S.%q.%{dbeventid}.%i.%J.%K.%L)
        splits = basename.split('.')

        center_x = splits[5]
        center_y = splits[6]
        area_width = splits[3]
        area_height = splits[4]

        xmin = center_x - area_width / 2
        xmax = center_x + area_width / 2
        ymin = center_y - area_width / 2
        ymax = center_y + area_width / 2

        # fix setting...
        width = 1600
        height = 1200

        attribute_list.append((basename, width, height, classification, xmin, ymin, xmax, ymax))

        # end for

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    file_df = pd.DataFrame(attribute_list, columns=column_name)
    return file_df
# end function

#######################################################################################################################
if __name__ == "__main__":
    main()