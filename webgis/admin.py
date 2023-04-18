from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as webgis_models


admin.site.register(webgis_models.UserEntry, LeafletGeoAdmin)
