from djgeojson.fields import PointField
from django.db import models
from django.contrib.postgres.fields import ArrayField


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
    entry_definitions = models.ManyToManyField(EntryDefinition)
    

class UserEntry(models.Model):

    project = models.ForeignKey(ProjectDefinition, to_field="url", on_delete=models.CASCADE)
    definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE)
    field_data = models.JSONField(db_index=True)
    geom = PointField()
