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
    """Event seat model available"""
    type = models.IntegerField(choices=TICKET_TYPES, default=0)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0.0)])

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['type', 'event']

    def __str__(self):
        return f"{self.type}: {self.tickets_available}/{self.quantity}"

    @property
    def tickets_available(self):
        return self.quantity - EventTicket.objects.all()\
            .filter(seat__event=self.event)\
            .filter(seat__type=self.type).count()


class EventTicket(models.Model):
    """Event ticket model"""
    date_bought = models.DateTimeField(default=datetime.now)
    is_payed = models.BooleanField(default=False)
    is_in_payment = models.BooleanField(default=False)

    seat = models.ForeignKey(EventSeat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=None, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.seat}, {self.user.username}"

    @property
    def tickets_price_by_type(self):
        return sum([ticket.seat.price
                    for ticket in EventTicket.objects.all().filter(user=self.user).filter(seat__type=self.seat.type)])

    @property
    def tickets_count_by_type(self):
        return EventTicket.objects.all().filter(user=self.user).filter(
            seat__type=self.seat.type).count()

    @property
    def tickets_price_by_event(self):
        return sum([ticket.seat.price
                    for ticket in EventTicket.objects.all().filter(user=self.user).filter(seat__event=self.seat.event)])

    @property
    def tickets_count_by_event(self):
        return EventTicket.objects.all().filter(user=self.user).filter(
            seat__event=self.seat.event).count()


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
