![header](https://capsule-render.vercel.app/api?type=waving&color=#154D9E&height=100&section=header&fontSize=90)

![image](https://user-images.githubusercontent.com/67942847/160072501-22b71534-b425-43a3-9cba-8e5f5a381b40.png)


<br><br>

---
# Target site
![Uploading image.png…]()

* ## 사이트 소개  
    [Site Link](https://www.koreanair.com/kr/ko)
    
    AIR FLYER은 항성간 우주여행 예약을 제공하는사이트입니다. 
    대한항공의 UX,UI를 오마쥬 했습니다.


* ## 사이트 선정 이유
    * 프론트 입장에서 각종 외부 API를 이용해 볼 수 있다 (ex: 달력)
    * UI, UX 가 깔끔했다.
    * 예약기능을 구현해볼 수 있었다.

<br><br>

---
# 초기기획 & ERD

## ERD
![image](https://user-images.githubusercontent.com/67942847/160069065-059d796e-4c05-4232-bf81-a15bbfe97123.png)

## User flow
![image](https://user-images.githubusercontent.com/67942847/160069162-775f05c8-82e2-42e2-a0cb-bcf1df82fbfa.png)

## 초기기획 및 구현 목표
* 짧은 기간동안 기능구현에 집중해야하므로 일단 최소기능을 우선 구현하는 것으로 목표를 설정
* UI, UX 제외 개발은 초기세팅부터 전부 직접 구현
* 편도 기능만 구현
* 필수 구현 사항을 소셜로그인, 항공권 검색, 항공권 선택, 예약, 예약기록확인 5가지로 설정 
* 지정한 날짜에 따라 항공권을 필터링 하는 기능 구현 

<br><br>

---
# 개발기간 및 팀원

* ## 개발기간  
    2022.03.14 ~ 2022.03.25
   

* ## 개발인원 및 파트

    * Front-end  
        강성훈 - 항공권 선택
        김혜진 - 항공권 검색, 마이 페이지 (예약 내역 확인)
        안광민 - 소셜 로그인, 양식작성 및 예약
        
    * Back-end   
        김산   - 소셜 로그인, 양식작성 및 예약, 마이페이지
        안성준 -  항공권 검색, 항공권 선택

<br><br>

---
# 적용 기술 및 구현 기능

* ## 기술 스택
    * ### Front-end  
        <a href="#"><img src="https://img.shields.io/badge/HTML-DD4B25?style=plastic&logo=html&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/SASS-254BDD?style=plastic&logo=sass&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/javascript-EFD81D?style=plastic&logo=javascript&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/React-68D5F3?style=plastic&logo=react&logoColor=white"/></a>
    * ### Back-end  
        <a href="#"><img src="https://img.shields.io/badge/python-3873A9?style=plastic&logo=python&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Django-0B4B33?style=plastic&logo=django&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/MySQL-005E85?style=plastic&logo=mysql&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/AWS-FF9701?style=plastic&logo=aws&logoColor=white"/></a>
    <a href="#"><img src="https://img.shields.io/badge/bcrypt-525252?style=plastic&logo=bcrypt&logoColor=white"/></a>
     <a href="#"><img src="https://img.shields.io/badge/postman-F76934?style=plastic&logo=postman&logoColor=white"/></a>
    * ### Common  
        <a href="#"><img src="https://img.shields.io/badge/git-E84E32?style=plastic&logo=git&logoColor=white"/></a>
        <a href="#"><img src="https://img.shields.io/badge/RESTful API-415296?style=plastic&logoColor=white"/></a>
    * ### Communication  
        <a href="#"><img src="https://img.shields.io/badge/github-1B1E23?style=plastic&logo=github&logoColor=white"/></a>
        <a href="#"><img src="https://img.shields.io/badge/Slack-D91D57?style=plastic&logo=slack&logoColor=white"/></a>
        <a href="#"><img src="https://img.shields.io/badge/Trello-2580F7?style=plastic&logo=trello&logoColor=white"/></a>
        <a href="#"><img src="https://img.shields.io/badge/Notion-F7F7F7?style=plastic&logo=notion&logoColor=black"/></a>
* ## 구현기능
    * 소셜로그인
        - 카카오서버와 통신하여 인증발급
        - 비밀번호 암호화 및 JWT 발급
        - request.header에 담긴 token을 통해 로그인 여부를 검사
    * 우주항공권 검색
        - 날짜 API를 이용하여 자체 달력 구현
        - 목표 날짜, 시간, 예약할 인원을 선택하는 기능 구현
    * 우주항공권 선택
        - 판매 상품의 분류에 따라 filtering (q객체 사용)
        - 사용자가 원하는 기준에 따라 sorting
    * 예약 기능
        - 여권 관련 정보 입력
        - 일련의 과정에 원자성을 부여하기 위해 transaction 사용
    * 예약 히스토리 조회 기능
        - 유저의 과거 예약 목록을 반환하는 기능
        - ORM 최적화 적용
<br><br>

---
# API 기능정의서
[Link](https://docs.google.com/spreadsheets/d/1kHa1x7mvLLuju8vVcu1wyLGEOUIxxjmnMllO_YJFP1k/edit?usp=sharing)

<br><br>

---
# 시연 영상
https://www.youtube.com/watch?v=m-aGi9i54J0&feature=emb_logo

<br><br>
---
# Reference
* 이 프로젝트는 [대한항공](https://www.koreanair.com/kr/ko) 사이트를 참조하여 학습목적으로 만들었습니다.
* 실무수준의 프로젝트이지만 학습용으로 만들었기 떄문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
* 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다
* 이 프로젝트에서 사용하고 있는 로고와 배너는 해당 프로젝트 팀원 소유이므로 해당 프로젝트 외부인이 사용할 수 없습니다

![Footer](https://capsule-render.vercel.app/api?type=waving&color=#154D9E&height=100&section=footer)
