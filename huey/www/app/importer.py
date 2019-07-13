import numpy as np
import pandas as pd
import os
import datetime

from app import db
from app.models import Buoy, BuoyRealtimeWaveDetail

def import_buoy_realtime_wave_detail():
    station_id = "46025"
    buoy = db.session.query(Buoy).filter(Buoy.station_id == station_id).first()

    realtime_url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.spec"
    df = pd.read_csv(realtime_url, delim_whitespace=True)
    df = df.replace('MM', np.NaN)

    latest_ob = db.session.query(BuoyRealtimeWaveDetail).filter(BuoyRealtimeWaveDetail.buoy_id == buoy.id ).order_by(BuoyRealtimeWaveDetail.ts.desc()).first()

    obs = []

    # skip first row which is header
    for (index, row) in df[1:].iterrows():

        # check row is not already in the system, if so stop
        ts = datetime.datetime(int(row['#YY']), int(row['MM']), int(row['DD']), int(row['hh']), int(row['mm']), tzinfo=datetime.timezone.utc)

        if latest_ob.ts == ts:
            print(f"observation for date: {ts} already present, saving and then halting import.")

            for ob in obs:
                db.session.add(ob)
            db.session.commit()

            return

        print(f"inserting observation for date: {ts}")

        #print(row['#YY'])
        ob = BuoyRealtimeWaveDetail()
        ob.buoy = buoy
        ts = datetime.datetime(int(row['#YY']), int(row['MM']), int(row['DD']), int(row['hh']), int(row['mm']), tzinfo=datetime.timezone.utc)
        ob.ts = ts
        ob.significant_wave_height = float(row['WVHT'])
        ob.swell_height = float(row['SwH'])
        ob.swell_period = float(row['SwP'])
        ob.swell_direction = row['SwD']
        ob.wind_wave_height = float(row['WWH'])
        ob.wind_wave_period = float(row['WWP'])
        ob.steepness = row['STEEPNESS']
        ob.dominant_wave_direction = int(row['MWD'])
        obs.append(ob)

    for ob in obs:
        db.session.add(ob)
    db.session.commit()
    
    print("import complete")
