from django.contrib import admin

from events.models import Event, EventTicket, EventSeat, UserProfile, TicketReservation
from user.models import User


admin.site.register(Event)
admin.site.register(EventTicket)
admin.site.register(EventSeat)
admin.site.register(UserProfile)
admin.site.register(TicketReservation)
admin.site.register(User)

