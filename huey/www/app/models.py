from flask_appbuilder import Model
# from flask_appbuilder.models.mixins import AuditMixin

from sqlalchemy import Column, Integer, String, ForeignKey, \
    Float, DateTime, UniqueConstraint

from sqlalchemy.orm import relationship

from geoalchemy2.types import Geometry

import datetime

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



# class BuoyRealtimeWaveSpectralRaw
