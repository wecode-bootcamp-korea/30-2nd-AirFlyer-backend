import requests, json, datetime

from datetime import datetime
from posixpath import split

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from users.models import PassengerInformation
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
        flight_schedule_id  = request.GET.get('flight_schedule_id', None)
        departure_planet_id = request.GET.get('departure_planet_id', None)
        arrival_planet_id   = request.GET.get('arrival_planet_id', None)
        departure_datetime  = request.GET.get('departure_datetime', None)
        arrival_datetime    = request.GET.get('arrival_datetime', None)

        departure_datetime        = departure_datetime.split(" ") 
        departure_datetime_string = departure_datetime[0]+' '+departure_datetime[1]
        departure_datetime        = datetime.strptime(departure_datetime_string, '%Y-%m-%d %H:%M:%S')
        
        arrival_datetime        = arrival_datetime.split(" ")
        arrival_datetime_string = arrival_datetime[0]+' '+arrival_datetime[1]
        arrival_datetime        = datetime.strptime(arrival_datetime_string, '%Y-%m-%d %H:%M:%S')
        
        economy_seat_price  = int(FlightSchedule.objects.get(id=flight_schedule_id).default_price)
        business_seat_price = int(FlightSchedule.objects.get(id=flight_schedule_id).default_price) * Seat.objects.get(type = '비즈니스').price_ratio/100

        # eco = flight_schedule.flight.seats.all()[0]
        # eco.type ==> '이코노미'
        # eco_seat = flight_schedule.flight.flightseat_set.get(seat=eco).seat_availability
        
        economy = Seat.objects.get(type = '이코노미')
        business = Seat.objects.get(type = '비즈니스')
        print(economy)
        print(business)

        # economy_seat = FlightSchedule.objects.filter
        
        total_reservated_economy_seat = PassengerInformation.objects.filter(seat_id = 1).count()
        print(total_reservated_economy_seat)
        total_reservated_business_seat = PassengerInformation.objects.filter(seat_id = 2).count()
        print(total_reservated_business_seat)
        # 같은 스케쥴에 seat_id가 1이면 economy이니깐  
        # economy_seat_remain = economy_seat_availability - total_reservated_economy_seat

        q = Q()

        if departure_datetime:
            q &= Q(departure_datetime = departure_datetime)

        if arrival_datetime:
            q &= Q(arrival_datetime = arrival_datetime)

        flight_filter = FlightSchedule.objects.filter(q)

        result = [{
            'flight_schedule_info' : {
                'flight_schedule_id'    : flight.id,
                'departure_planet_code' : flight.departure_planet.code,
                'arrival_planet_code'   : flight.arrival_planet.code,
                'departure_datetime' : flight.departure_datetime,
                'arrival_datetime' : flight.arrival_datetime,
                'duration' : flight.duration
            },
            'flight_seat_info' : {
                # 'economy_seat_remain' 
                # 'business_seat_remain'
                'economy_seat_price' : economy_seat_price,
                'business_seat_price' : business_seat_price
            }
        }for flight in flight_filter]

        return JsonResponse({'result' : result}, status = 200)