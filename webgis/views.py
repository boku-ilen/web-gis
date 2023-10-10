import json
import traceback
from django.core import serializers
from djgeojson.views import GeoJSONLayerView
from django.http import JsonResponse
from .models import EntryDefinition, LocationEntry, ProjectDefinition, SurveyEntry, DemographicEntry
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest


def create_entry(request: WSGIRequest, project_url):
    # get project via unique project_url
    # get EntryDefinition and field values with calls like request.POST['<field_name>']
    if request.method == "POST":
        try:
            rq = json.loads(request.body.decode('utf-8'))
            project = ProjectDefinition.objects.get(url=rq["project"])
            definition = EntryDefinition.objects.get(id=rq["definition"])

            # TODO: Validate rq["survey_data"] against definition
            
            # Location entry exists and is correct project, so we can use it
            if "location_entry_id" in rq and LocationEntry.objects.filter(project=project, id=rq["location_entry_id"]).exists():
                location_entry = LocationEntry.objects.get(id=rq["location_entry_id"])
            # Otherwise, we need to create it
            else:
                location_entry = LocationEntry(project=project, geom=rq["geom"])
                location_entry.save()

            new_survey_entry = SurveyEntry(
                project=project,
                definition=definition,
                location_entry=location_entry,
                field_data=rq["survey_data"]
            )
            new_survey_entry.save()
            
            if project.demographic_entry_definition:
                # TODO: Validate rq["demographic_data"] against project.demographic_entry_definition

                new_demographic_entry = DemographicEntry(
                    survey_entry=new_survey_entry,
                    definition=project.demographic_entry_definition,
                    field_data=rq["demographic_data"]
                )
                new_demographic_entry.save()
            # return success
            return JsonResponse({"success": True})
        except Exception:
            traceback.print_exc()
            
            raise Http404




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
        context['project_description'] = project.description

        entries = SurveyEntry.objects.filter(project=self.project_url)
        locations = LocationEntry.objects.filter(project=self.project_url)

        context["entries"] = serializers.serialize("json", entries.all(), use_natural_foreign_keys=True)
        context["locations"] = serializers.serialize("json", locations.all(), use_natural_foreign_keys=True)

        return context

    # More readable properties for kwargs arguments
    @property
    def project_url(self):
       return self.kwargs['project_url']



class SurveyEntryView(TemplateView):
    template_name = "user_entry_form.html"

    def get_context_data(self, *args, **kwargs):
        context = TemplateView.get_context_data(self, *args, **kwargs)

        project = ProjectDefinition.objects.get(url=self.project_url)
        # Add to different context entries for html and python (javascript needs a serialized version)
        context["survey_entry_definitions"] = project.survey_entry_definitions.all()
        context["survey_entry_definitions_js"] = serializers.serialize("json", context["survey_entry_definitions"])

        context["demographic_entry_definition"] = [project.demographic_entry_definition]
        context["demographic_entry_definition_js"] = serializers.serialize("json", context["demographic_entry_definition"]) \
                if project.demographic_entry_definition else {}
        
        return context
    
    @property
    def project_url(self):
        return self.kwargs["project_url"]
