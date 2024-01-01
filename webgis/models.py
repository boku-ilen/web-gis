from djgeojson.fields import GeoJSONField
from django.db import models
from django.contrib.postgres.fields import ArrayField


#
# Definitions
#

class EntryDefinitionManager(models.Manager):
    def get_by_natural_key(self, name, field_definition):
        return self.get(name=name, field_definition=field_definition)


class EntryDefinition(models.Model):
    
    objects = EntryDefinitionManager()
    name = models.CharField(max_length=256)
    field_definition = models.JSONField(db_index=True)

    def natural_key(self):
        return (self.name, self.field_definition)

    class Meta:
        unique_together = (('name', 'field_definition'),)


class ProjectDefinition(models.Model):
    
    url = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    survey_entry_definitions = models.ManyToManyField(EntryDefinition, related_name="project_surveys")
    demographic_entry_definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE, null=True, blank=True, related_name="project_demographics")


#
# User entries
#

class LocationEntry(models.Model):

    project = models.ForeignKey(ProjectDefinition, to_field="url", on_delete=models.CASCADE)
    geom = GeoJSONField()


class SurveyEntry(models.Model):

    project = models.ForeignKey(ProjectDefinition, to_field="url", on_delete=models.CASCADE)
    location_entry = models.ForeignKey(LocationEntry, on_delete=models.CASCADE)
    definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE)
    field_data = models.JSONField(db_index=True)

class DemographicEntry(models.Model):

    survey_entry = models.OneToOneField(SurveyEntry, on_delete=models.CASCADE, primary_key=True)
    definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE)
    field_data = models.JSONField(db_index=True)
