from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count
from users.models import *
from flights.models import *
from my_settings  import ALGORITHM, SECRET_KEY

import requests, jwt, json

class SocialSignIn(View):
    def get(self, request):
            access_token    = request.headers.get('Authorization')
            profile_request = requests.get( "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"},)

            profile_json   = profile_request.json()
            print(profile_json)
            kakao_id       = profile_json["id"]
            kakao_account  = profile_json["kakao_account"]
            kakao_nickname = kakao_account["profile"].get("nickname",'')     
            email          = kakao_account.get('email', 'not agreed')
            print(kakao_id)

            if not kakao_nickname:
                print("닉네임 없음")
                return JsonResponse({"message" : "Nickname not offerd"},status = 400)
                
            
            if User.objects.filter(kakao_id = kakao_id).exists():
                user = User.objects.get(kakao_id=kakao_id)
                token = jwt.encode({"user_id":user.id}, SECRET_KEY, ALGORITHM)
                print("ID 생성됨")
                return JsonResponse({"token": token},status = 200)

            else:
                User.objects.create(kakao_id = kakao_id, kakao_nickname=kakao_nickname , email = email)
                user = User.objects.get(kakao_id=kakao_id)
                token = jwt.encode({"user_id":user.kakao_id},SECRET_KEY, ALGORITHM)
                print("기존에 있음")
                return JsonResponse({"token":token},status=200)


        
