import requests, jwt , json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import F
from django.db import transaction

from users.models     import User ,Reservation, PassengerInformation
from .decorator       import login_decorator
from my_settings      import ALGORITHM, SECRET_KEY

class SocialSignIn(View):
    def post(self, request):
            try:
                
                access_token    = request.headers.get('Authorization')
                profile_request = requests.get( "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"},)   
                profile_json    = profile_request.json()
                message_code    = profile_json.get("code",'')
                
                if message_code == -401:
                    return JsonResponse({"message" : "INVALID TOKEN"}, status = 401)
                
                kakao_id       = profile_json["id"]
                kakao_account  = profile_json["kakao_account"]
                kakao_nickname = kakao_account["profile"].get("nickname",'')     
                email          = kakao_account.get('email', 'not agreed')
                mileage        = 100000
                
                user, is_created = User.objects.get_or_create(
                    kakao_id = kakao_id, 
                    defaults = { 
                        "kakao_nickname" : kakao_nickname , 
                        "email"          : email ,
                        "mileage"        : mileage
                    }
                )

                status_code      = 201 if is_created else 200
                token            = jwt.encode({"user_id":user.id}, SECRET_KEY, ALGORITHM)
                
                return JsonResponse({"token": token},status = status_code)
                
            
            except KeyError:
                return JsonResponse({"message" : "KEYERROR"}, status = 400)


class ReservationView(View):
    
    @login_decorator 
    def post(self,request):
        try:
            data =  json.loads(request.body.decode('utf-8'))

            user         = request.user
            total_price  = data['total_price']
            user.mileage = F('mileage')-total_price
            
            with transaction.atomic():
                user.save()
                reservation = Reservation.objects.create(user_id=user.id)

            passenger_informations = data['passenger_informations']
            
            number_of_passenger    = len(passenger_informations)
            seat_hashmap           = {'이코노미':'1',"비즈니스":'2'} 
            
            for passenger_information in passenger_informations:   
                with transaction.atomic():
                    PassengerInformation.objects.create(
                                first_name         = passenger_information['first_name'],
                                last_name          = passenger_information['last_name'],
                                gender             = passenger_information['gender'],
                                email              = passenger_information['email'],
                                birth_date         = passenger_information['birth_date'],
                                price              = total_price/number_of_passenger ,
                                reservation_id     = reservation.id,
                                flight_schedule_id = passenger_information['flight_schedule_id'],
                                seat_id            = seat_hashmap[passenger_information['seat_name']]
                                )
                    

            return JsonResponse({"message":'success'},status=201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)
        