"""webgis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, register_converter
from django.views.generic import TemplateView

from . import converters, views

register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    path('<str:project_url>/', views.ProjectView.as_view(), name="project"),
    path('<str:project_url>/create/', views.create_entry, name="project"),
    path('api/entries/<str:project_url>', views.api_get_entries, name="api_entries"),
    path('<str:project_url>/user-entry/<float:lat>/<float:lon>', views.SurveyEntryView.as_view(), name='user_entry'),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
