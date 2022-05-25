from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
	path('iss', views.show_location, name = 'show_location'),
	path('peeps', views.show_people, name = 'show_people'),
]


