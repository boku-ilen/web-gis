from djgeojson.views import GeoJSONLayerView
from django.http import JsonResponse
from .models import ProjectDefinition, UserEntry
from django.views.generic import TemplateView


def get_entry_data():
    return GeoJSONLayerView.as_view(model=UserEntry, properties=('field_data'))


def create_entry(request, project_name):
    # get project via unique project_name
    # get EntryDefinition and field values with calls like request.POST['<field_name>']
    return JsonResponse({"success": False})


class ProjectView(TemplateView):
    template_name = "project.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)

        # TODO: Validate the project_name by getting the corresponding ProjectDefinition

        context['message'] = self.project_name
        return context

    @property
    def project_name(self):
       return self.kwargs['project_name']


class UserEntryView(TemplateView):
    template_name = "user_entry_form.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)

        context["project_definition"] = ProjectDefinition.objects.get(url=self.project_name)
        return context
    
    @property
    def project_name(self):
        return self.kwargs["project_name"]