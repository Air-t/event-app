from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator
from user.models import User, UserProfile

from events.utils import now_plus_15_min


TICKET_TYPES = (
    (0, 'Regular'),
    (1, 'Discount'),
    (2, 'Premium'),
    (3, 'V.I.P'),
    (4, 'Family'),
)

PAYMENT_TYPE = {
    (0, 'Card'),
    (1, 'Bank Transfer'),
    (2, 'PayPal'),
}


class Event(models.Model):
    """Event model"""
    name = models.CharField(unique=True, max_length=256)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    # TODO may be implemented as separate 'Address' model in future
    city = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EventSeat(models.Model):
    type = models.IntegerField(choices=TICKET_TYPES, default=0, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class EventTicket(models.Model):
    """Event ticket model"""
    price_bought = models.FloatField(validators=[MinValueValidator(0.0)])
    date_bought = models.DateTimeField(default=datetime.now)
    is_payed = models.BooleanField(default=False)

    seat = models.OneToOneField(EventSeat, on_delete=models.CASCADE)
    user = models.OneToOneField(User, default=None, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}, quantity: {self.quantity}"


class TicketReservation(models.Model):
    """Reservation model"""
    date_created = models.DateTimeField(default=datetime.now)
    date_expired = models.DateTimeField(default=now_plus_15_min)

    ticket = models.OneToOneField(EventTicket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ticket.user.username}: expires in: {(self.date_expired - self.date_created)}"


class Payment(models.Model):
    """Payment model"""
    type = models.IntegerField(choices=PAYMENT_TYPE, default=0)
    date_payed = models.DateTimeField(default=datetime.now)

    ticket = models.OneToOneField(EventTicket, on_delete=models.CASCADE)

    def __str__(self):
        return self.type
