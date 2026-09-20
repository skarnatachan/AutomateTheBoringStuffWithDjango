from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("import-data/", views.import_data, name="import_data"),
]
