from djgeojson.views import GeoJSONLayerView
from .models import UserEntry


def get_entry_data():
    return GeoJSONLayerView.as_view(model=UserEntry, properties=('field_data'))