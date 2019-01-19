from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go

# on mac...
# env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install mysqlclient

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta



app = Flask(__name__)
stmt = """SELECT * FROM motion_events 
WHERE start_time > date_sub(now(), interval 14 day) 
  AND ( classification in ('minz', 'dottie') 
       or 
      (changed_pixels_median > 20000 AND number_of_images > 20)
)"""

stmt = """SELECT 
  start_time
, round(TIMESTAMPDIFF(SECOND, start_time, end_time)/60, 1) as minutes
, changed_pixels_median
, CASE 
  WHEN classification in ('minz', 'dottie', 'mouse') THEN classification
  WHEN changed_pixels_median > 20000 THEN 'oCat'
  ELSE classification
  END AS classification
  FROM motion_events 
WHERE start_time > date_sub(now(), interval %d day) 
  AND number_of_images > 20
"""

MYSQL_HOST = os.getenv('MYSQL_HOST', 'catcam.fritz.box')
db = create_engine('mysql://motion:mypasswordformotion!@' + MYSQL_HOST + '/motion')
metadata = MetaData(db)

# debug mode in ipython, otherwise False!
# db.echo = True

motion_events = Table('motion_events', metadata, autoload=True)


@app.route('/cat/<int:days>')
def index(days=2):
    feature = 'Bar'
    # bar = create_plot(feature)
    graphJSONCats, graphJSONothers = catcam(days)
    return render_template('index.html', plotCats=graphJSONCats, plotOthers=graphJSONothers)


def catcam(days):
    df = pd.read_sql_query(stmt % days, db)
    x_to = datetime.now()
    x_from = x_to - timedelta(days=days)

    data_cats = []
    data_others = []
    for classification in df['classification'].unique():
        dfp = df[df['classification'] == classification]
        part = go.Bar(
            x=dfp['start_time'],
            y=dfp['minutes'],
            name=classification,
        )
        if classification in ['dottie', 'minz', 'oCat']:
            data_cats.append(part)
        else:
            data_others.append(part)

        layoutCats = dict(
            title="Minz, Dottie, andere Katze(?) (%d Tage)" % days,
            xaxis=dict(
                range=[x_from, x_to])
        )
        layoutOthers = dict(
            title="Maus und unbekannte Events (%d Tage)" % days,
            xaxis=dict(
                range=[x_from, x_to])
        )

        figCats = dict(data=data_cats, layout=layoutCats)
        figOthers = dict(data=data_others, layout=layoutOthers)

        graphJSONCats = json.dumps(figCats, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSONothers = json.dumps(figOthers, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSONCats, graphJSONothers

if __name__ == '__main__':
    app.run()