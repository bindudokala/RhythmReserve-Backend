from django.db import models
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    venue_user_email = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    event_time = models.CharField(max_length=255)  # Storing time as a Unix timestamp
    event_location = models.CharField(max_length=255)
    event_image_url = models.URLField(max_length=1024)
    available_general_admission_tickets = models.PositiveIntegerField()
    general_admission_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_vip_tickets = models.PositiveIntegerField()
    vip_ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=60)
    description = models.TextField()
    
    # Add venue_user field as a ForeignKey to VenueUser model
    #venue_user = models.ForeignKey('venue_auth.VenueUser', on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.event_name

    def get_event_time(self):
        # import time
        # return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.event_time))
        return self.event_time
    
    @classmethod
    def create_event(cls, venue_user_email, event_name, event_time, event_location, event_image_url,
                     available_general_admission_tickets, general_admission_price,
                     available_vip_tickets, vip_ticket_price, genre, description):
        # Custom method to create a new Event instance.
        event = cls(venue_user_email=venue_user_email,
                    event_name=event_name,
                    event_time=event_time,
                    event_location=event_location,
                    event_image_url=event_image_url,
                    available_general_admission_tickets=available_general_admission_tickets,
                    general_admission_price=general_admission_price,
                    available_vip_tickets=available_vip_tickets,
                    vip_ticket_price=vip_ticket_price,
                    genre=genre,
                    description=description)
        event.save()
        return event
