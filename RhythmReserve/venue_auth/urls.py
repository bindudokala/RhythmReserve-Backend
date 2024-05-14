from django.urls import path



from . import views

urlpatterns = [
    path("venue_signup/", views.venue_signup, name="venue_signup"),
    path("venue_login/", views.venue_login, name="venue_login"),
    path("get_venue_data/", views.get_venue_data, name="get_venue_data"),
]
