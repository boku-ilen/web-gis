# web-gis

## setup

Make sure GDAL is installed system-wide.

Install the required Python libraries: `pip3 install -r requirements.txt`

Setup the server:

```sh
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

In the admin interface (127.0.0.1:8000/admin/webgis), entries and definitions can be created for testing.

## models

The basic architecture is a modular connection of:

- A `ProjectDefinition` consists of multiple `EntryDefinition`s for survey entry and (optionally) one `EntryDefinition` for demographic data. 
- An `EntryDefinition` is model of one or more typed fields which are automatically reflected in the UI (see `/webgis/static/ui_reflection.js`). 
    - The field defintion has to a JSON-like map, with (key->name, value->type).
    - Each value->type in the dictionary has to be defined in `/webgis/static/ui_reflection.js`
- A User entry which will be of the format defined by its entry definition

## EntryDefinition examples

### Survey

```json
{
  "An diesem Ort kann ich mir Synergies zwischen folgenden Punkten vorstellen": {
    "type": "Checkbox",
    "description": "Wählen Sie alle zutreffenden Felder aus.",
    "params": {
      "values": [
        "PV Anlagen",
        "Artenvielfalt",
        "Freizeitnutzung",
        "Naturschutz"
      ]
    }
  },
  "Zustimmung": {
    "type": "Radio",
    "params": {
      "values": [
        "Diesen Standort empfinde ich als sehr relevant für Artenvielfalt",
        "Diesen Standort empfinde ich als relevant für Artenvielfalt",
        "Diesen Standort empfinde ich als wenig relevant für Artenvielfalt",
        "Diesen Standort empfinde ich als nicht relevant für Artenvielfalt"
      ]
    }
  },
  "Schönheit des Ortes": {
    "type": "Spinbox",
    "description": "(1 ... nicht schön, 10 ... sehr schön)",
    "params": {
      "min_value": 0,
      "max_value": 10,
      "step": 1,
      "value": 5
    }
  },
  "Kommentar": {
    "type": "Comment",
    "params": {}
  },
  "Bild": {
    "type": "Image",
    "params": {}
  },
  "Semantic": {
     "type": "SemanticDifferential",
     "params": {
       "scales": [
         "very",
         "somewhat",
         "neither/nor",
         "somewhat",
         "very"
       ],
       "rowDefinitions": [
         [
           "experienced",
           "inexperienced"
         ],
         [
            "effective",
            "ineffective"
         ]
       ]
     }
   }
}
```

### Demographics

```json
{
  "Alter": {
    "type": "Spinbox",
    "params": {
      "min_value": 0,
      "max_value": 150,
      "step": 1,
      "value": 35
    }
  },
  "Gemeinde": {
    "type": "Dropdown",
    "description": "Wählen Sie die Gemeinde, in der Sie wohnhaft sind.",
    "params": {
      "values": [
        "Testgemeinde 1",
        "Testgemeinde 2",
        "Testgemeinde 3",
        "Andere"
      ]
    }
  }
}
```
