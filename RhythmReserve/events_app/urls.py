from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_event/", views.create_event, name="create_event"),
    path("update_event/<int:event_id>/", views.update_event, name="update_event"),
    path("delete_event/<int:event_id>/", views.delete_event, name="delete_event"),
    path("event_detail/<int:event_id>/", views.event_detail, name="event_detail"),
    path("get_events/", views.get_events, name="get_events"),
    path("search_events/", views.search_events, name="search_events"),
    path("upcoming_events/", views.upcoming_events, name="upcoming_events")

]