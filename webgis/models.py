from djgeojson.fields import PolygonField
from django.db import models
from django.contrib.postgres.fields import ArrayField


class EntryDefinition(models.Model):
    
    name = models.CharField(max_length=256)
    field_definition = models.JSONField(db_index=True)


class UserEntry(models.Model):

    field_data = models.JSONField(db_index=True)
    geom = PolygonField()


class ProjectDefinition(models.Model):
    
    url = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    entry_definitions = models.ManyToManyField(EntryDefinition)
