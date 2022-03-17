from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id       = models.BigIntegerField()
    kakao_nickname = models.CharField(max_length=45)
    email          = models.EmailField(max_length=200)
    mileage        = models.IntegerField()

    class Meta:
        db_table = 'users'

class Reservation(TimeStampModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'

class PassengerInformation(TimeStampModel):
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    gender          = models.CharField(max_length=45)
    email           = models.CharField(max_length=200)
    birth_date      = models.CharField(max_length=45)
    price           = models.DecimalField(max_digits=20, decimal_places=1)
    reservation     = models.ForeignKey('users.Reservation', on_delete=models.CASCADE)
    flight_schedule = models.ForeignKey('flights.FlightSchedule', on_delete=models.CASCADE)
    seat            = models.ForeignKey('flights.Seat', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'passenger_informations'
