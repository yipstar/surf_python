import numpy as np
import pandas as pd
import os
import datetime
import requests

from huey.models import Buoy, BuoyRealtimeWaveDetail, BuoyRawSpectralWaveData

def import_buoy_realtime_wave_detail(db_session):
    station_id = "46025"
    buoy = db_session.query(Buoy).filter(Buoy.station_id == station_id).first()
    latest_ob = db_session.query(BuoyRealtimeWaveDetail).filter(BuoyRealtimeWaveDetail.buoy_id == buoy.
id ).order_by(BuoyRealtimeWaveDetail.ts.desc()).first()

    realtime_url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.spec"
    df = pd.read_csv(realtime_url, delim_whitespace=True)
    df = df.replace('MM', np.NaN)

    # skip first row which is header
    for (index, row) in df[1:].iterrows():

        ob = BuoyRealtimeWaveDetail.from_pd_row(row)
        ob.buoy = buoy

        if (latest_ob is None or ob.ts > latest_ob.ts):
            print(f"inserting observation for date: {ob.ts}")
            db_session.add(ob)
        else:
            print(f"observation for date: {ob.ts} already present, skipping.")
            break

    db_session.commit()
    print("import complete")

def import_buoy_raw_spectral_wave_data(db_session):
    station_id = "46025"
    buoy = db_session.query(Buoy).filter(Buoy.station_id == station_id).first()
    latest_ob = db_session.query(BuoyRawSpectralWaveData).filter(BuoyRawSpectralWaveData.buoy_id == buoy.id ).order_by(BuoyRawSpectralWaveData.ts.desc()).first()

    raw_spec_url = f"https://www.ndbc.noaa.gov/data/realtime2/{station_id}.data_spec"
    response = requests.get(raw_spec_url)
    data = response.text

    # skip first row which is header
    for line in data.splitlines()[1:]:
    
        ob = BuoyRawSpectralWaveData.from_data_line(line)
        ob.buoy = buoy

        if (latest_ob is None or ob.ts > latest_ob.ts):
            print(f"inserting observation for date: {ob.ts}")
            db_session.add(ob)
        else:
            print(f"observation for date: {ob.ts} already present, skipping.")
            break

    db_session.commit()
    print("import complete")
