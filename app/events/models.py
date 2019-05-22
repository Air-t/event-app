from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from events.utils import now_plus_15_min


class UserProfile(models.Model):
    """Extends base django user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


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
    name = models.CharField(unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class EventSeat(models.Model):
    type = models.IntegerField(choices=TICKET_TYPES, default=0)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0.0)])


class EventTicket(models.Model):
    """Event ticket model"""
    price_bought = models.FloatField(validators=[MinValueValidator(0.0)])
    date_bought = models.DateTimeField(default=datetime.now)

    seat = models.OneToOneField(EventSeat, on_delete=models.CASCADE)
    user = models.OneToOneField(UserProfile, default=None, blank=True)

    def __str__(self):
        return f"{self.type}, quantity: {self.quantity}"


class TicketReservation(models.Model):
    """Reservation model"""
    date_created = models.DateTimeField(default=datetime.now)
    date_expired = models.DateTimeField(default=now_plus_15_min)
    is_confirmed = models.BooleanField(default=False)

    ticket = models.OneToOneField(EventTicket, on_delete=models.CASCADE)


class Payment(models.Model):
    type = models.IntegerField(choices=PAYMENT_TYPE, default=0)
    date_payed = models.DateTimeField(default=datetime.now)
