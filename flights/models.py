from django.db import models
from core.models import TimeStampModel

class FlightSchedule(TimeStampModel):
    departure_datetime = models.DateTimeField()
    arrival_datetime   = models.DateTimeField()
    duration           = models.IntegerField()
    default_price      = models.DecimalField(max_digits=20, decimal_places=1)
    flight             = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)
    arrival_planet     = models.ForeignKey('flights.Planet', on_delete=models.CASCADE, related_name='arrival_flight')
    departure_planet   = models.ForeignKey('flights.Planet', on_delete=models.CASCADE, related_name='departure_flight')

    class Meta:
        db_table = 'flight_schedules'

class Planet(TimeStampModel):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=45)

    class Meta:
        db_table = 'planets'

class Flight(TimeStampModel):
    name = models.CharField(max_length=45)
    seats = models.ManyToManyField('flights.Seat', through='FlightSeat')

    class Meta:
        db_table = 'flights'

class FlightSeat(TimeStampModel):
    seat_availability = models.IntegerField()
    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)
    seat   = models.ForeignKey('flights.Seat', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'flight_seats'

class Seat(TimeStampModel):
    type        = models.CharField(max_length=45)
    price_ratio = models.IntegerField()

    class Meta:
        db_table = 'seats'