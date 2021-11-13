from django.urls import path

from . import views

app_name = "beers"

urlpatterns = [
    path(route='',                   view=views.index,      name='index'),
    path(route='tags/',              view=views.tags,       name='tags'),
    path(route='<int:beer_id>/',     view=views.beer_view,  name='beer_view'),
    path(route='beers_by_tag/<int:tag_id>/', view=views.beers_by_tag,  name='beers_by_tag'),
]