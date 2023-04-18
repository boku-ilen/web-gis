from djgeojson.views import GeoJSONLayerView
from django.http import JsonResponse
from .models import UserEntry
from django.views.generic import TemplateView


def get_entry_data():
    return GeoJSONLayerView.as_view(model=UserEntry, properties=('field_data'))


def create_entry(request, project_name):
    # get project via unique project_name
    # get EntryDefinition and field values with calls like request.POST['<field_name>']
    return JsonResponse({"success": False})


class ProjectView(TemplateView):
    template_name = "index.html"