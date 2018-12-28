#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
import pandas as pd
from sys import argv, exit

db = create_engine('mysql://motion:mypasswordformotion!@localhost/motion')
metadata = MetaData(db)

# debug mode in ipython, otherwise False!
# db.echo = True

images = Table('images', metadata, autoload=True)
motion_events = Table('motion_events', metadata, autoload=True)

# filter all rows where column x is None/null
# print(df.loc[df['changed_pixels_median'].isnull()])

query="SELECT count(*) as number_of_images, min(creation_time) as start_time, max(creation_time) as end_time FROM images where event_id = %d"
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

def set_motion_evens_values(event_id):
    connection = db.connect()
    result = connection.execute(query % event_id)
    for row in result:
        number_of_images, start_time, end_time = row

    result = connection.execute(query_median % event_id)
    for row in result:
        changed_pixels_median, = row

    classification = None
    if changed_pixels_median < 10000:
        classification='mouse'

    print event_id, number_of_images, start_time, end_time, changed_pixels_median, classification

    motion_events.update(motion_events.c.event_id == event_id).execute(
        changed_pixels_median=changed_pixels_median
    #    , start_time=start_time
        , end_time=end_time
        , number_of_images=number_of_images
        , classification=classification)

def get_int(s):
        return int(s)

if len(argv) != 2:
    print "Usage: on_event_end.py ['all', <event_id>]"
    exit(1)
elif argv[1] == 'all':
    df = pd.read_sql_query('SELECT * FROM motion_events', db)
    for event_id in df['event_id']:
        set_motion_evens_values(event_id)
elif argv[1]:
    event_id = get_int(argv[1])
    set_motion_evens_values(event_id)



