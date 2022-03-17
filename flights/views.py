import requests, json, datetime

from datetime import date, datetime, timedelta
from posixpath import split

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from flights.models import Flight, FlightSchedule, Planet, Seat, FlightSeat

class PlanetListView(View):
    def get(self, request):
        
        planets = Planet.objects.all()

        result = [
            {
                'planet_id'   : planet.id,
                'planet_name' : planet.name,
                'planet_code' : planet.code
            } for planet in planets]

        return JsonResponse({'planet_list' : result}, status = 200)

class FlightListView(View):
    def get(self, request):
        sort                = request.GET.get('sort', 'departure_time')
        departure_planet_id = request.GET.get('departure_planet_id', None)
        arrival_planet_id   = request.GET.get('arrival_planet_id', None)
        departure_date      = request.GET.get('departure_date', None)

        sort_set = {
            "departure_time" : "departure_datetime", 
            "arrival_time"   : "arrival_datetime",
            "duration"       : "duration",
            "price"          : "default_price"
        }
        
        q = Q()

        if departure_planet_id and arrival_planet_id:
            q &= Q(departure_planet_id = departure_planet_id)
            q &= Q(arrival_planet_id   = arrival_planet_id)
        
        if departure_date:
            departure_datetime = datetime.strptime(departure_date, "%Y-%m-%d")
            q &= Q(departure_datetime__gte = departure_datetime)
            q &= Q(departure_datetime__lt  = departure_datetime + timedelta(days=1))


        flight_schedules = FlightSchedule.objects.filter(q).order_by(sort_set.get(sort, "departure_datetime"))

        result = [{
            'flight_schedule_info' : {
                'flight_schedule_id'    : flight_schedule.id,
                'departure_planet_code' : flight_schedule.departure_planet.code,
                'arrival_planet_code'   : flight_schedule.arrival_planet.code,
                'departure_datetime'    : flight_schedule.departure_datetime,
                'arrival_datetime'      : flight_schedule.arrival_datetime,
                'duration'              : str(flight_schedule.duration) + ":00", 
                'spaceship_name'        : flight_schedule.flight.name
            },
            'flight_seat_info' : [{
                'seat_id'     : flightseat.seat.id,
                'seat_type'   : flightseat.seat.type,
                'seat_remain' : flightseat.seat_availability - \
                                flight_schedule.passengerinformation_set.filter(seat=flightseat.seat).count(),
                'seat_price'  : int(flight_schedule.default_price * flightseat.seat.price_ratio/100)
            }for flightseat in flight_schedule.flight.flightseat_set.all()]
        }for flight_schedule in flight_schedules]

        return JsonResponse({'result' : result}, status = 200)