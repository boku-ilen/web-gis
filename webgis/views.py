from django.core import serializers
from djgeojson.views import GeoJSONLayerView
from django.http import JsonResponse
from .models import ProjectDefinition, UserEntry
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def get_entry_data():
    return GeoJSONLayerView.as_view(model=UserEntry, properties=('field_data'))


def create_entry(request, project_url):
    # get project via unique project_url
    # get EntryDefinition and field values with calls like request.POST['<field_name>']
    return JsonResponse({"success": False})


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)
        
        context['projects'] = ProjectDefinition.objects.all()

        return context



class ProjectView(TemplateView):
    template_name = "project.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)

        try:
            project = ProjectDefinition.objects.get(url=self.project_url)
        except ObjectDoesNotExist:
            # If there is no project with the given URL, output a 404 page
            raise Http404
        
        context['project_name'] = project.name

        return context

    # More readable properties for kwargs arguments
    @property
    def project_url(self):
       return self.kwargs['project_url']



class UserEntryView(TemplateView):
    template_name = "user_entry_form.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)

        project = ProjectDefinition.objects.get(url=self.project_url)
        # Add to different context entries for html and python (javascript needs a serialized version)
        context["entry_definitions"] = project.entry_definitions.all()
        context["entry_definitions_js"] = serializers.serialize("json", context["entry_definitions"])
        return context
    
    @property
    def project_url(self):
        return self.kwargs["project_url"]
