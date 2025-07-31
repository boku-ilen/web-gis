from djgeojson.fields import PointField, MultiPointField
from django.db import models
from django_jsonform.models.fields import JSONField


#
# Definitions
#

class EntryDefinitionManager(models.Manager):
    def get_by_natural_key(self, name, field_definition):
        return self.get(name=name, field_definition=field_definition)


class EntryDefinition(models.Model):
    FORM_TYPES = [
        "Comment",
        "MultiLineText",
        "Dropdown",
        "Spinbox",
        "Image",
        "Radio",
        "Checkbox",
        "SemanticDifferential",
        "MatrixQuestions",
    ]
    
    PARAMS_SCHEMA = {
        "Comment_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Comment" },
            },
            "additionalProperties": False
        },
        "MultiLineText_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "MultiLineText" },
            },
            "additionalProperties": False
        },
        "Dropdown_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Dropdown" },
                "values": {
                    "type": "array",
                    "title": "Options",
                    "minItems": 2,
                    "items": {"type": "string"}
                }
            },
            "required": ["values"],
            "additionalProperties": False
        },
        "Spinbox_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Spinbox" },
                "min_value": {"type": "number"},
                "max_value": {"type": "number"},
                "step": {"type": "number"},
                "value": {"type": "number"}
            },
            "required": ["min", "max", "step", "value"],
            "additionalProperties": False
        },
        "Image_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Image" },    
            },
            "additionalProperties": False
        },
        "Radio_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Radio" },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["values"],
            "additionalProperties": False
        },
        "Checkbox_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "Checkbox" },
                "values": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["values"],
            "additionalProperties": False
        },
        "SemanticDifferential_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "SemanticDifferential" },
                "scales": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "rowDefinitions": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2,
                    }
                }
            }
        },
        "MatrixQuestions_params": {
            "type": "object",
            "properties": {
                "kind": { "const": "MatrixQuestions" },
                "scales": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
    
    DEFINITION_SCHEMA = {
        "type": "array",
        "items": {
            "type": "dict",
            "keys": {
                "question": {
                    "type": "string"
                },
                "description": {
                    "type": "string",
                    "helpText": "(Optionally) explain the user how to operate this field and what it means (e.g. \"1... very dissatisfactory, 5... very satisfactory\")"
                },
                "type": {
                    "type": "string",
                    "choices": FORM_TYPES
                },
                "params": {
                    "oneOf": [
                        { "title": "Comment", "$ref": "#/$defs/Comment_params", "default": {"kind": "Comment"} },
                        { "title": "MultiLineText", "$ref": "#/$defs/MultiLineText_params", "default": {"kind": "MultiLineText"} },
                        { "title": "Dropdown", "$ref": "#/$defs/Dropdown_params", "default": {"kind": "Dropdown"} },
                        { "title": "Spinbox", "$ref": "#/$defs/Spinbox_params", "default": {"kind": "Spinbox"} },
                        { "title": "Image", "$ref": "#/$defs/Image_params", "default": {"kind": "Image"} },
                        { "title": "Radio", "$ref": "#/$defs/Radio_params", "default": {"kind": "Radio"} },
                        { "title": "Checkbox", "$ref": "#/$defs/Checkbox_params", "default": {"kind": "Checkbox"} },
                        { "title": "SemanticDifferential", "$ref": "#/$defs/SemanticDifferential_params", "default": {"kind": "SemanticDifferential"} },
                        { "title": "MatrixQuestions", "$ref": "#/$defs/MatrixQuestions_params", "default": {"kind": "MatrixQuestions"} },
                    ]
                },
            },
            "required": ["question", "type"]
        },
        "$defs": PARAMS_SCHEMA
    }
    
    objects = EntryDefinitionManager()
    name = models.CharField(max_length=256)
    field_definition = JSONField(schema=DEFINITION_SCHEMA, db_index=True)

    def natural_key(self):
        return (self.name, self.field_definition)

    class Meta:
        unique_together = (('name', 'field_definition'),)


class ProjectDefinition(models.Model):
    
    url = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    bounds = MultiPointField(null=True, blank=True)
    limit_to_bounds = models.BooleanField(default=False)
    survey_entry_definitions = models.ManyToManyField(EntryDefinition, related_name="project_surveys")
    demographic_entry_definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE, null=True, blank=True, related_name="project_demographics")


#
# User entries
#

class LocationEntry(models.Model):

    project = models.ForeignKey(ProjectDefinition, to_field="url", on_delete=models.CASCADE)
    geom = PointField()


class SurveyEntry(models.Model):

    project = models.ForeignKey(ProjectDefinition, to_field="url", on_delete=models.CASCADE)
    location_entry = models.ForeignKey(LocationEntry, on_delete=models.CASCADE)
    definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE)
    field_data = models.JSONField(db_index=True)

class DemographicEntry(models.Model):

    survey_entry = models.OneToOneField(SurveyEntry, on_delete=models.CASCADE, primary_key=True)
    definition = models.ForeignKey(EntryDefinition, on_delete=models.CASCADE)
    field_data = models.JSONField(db_index=True)
