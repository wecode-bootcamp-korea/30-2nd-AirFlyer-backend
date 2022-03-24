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

        """
        목적: 플라이트 스케줄 리스트 정보 get
        조건:
            1. 출발지, 도착지
            2. 입력한 날짜에 예약이 가능한 스케줄
        정렬:
            1. 출발 시간
            2. 도착 시간
            3. 비행 시간
            4. 가격 

        
        """
        sort                = request.GET.get('sort', 'departure_time')
        departure_planet_id = request.GET.get('departure_planet_id', None)
        arrival_planet_id   = request.GET.get('arrival_planet_id', None)
        departure_datetime  = request.GET.get('departure_datetime', None)
        
        
        # departure_datetime        = departure_datetime.split(" ") 
        # departure_datetime_string = departure_datetime[0]+' '+departure_datetime[1]
        # departure_datetime        = datetime.strptime(departure_datetime_string, '%Y-%m-%d %H:%M:%S')
        
        # arrival_datetime        = arrival_datetime.split(" ")
        # arrival_datetime_string = arrival_datetime[0]+' '+arrival_datetime[1]
        # arrival_datetime        = datetime.strptime(arrival_datetime_string, '%Y-%m-%d %H:%M:%S')
        "2022-03-31"

        sort_set = {
            "departure_time" : "departure_datetime",
            "arrival_time"   : "arrival_datetime",
            "duration"       : "duration",
            "price"          : "default_price"
        }
        
        q = Q()

        if departure_planet_id and arrival_planet_id:
            q &= Q(departure_planet_id=departure_planet_id)
            q &= Q(arrival_planet_id=arrival_planet_id)
        
        if departure_datetime:
            q &= Q(departure_datetime = departure_datetime)

        flight_schedules = FlightSchedule.objects.filter(q).order_by(sort_set.get(sort, "departure_time"))

        result = [{
            'flight_schedule_info' : {
                'flight_schedule_id'    : flight_schedule.id,
                'departure_planet_code' : flight_schedule.departure_planet.code,
                'arrival_planet_code'   : flight_schedule.arrival_planet.code,
                'departure_datetime'    : flight_schedule.departure_datetime,
                'arrival_datetime'      : flight_schedule.arrival_datetime,
                'duration'              : flight_schedule.duration
            },
            'flight_seat_info' : [{
                'seat_id'     : flightseat.seat.id,
                'seat_type'   : flightseat.seat.type,
                'seat_remain' : flightseat.seat_availability - \
                                flight_schedule.passengerinformation_set.filter(seat=flightseat.seat).count(),
                'seat_price': float(flight_schedule.fligth.default_price * flightseat.seat.price_ratio/100)
            }for flightseat in flight_schedule.fligth.flightseat_set.all()]
        }for flight_schedule in flight_schedules]

        return JsonResponse({'result' : result}, status = 200)