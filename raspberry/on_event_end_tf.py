#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
import pandas as pd
import numpy as np
from sys import argv, exit
import cv2
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import os


NUM_CLASSES = 3
BASEPATH = os.getenv('BASEPATH', "/home/pi/Raspberry-Motion-OpenCV")
IMAGE_PATH_ORG = os.getenv('IMAGE_PATH_ORG')
IMAGE_PATH_REPLACE = os.getenv('IMAGE_PATH_REPLACE')
FROZEN_INFERENCE_GRAPH_LOC = BASEPATH + "/exported_model/frozen_inference_graph.pb"
LABELS_LOC = BASEPATH + "/training_data/" + "label_map.pbtxt"

MYSQL_HOST = os.getenv('MYSQL_HOST', 'catcam.fritz.box')
db = create_engine('mysql://motion:mypasswordformotion!@' + MYSQL_HOST + '/motion')
metadata = MetaData(db)

# debug mode in ipython, otherwise False!
db.echo = True

images = Table('images', metadata, autoload=True)
motion_events = Table('motion_events', metadata, autoload=True)

# filter all rows where column x is None/null
# print(df.loc[df['changed_pixels_median'].isnull()])


def set_motion_events_values(event_id):
    start_time = None
    end_time = None
    changed_pixels_median = None
    classification = None

    query = 'SELECT * FROM images WHERE event_id = %d' % event_id
    df = pd.read_sql_query(query, db)
    df['class'] = None
    df['score'] = 0
    number_of_images = df.shape[0]
    if number_of_images > 0:
        start_time = min(df['creation_time'])
        end_time = max(df['creation_time'])
        changed_pixels_median = df['changed_pixels'].median().astype(int)

        # some optimizations:
        if number_of_images > 50:
            # remove first and last rows
            df.drop(df.head(10).index, inplace=True)
            df.drop(df.tail(10).index, inplace=True)

            # randomize shuffel the dataframe rows
            df = df.apply(np.random.permutation)

            # 32 images to analyse should be enough
            df.drop(df.index[32:], inplace=True)
        if IMAGE_PATH_REPLACE:
            df.replace({'filename': r'^'+IMAGE_PATH_ORG}, {'filename': IMAGE_PATH_REPLACE}, regex=True, inplace=True)

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(FROZEN_INFERENCE_GRAPH_LOC, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(LABELS_LOC)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                for image_path in df['filename']:
                    # /home/pi/motioneye/pics/2019-05-19/4177/15-29-47.03.4177.764.1198.290.599.jpg

                    image_np = cv2.imread(image_path)

                    # Definite input and output Tensors for detection_graph
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    # Actual detection.
                    (boxes, scores, classes, num) = sess.run(
                        [detection_boxes, detection_scores, detection_classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})

                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8,
                        min_score_thresh=0.20)

                    # overwrite the image with tensorflow information
                    image_path_new = image_path.replace('pics', 'pics_classified')
                    image_dir = os.path.dirname(os.path.realpath(image_path_new))
                    if not os.path.isdir(image_dir):
                        os.makedirs(image_dir)
                    cv2.imwrite(image_path_new, image_np)

                    objects = []
                    threshold = 0.2  # in order to get higher percentages you need to lower this number; usually at 0.01 you get 100% predicted objects
                    for index, value in enumerate(classes[0]):
                        object_dict = {}
                        if scores[0, index] > threshold:
                            object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                                scores[0, index]
                            objects.append(object_dict)
                    # objects: [{b'mouse': 0.971244}]

                    # we assume there is only one object found:
                    try:
                        classification = list(objects[0].keys())[0]
                        score = round(objects[0][classification] * 100)
                        classification = classification.decode("utf-8")
                    except IndexError:
                        classification = None
                        score = 0
                    # print("%s : %s : %r" % (image_path, classification, score))

                    idx = df[df['filename'] == image_path].index.values.astype(int)[0]
                    df.loc[idx, 'score'] = score
                    df.loc[idx, 'class'] = classification

                    # update the images metadata with classification and score
                    images.update(images.c.id == df.loc[idx, 'id']).execute(
                        classification=classification
                        , score=score
                    )

                    image_np = None
                    image_np_expanded = None

        # pdSeries = df.groupby('class')['score'].mean()
        # df2 = pd.DataFrame({'class': pdSeries.index, 'score': pdSeries.values})
        try:
            grouped = df.groupby('class').sum()
            most_valueable_class = grouped.score.idxmax()

            classification = most_valueable_class
        except ValueError: #attempt to get argmax of an empty sequence
            classification = 'unknown'


    print(event_id, number_of_images, start_time, end_time, changed_pixels_median, classification)

    motion_events.update(motion_events.c.event_id == event_id).execute(
        changed_pixels_median=changed_pixels_median
    #    , start_time=start_time
        , end_time=end_time
        , number_of_images=number_of_images
        , classification=classification)


def get_int(s):
        return int(s)


def main():
    if len(argv) != 2:
        print("Usage: on_event_end.py ['all', <event_id>]")
        exit(1)

    elif argv[1] == 'all':
        df = pd.read_sql_query('SELECT * FROM motion_events', db)
        for event_id in df['event_id']:
            set_motion_events_values(event_id)

    elif argv[1]:
        event_id = get_int(argv[1])
        set_motion_events_values(event_id)


if __name__ == '__main__':
    main()

