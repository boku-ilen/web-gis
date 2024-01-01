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


def api_get_entries(request: WSGIRequest, project_url):
    entries = SurveyEntry.objects.select_related().filter(project=project_url).values(
        "field_data",
        "location_entry__geom"
    )
    return JsonResponse(list(entries), safe=False)


# Returns an is_valid boolean, an error message, and the related attribute title
def validate_entry_data(entry_data, definition_data):
    # Check whether there is superfluous data
    for attribute_title, values in entry_data.items():
        if not attribute_title in definition_data:
            return False, "UNDEFINED_ENTRY", attribute_title

    # Check if all required attributes from the definition are present
    for attribute_title, attribute_def in definition_data.items():
        attribute_type = attribute_def["type"]

        if attribute_type == "Checkbox":
            if attribute_title in entry_data:
                for value in entry_data[attribute_title]:
                    if not value in attribute_def["params"]["values"]:
                        return False, "UNDEFINED_CHECKBOX_VALUE", attribute_title
        elif attribute_type == "Radio" or attribute_type == "Dropdown":
            if not attribute_title in entry_data:
                return False, "MISSING_RADIO_INPUT", attribute_title
            
            if not entry_data[attribute_title][0] in attribute_def["params"]["values"]:
                return False, "UNDEFIND_RADIO_VALUE", attribute_title
        elif attribute_type == "Spinbox":
            if not attribute_title in entry_data or not entry_data[attribute_title][0]:
                return False, "MISSING_SPINBOX_INPUT", attribute_title
            
            if float(entry_data[attribute_title][0]) > attribute_def["params"]["max_value"] \
                    or float(entry_data[attribute_title][0]) < attribute_def["params"]["min_value"]:
                return False, "INVALID_SPINBOX_VALUE", attribute_title
        elif attribute_type == "Bild":
            # TODO: Add "Required" property and validate?
            pass
 
    return True, "", ""


def create_entry(request: WSGIRequest, project_url):
    # get project via unique project_url
    # get EntryDefinition and field values with calls like request.POST['<field_name>']
    if request.method == "POST":
        try:
            rq = json.loads(request.body.decode('utf-8'))
            project = ProjectDefinition.objects.get(url=rq["project"])
            definition = EntryDefinition.objects.get(id=rq["definition"])

            # Validate
            is_valid, error, attribute = validate_entry_data(rq["survey_data"], definition.field_definition)
            if not is_valid:
                print(f"Request with data {rq} was invalid with error {error} in attribute {attribute}")
                return JsonResponse({"success": False, "error": error, "attribute": attribute})
            
            # Location entry exists and is correct project, so we can use it
            if "location_entry_id" in rq and LocationEntry.objects.filter(project=project, id=rq["location_entry_id"]).exists():
                location_entry = LocationEntry.objects.get(id=rq["location_entry_id"])
            # Otherwise, we need to create it
            else:
                location_entry = LocationEntry(project=project, geom=rq["geom"])

            new_survey_entry = SurveyEntry(
                project=project,
                definition=definition,
                location_entry=location_entry,
                field_data=rq["survey_data"]
            )
            
            if project.demographic_entry_definition:
                # Validate
                is_valid, error, attribute = validate_entry_data(rq["demographic_data"], project.demographic_entry_definition.field_definition)
                if not is_valid:
                    print(f"Request with data {rq} was invalid with error {error} in attribute {attribute}")
                    return JsonResponse({"success": False, "error": error, "attribute": attribute})

                new_demographic_entry = DemographicEntry(
                    survey_entry=new_survey_entry,
                    definition=project.demographic_entry_definition,
                    field_data=rq["demographic_data"]
                )
                
                # Save all if valid
                location_entry.save()
                new_survey_entry.save()
                new_demographic_entry.save()
            else:
                # No demographic entry definition, so we can save everything
                location_entry.save()
                new_survey_entry.save()

            # return success
            return JsonResponse({"success": True})
        except Exception:
            traceback.print_exc()
            return JsonResponse({"success": False, "error": "SERVER_ERROR"})




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

        context["survey_entry_definitions"] = project.survey_entry_definitions.all()
        context["survey_entry_definitions_js"] = serializers.serialize("json", context["survey_entry_definitions"])

        context["demographic_entry_definition"] = [project.demographic_entry_definition]
        context["demographic_entry_definition_js"] = serializers.serialize("json", context["demographic_entry_definition"]) \
                if project.demographic_entry_definition else {}
        
        return context
    

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["geometry"] = request.POST["geometry"]

        return self.render_to_response(context)
    
    @property
    def project_url(self):
        return self.kwargs["project_url"]
