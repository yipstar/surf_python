from flask_appbuilder import Model

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

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
