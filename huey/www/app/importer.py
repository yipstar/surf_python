import numpy as np
import pandas as pd
import os
import datetime
import requests

from app import db
from app.models import Buoy, BuoyRealtimeWaveDetail, RawSpectralWaveData

# class BuoyDataExistsException(BaseException):
#     pass

def import_buoy_realtime_wave_detail():
    station_id = "46025"
    buoy = db.session.query(Buoy).filter(Buoy.station_id == station_id).first()

    realtime_url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.spec"
    df = pd.read_csv(realtime_url, delim_whitespace=True)
    df = df.replace('MM', np.NaN)

    latest_ob = db.session.query(BuoyRealtimeWaveDetail).filter(BuoyRealtimeWaveDetail.buoy_id == buoy.id ).order_by(BuoyRealtimeWaveDetail.ts.desc()).first()

    # skip first row which is header
    for (index, row) in df[1:].iterrows():

        ob = BuoyRealtimeWaveDetail.from_pd_row(row)
        ob.buoy = buoy

        if ob.ts > latest_ob.ts:
            print(f"inserting observation for date: {ob.ts}")
            db.session.add(ob)
        else:
            print(f"observation for date: {ob.ts} already present, skipping.")
            break

    db.session.commit()
    print("import complete")

def import_raw_spectral_wave_data():
    station_id = "46025"
    buoy = db.session.query(Buoy).filter(Buoy.station_id == station_id).first()

    url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.data_spec"

    latest_ob = db.session.query(BuoyRealtimeWaveDetail).filter(RawSpectralWaveData.buoy_id == buoy.id ).order_by(RawSpectralWaveData.ts.desc()).first()

    obs = []

    response = requests.get(url)
    data = response.text

    for line in data.splitlines()[1:]:
    
        columns = line.split()

        #print(line)
        #print("break")
        print(columns)
        #print("break")
        sep_freq = columns[5]

        ts = datetime.datetime(int(columns[0]), int(columns[1]), int(columns[2]), int(columns[3]), int(columns[4]), tzinfo=datetime.timezone.utc)

        if latest_ob and latest_ob.ts == ts:
            print(f"observation for date: {ts} already present, saving and then halting import.")

            for ob in obs:
                db.session.add(ob)
            db.session.commit()

            return

        x, y = [], []

        count = 0
        for val in columns[6:]:

            if (count % 2 == 0):
                #print("x")
                #print(val)
                x.append(float(val))
            else:
                #print("y")
                val = val.replace('(', '')
                val = val.replace(')', '')
                #print(val)
                y.append(float(val))

            count += 1

        #print(x)
        #print(y)

        print(f"inserting observation for date: {ts}")

        #print(row['#YY'])
        ob = RawSpectralWaveData()
        ob.buoy = buoy
        ob.ts = ts
        ob.sep_freq = sep_freq
        ob.spec_x = x
        ob.spec_y = y

        obs.append(ob)

    for ob in obs:
        db.session.add(ob)
    db.session.commit()
    
    print("import complete")
