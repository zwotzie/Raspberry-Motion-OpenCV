#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
import pandas as pd
import numpy as np
from sys import argv, exit
import os
import cv2
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

NUM_CLASSES = 3
BASEPATH="/home/pi/Raspberry-Motion-OpenCV"
FROZEN_INFERENCE_GRAPH_LOC = BASEPATH + "/exported_model/frozen_inference_graph.pb"
LABELS_LOC = BASEPATH + "/training_data/" + "label_map.pbtxt"

db = create_engine('mysql://motion:mypasswordformotion!@localhost/motion')
metadata = MetaData(db)

# debug mode in ipython, otherwise False!
# db.echo = True

images = Table('images', metadata, autoload=True)
motion_events = Table('motion_events', metadata, autoload=True)

# filter all rows where column x is None/null
# print(df.loc[df['changed_pixels_median'].isnull()])

query_median = """
SELECT round(AVG(dd.changed_pixels), 0) as changed_pixels_median
FROM (
SELECT d.changed_pixels, @rownum:=@rownum+1 as row_number, @total_rows:=@rownum
  FROM images d, (SELECT @rownum:=0) r
  WHERE d.changed_pixels is NOT NULL
  and event_id = %d
  ORDER BY d.changed_pixels
) as dd
WHERE dd.row_number IN ( FLOOR((@total_rows+1)/2), FLOOR((@total_rows+2)/2) )
"""

# query_filenames = "SELECT filename FROM images WHERE event_id = %d"

def set_motion_evens_values(event_id):

    query = 'SELECT * FROM images WHERE event_id = %d' % event_id
    df = pd.read_sql_query(query, db)
    df['class'] = None
    df['score'] = 0
    number_of_images = df.shape[0]
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
        # index starts with 10 so
        df.drop(df.index[:41], inplace=True)


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

                objects = []
                threshold = 0.5  # in order to get higher percentages you need to lower this number; usually at 0.01 you get 100% predicted objects
                for index, value in enumerate(classes[0]):
                    object_dict = {}
                    if scores[0, index] > threshold:
                        object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                            scores[0, index]
                        objects.append(object_dict)
                # objects: [{b'mouse': 0.971244}]

                # we assume there is only one object found:
                try:
                    classification = list(objects[0].keys())[0].decode("utf-8")
                    score = round(objects[0][classification], 2) * 100
                except IndexError:
                    classification = None
                    score = 0
                # print("%s : %s : %s %" % (image_path, classification, score))

                idx = df[df['filename'] == image_path].index.values.astype(int)[0]
                df.loc[idx, 'score'] = score
                df.loc[idx, 'class'] = classification

    # pdSeries = df.groupby('class')['score'].mean()
    # df2 = pd.DataFrame({'class': pdSeries.index, 'score': pdSeries.values})
    grouped = df.groupby('class').sum()
    most_valueable_class = grouped.score.idxmax()

    classification = most_valueable_class

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
            set_motion_evens_values(event_id)

    elif argv[1]:
        event_id = get_int(argv[1])
        set_motion_evens_values(event_id)


if __name__ == '__main__':
    main()

