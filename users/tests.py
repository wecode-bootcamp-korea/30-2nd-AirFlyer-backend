import jwt,json
from datetime import datetime

from django.test       import TestCase
from django.test       import Client
from django.db         import transaction
from unittest.mock     import patch, MagicMock

from users.models     import User ,Reservation, PassengerInformation
from flights.models   import FlightSchedule, Planet , Flight, FlightSeat , Seat
from airflyer.settings import SECRET_KEY
from my_settings       import ALGORITHM

class socialSigninTest(TestCase):
    def setUp(self):                        
        User.objects.create(
            id              = 1,
            kakao_id        = 12345,
            kakao_nickname  = '김근성',
            email           = '600gstars@yahoo.co.kr',
            mileage         = 100000
        )

    def tearDown(self):                     
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_social_login_user_exist_success(self, mocked_requests):  

        client = Client()                             

        class MockedResponse:                                             
            def json(self):
                return {
                "id":12345,
                "kakao_account": { 
                    "profile": {
                        "nickname": "김근성",             
                    },
                    "email": '500gstars@yahoo.co.kr',
                    }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {'Authorization' : 'access_token'} 
        response = client.post("/users/signin", **headers)
        
        access_token = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.json(),{'token':access_token})
        self.assertEqual(response.status_code, 200)

    @patch("users.views.requests")
    def test_social_login_user_not_exist_success(self, mocked_requests):  

        client = Client()                             

        class MockedResponse:                                             
            def json(self):
                return {
                "id":66666,
                "kakao_account": { 
                    "profile": {
                        "nickname": "김근성",             
                    },
                    "email": '600gstars@yahoo.co.kr',
                    }
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {'Authorization' : 'access_token'} 
        response = client.post("/users/signin", **headers)
        
        access_token = jwt.encode({'user_id':2}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.json(),{'token':access_token})
        self.assertEqual(response.status_code, 201)

    @patch("users.views.requests")
    def test_social_login_user_invalid_token_fail(self, mocked_requests):  

        client = Client()                             

        class MockedResponse:                                             
            def json(self):
                return {'msg': 'this access token does not exist', 'code': -401}

        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers  = {'Authorization' : 'access_token'} 
        response = client.post("/users/signin", **headers)
        
        self.assertEqual(response.status_code, 401)


class ReservationTest(TestCase):
    def setUp(self):                        
        User.objects.create(
            id              = 1,
            kakao_id        = 12345,
            kakao_nickname  = '김근성',
            email           = '600gstars@yahoo.co.kr',
            mileage         = 100000
        )
        departure_planet= Planet.objects.create(
            name ='지구', 
            code = "ETH"
            )
        arrival_planet = Planet.objects.create(
            name ='달',   
            code = "MON"
            )

        Seat.objects.create(
            id = 1,
            type = "이코노미",
            price_ratio = 100
            )
        Seat.objects.create(
            id = 2,
            type = "비즈니스",
            price_ratio = 150
            )
        
        Flight.objects.create(
            id  = 1,
            name="출퇴근 우주선"
            )
        Flight.objects.create(
            id = 2,
            name="초호화 우주선"
            )
       
        departure_datetime = datetime.strptime('2023-03-18 9:00:00', '%Y-%m-%d %H:%M:%S')
        arrive_datetime    = datetime.strptime('2023-03-18 12:00:00', '%Y-%m-%d %H:%M:%S')
        
        FlightSchedule.objects.create(
            id                 = 1,
            departure_datetime = departure_datetime, 
            arrival_datetime   = arrive_datetime,
            duration           = 2,
            default_price      = 10000,
            flight_id          = 1,
            arrival_planet     = arrival_planet,
            departure_planet   = departure_planet
        )
        
        
    def tearDown(self):                     
        User.objects.all().delete()
        Reservation.objects.all().delete()
        PassengerInformation.objects.all().delete()
        Planet.objects.all().delete()
        Seat.objects.all().delete()
        Flight.objects.all().delete()
        FlightSchedule.objects.all().delete()
    def test_reservation_success(self):  

            client = Client()                             
            
            data={      
                'total_price' : 20000,
                    
                "passenger_informations" : 
                [
                    {
                        "first_name"         : "김", 
                        "last_name"          : "근성1",  
                        "gender"             : "남" , 
                        "email"              : "email1@naver.com", 
                        "birth_date"         : "1984.08.04", 
                        "user_id"            : 1, 
                        "flight_schedule_id" : 1 ,
                        "seat_name"          : "이코노미"
                    },
                    {
                        "first_name"         : "김", 
                        "last_name"          : "근성2", 
                        "gender"             : "여" , 
                        "email"              : "email2@naver.com",
                        "birth_date"         : "1984.08.04",
                        "user_id"            : 1,
                        "flight_schedule_id" : 1 ,
                        "seat_name"          : "이코노미"
                    }
                ]
                    
                }
            
            access_token = jwt.encode({'user_id' : 1 }, SECRET_KEY, ALGORITHM)

            response     = client.post("/users/reservation",json.dumps(data), content_type='application/json' ,HTTP_Authorization = access_token)
            
            passenger_1= PassengerInformation.objects.get(id=1)
            passenger_2= PassengerInformation.objects.get(id=2)
            
            saved_test_data = {      
                    'total_price' : User.objects.get(id=1).mileage ,

                    "passenger_informations" : 
                    [
                        {
                            "first_name"         : passenger_1.first_name, 
                            "last_name"          : passenger_1.last_name,  
                            "gender"             : passenger_1.gender , 
                            "email"              : passenger_1.email, 
                            "birth_date"         : passenger_1.birth_date, 
                            "price"              : passenger_1.price, 
                            "reservation_id"     : passenger_1.reservation_id ,
                            "flight_schedule_id" : passenger_1.flight_schedule_id ,
                            "seat_id"            : passenger_1.seat_id
                        },
                        {
                            "first_name"         : passenger_2.first_name, 
                            "last_name"          : passenger_2.last_name,  
                            "gender"             : passenger_2.gender , 
                            "email"              : passenger_2.email, 
                            "birth_date"         : passenger_2.birth_date, 
                            "price"              : passenger_2.price, 
                            "reservation_id"     : passenger_2.reservation_id ,
                            "flight_schedule_id" : passenger_2.flight_schedule_id ,
                            "seat_id"            : passenger_2.seat_id
                        }
                    ]
                }
            
            expected_data = {      
                    'total_price' :80000 ,

                    "passenger_informations" : 
                    [
                        {
                            "first_name"         : "김", 
                            "last_name"          : "근성1",  
                            "gender"             : "남" , 
                            "email"              : "email1@naver.com", 
                            "birth_date"         : "1984.08.04", 
                            "price"              : 10000, 
                            "reservation_id"     : 1 ,
                            "flight_schedule_id" : 1,
                            "seat_id"            : 1
                        },
                        {
                            "first_name"         : "김", 
                            "last_name"          : "근성2",  
                            "gender"             : "여" , 
                            "email"              : "email2@naver.com", 
                            "birth_date"         : "1984.08.04", 
                            "price"              : 10000, 
                            "reservation_id"     : 1 ,
                            "flight_schedule_id" : 1,
                            "seat_id"            : 1
                        }
                    ]
                }  

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), {"message":'success'})
            self.assertEqual(saved_test_data, expected_data )
    
    def test_reservation_fail(self):  

            client = Client()                             
            
            data={      
                #'total_price' : 20000,  Cause KEYERROR
                "passenger_informations" : 
                [
                    {
                        "first_name"         : "김", 
                        "last_name"          : "근성1",  
                        "gender"             : "남" , 
                        "email"              : "email1@naver.com", 
                        "birth_date"         : "1984.08.04", 
                        "user_id"            : 1, 
                        "flight_schedule_id" : 1 ,
                        "seat_name"          : "이코노미"
                    },
                    {
                        "first_name"         : "김", 
                        "last_name"          : "근성2", 
                        "gender"             : "여" , 
                        "email"              : "email2@naver.com",
                        "birth_date"         : "1984.08.04",
                        "user_id"            : 1,
                        "flight_schedule_id" : 1 ,
                        "seat_name"          : "이코노미"
                    }
                ]
                    
                }
            
            access_token = jwt.encode({'user_id' : 1 }, SECRET_KEY, ALGORITHM)
     
            response     = client.post("/users/reservation",json.dumps(data), content_type='application/json' ,HTTP_Authorization = access_token)
                
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"message" : "KEYERROR"})
            
