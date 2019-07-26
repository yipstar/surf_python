import datetime

from flask_appbuilder import Model
# from flask_appbuilder.models.mixins import AuditMixin

from sqlalchemy import Column, Integer, String, ForeignKey, \
    Float, DateTime, UniqueConstraint

from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from geoalchemy2.types import Geometry

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class Buoy(Model):
    id = Column(Integer, primary_key=True)
    station_id =  Column(String(150), unique = True, nullable=False)
    name = Column(String(564))
    owner = Column(String(564))
    pgm = Column(String(564))
    station_type = Column(String(150))
    lat = Column(Float())
    lng = Column(Float())
    point = Column(Geometry(geometry_type='POINT', srid=4326))

    elevation = Column(Float())
    hull = Column(String(100))
    anemom_height = Column(Float())

    def __repr__(self):
        return f"{self.station_id} - {self.name}"

#YY  MM DD hh mm WVHT  SwH  SwP  WWH  WWP SwD WWD  STEEPNESS  APD MWD
#yr  mo dy hr mn    m    m  sec    m  sec  -  degT     -      sec degT
#2019 06 26 11 40  0.7  0.7 13.8  0.2  2.9 SSW WSW        N/A  7.7 201
# https://www.ndbc.noaa.gov/measdes.shtml#stdmet

class BuoyRealtimeWaveDetail(Model):
    id = Column(Integer, primary_key=True)
    buoy_id = Column(Integer, ForeignKey('buoy.id'), nullable=False)
    buoy = relationship("Buoy")
    ts = Column(DateTime(timezone=True), nullable=False)
    significant_wave_height = Column(Float())
    swell_height = Column(Float())
    swell_period = Column(Float())
    swell_direction = Column(String(10))
    wind_wave_height = Column(Float())
    wind_wave_period = Column(Float())
    steepness = Column(String(50))
    average_wave_period = Column(Float())
    dominant_wave_direction = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint('buoy_id', 'ts', name='unique_buoy_ts'),
    )

    def __repr__(self):
        return f"{self.buoy_id} - {ts}"

    @classmethod
    def from_pd_row(cls, row):
        ob = cls()
        ts = cls.ts_from_pd_row(row)
        # ts = datetime.datetime(int(row['#YY']), int(row['MM']), int(row['DD']), int(row['hh']), int(row['mm']), tzinfo=datetime.timezone.utc)
        ob.ts = ts
        ob.significant_wave_height = float(row['WVHT'])
        ob.swell_height = float(row['SwH'])
        ob.swell_period = float(row['SwP'])
        ob.swell_direction = row['SwD']
        ob.wind_wave_height = float(row['WWH'])
        ob.wind_wave_period = float(row['WWP'])
        ob.steepness = row['STEEPNESS']
        ob.dominant_wave_direction = int(row['MWD'])

        return ob

    @classmethod
    def ts_from_pd_row(cls, row):
        return datetime.datetime(int(row['#YY']), int(row['MM']), int(row['DD']), int(row['hh']), int(row['mm']), tzinfo=datetime.timezone.utc)

class RawSpectralWaveData(Model):
    id = Column(Integer, primary_key=True)
    buoy_id = Column(Integer, ForeignKey('buoy.id'), nullable=False)
    buoy = relationship("Buoy")
    ts = Column(DateTime(timezone=True), nullable=False)
    sep_freq = Column(Float())
    spec_x = Column(postgresql.ARRAY(Float), default='{}')
    spec_y = Column(postgresql.ARRAY(Float), default='{}')
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint('buoy_id', 'ts', name='unique_buoy_raw_spectral_wave_data_ts'),
    )

    @classmethod
    def from_data_line(cls, line):
        columns = line.split()

        ob = cls()
        ob.ts = datetime.datetime(int(columns[0]), int(columns[1]), int(columns[2]), int(columns[3]), int(columns[4]), tzinfo=datetime.timezone.utc)
        ob.sep_freq = columns[5]

        x, y = [], []
        count = 0
        for val in columns[6:]:
            if (count % 2 == 0):
                x.append(float(val))
            else:
                val = val.replace('(', '')
                val = val.replace(')', '')
                y.append(float(val))

            count += 1

        ob.spec_x = x
        ob.spec_y = y

        return ob


