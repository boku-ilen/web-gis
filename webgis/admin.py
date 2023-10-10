from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as webgis_models


admin.site.register(webgis_models.UserEntry, LeafletGeoAdmin)
admin.site.register(webgis_models.EntryDefinition, LeafletGeoAdmin)
admin.site.register(webgis_models.ProjectDefinition, LeafletGeoAdmin)
admin.site.register(webgis_models.LocationEntry, LeafletGeoAdmin)