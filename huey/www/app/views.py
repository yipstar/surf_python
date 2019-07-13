from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
# from flask_appbuilder import ModelRestApi

from flask_appbuilder import AppBuilder, expose, BaseView, has_access
from app import appbuilder, db

# from . import appbuilder, db

from .models import Buoy, BuoyRealtimeWaveDetail

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

class BuoyRealtimeWaveDetailModelView(ModelView):
    datamodel = SQLAInterface(BuoyRealtimeWaveDetail)

    label_columns = {'buoy': 'Buoy'}
    list_columns = ['buoy',
                    'ts',
                    'significant_wave_height',
                    'swell_height',
                    'swell_period',
                    'swell_direction',
                    'wind_wave_height',
                    'wind_wave_period',
                    'steepness',
                    'average_wave_period',
                    'dominant_wave_direction',
                    'created_at',
                    'updated_at']


    # show_exclude_columns = ['point']
    # add_exclude_columns = ['point']
    # edit_exclude_columns = ['point']

    # show_fieldsets = [
    #     (
    #         'Summary,
                    #         {'fields': ['name', 'address', 'contact_group']}
    #     ),
    #     (
    #         'Personal Info',
    #         {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
    #     ),
    # ]

class BuoyModelView(ModelView):
    datamodel = SQLAInterface(Buoy)
    related_views = [BuoyRealtimeWaveDetailModelView]
    list_columns = ['station_id', 'name', "owner", "pgm", "station_type", "lat", "lng"]
    show_exclude_columns = ['point']
    add_exclude_columns = ['point']
    edit_exclude_columns = ['point']
    search_exclude_columns = ['point']

appbuilder.add_view(
    BuoyModelView,
    "List Buoys",
    icon = "fa-folder-open-o",
    category = "Buoys",
    category_icon = "fa-envelope"
)

appbuilder.add_view(
    BuoyRealtimeWaveDetailModelView,
    "List Realtime Wave Detail Data",
    icon = "fa-envelope",
    category = "Buoys"
)

"""
    Application wide 404 error handler
"""

class MyView(BaseView):
    # route_base = "/myview"
    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return it
        return 'Hello'

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render it
        param1 = 'Goodbye %s' % (param1)
        return param1

# appbuilder.add_view_no_menu(MyView())
appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


# db.create_all()
# db.update_all()
