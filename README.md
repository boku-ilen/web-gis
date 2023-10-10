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

- A `ProjectDefinition` consists of multiple `EntryDefinition`s. 
- An `EntryDefinition` is model of one or more typed fields which are automatically reflected in the UI (see `/webgis/static/ui_reflection.js`). 
    - The field defintion has to a JSON-like map, with (key->name, value->type). For instance:
```json
{
    "Approval": {
        "type": "Radio", 
        "params": {
            "values": ["mir gefällt dieses Windrad sehr gut", "mir gefällt dieses Windrad", "mir gefällt dieses Windrad nicht", "ich finde dieses Windrad grässlich!"]}}, 
    "Okay": {
        "type": "Dropdown", 
        "params": {
            "values": [0, 1, 2]
        }
    }, 
    "Zustimmung": {
        "type": "Spinbox", 
        "params": {
            "min_value": 0, "max_value": 10, "step": 1, "value": 5
        }
    }, 
    "Kommentar": {
        "type": "Comment", 
        "params": {}
    }, 
    "Bild": {
        "type": "Image", 
        "params": {}
    }
}
```
    - Each value->type in the dictionary has to be defined in `/webgis/static/ui_reflection.js`
- A User entry which will be of the format defined by its entry definition
