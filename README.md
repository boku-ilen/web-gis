# web-gis

## setup

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
{"Okay": "Boolean", "Approval": "Integer", "Comment": "String", "Image": "HTMLImageElement"}
```
    - Each value->type in the dictionary has to be defined in `/webgis/static/ui_reflection.js`
- A User entry which will be of the format defined by its entry definition