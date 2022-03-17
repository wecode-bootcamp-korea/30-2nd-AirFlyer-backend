import requests, jwt , json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from users.models      import User 
from my_settings  import ALGORITHM, SECRET_KEY

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
