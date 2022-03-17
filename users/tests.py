import jwt,json

from django.test       import TestCase
from django.test       import Client
from unittest.mock     import patch, MagicMock

from users.models      import User
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

