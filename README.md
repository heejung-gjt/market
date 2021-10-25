# market v2.0

![블루 우드](https://user-images.githubusercontent.com/64240637/136060285-08c6a17f-bdd3-4afc-a57e-ae4fce92183c.png)


<br>

## 목차 | Contents
1. [감자마켓 소개](https://github.com/heejung-gjt/market#-%EA%B0%90%EC%9E%90%EB%A7%88%EC%BC%93-%EC%86%8C%EA%B0%9C)      
2. [개요](https://github.com/heejung-gjt/market#-%EA%B0%9C%EC%9A%94)    
3. [개발환경 및 기술스택](https://github.com/heejung-gjt/market#%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-%EB%B0%8F-%EA%B8%B0%EC%88%A0%EC%8A%A4%ED%83%9D)     
4. [Sequence Diagram](https://github.com/heejung-gjt/market#sequence-diagram)    
5. [주요 기능](https://github.com/heejung-gjt/market#%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5)    
6. [ERD](https://github.com/heejung-gjt/market#erd)     
7. [History](https://github.com/heejung-gjt/market#history)     

<br>

## 📚 감자마켓 소개

__자신이 가지고 있는 제품들을 사고 팔 수 있는 웹 사이트입니다.__    
<br>
장고의 기본적인 CRUD와 다양한 기능을 구현해보기 위해서 중고 쇼핑몰 사이트를 선택했습니다. 실제 유저가 사용할 수 있는 완성도로 개발하기 위해 여전히 진행중에 있습니다. 

<br>

## 📌 개요

- 기간 : 2021.06.03 ~ 
- 팀원
  - Back-end & Front-end : [손희정](https://github.com/heejung-gjt)
  - 개인 프로젝트로 진행하였습니다.   

<br>

## 개발환경 및 기술스택

|종류|이름|
|---|---|
|IDE|Visual Studio Code|
|OS|Ubuntu20.04|

<br>

|Stack|Role|
|---|---|
|HTML|프론트 구현|
|CSS|프론트 구현|
|JavaScript|프론트 구현, Ajax요청|
|Django 3.2.6|프레임워크|
|Ajax|좋아요, 댓글등 비동기처리|
|OAuth|회원가입|
|ORM|DB조작, 관리|
|AWS RDS|데이터베이스|
|AWS S3|이미지 저장공간|
|AWS 53|DNS서비스|


<br>

## Sequence Diagram
<!-- <p align="center"><img src="https://user-images.githubusercontent.com/64240637/134929474-c0e39c91-fcb8-49b2-8462-bc47d4ce71b9.png" width=600 height=500></p> -->
<img src="https://user-images.githubusercontent.com/64240637/134929474-c0e39c91-fcb8-49b2-8462-bc47d4ce71b9.png"></p>

<br>

## 주요 기능
> __테스트ID: test1@test1.com, 테스트PWD: test1__   

- ### user 기능
  - 로그인/회원가입 기능
  - 프로필기능(사용자 정보 수정 가능, 내가 쓴 글, 찜 한 제품 보기)      
  
<br>

###### ▶️ 카카오 로그인
![카카오회원가입](https://user-images.githubusercontent.com/64240637/135295714-7bbb44be-9e60-4516-906c-d1efd1a7ee68.gif)    

<br>

- ### product 기능
  - 제품 업로드 기능(카테고리별 선택, 제품가격, 제품의 정가와 판매가 비교)
  - 제품 업데이트 기능(내용변경, 가격조정)
  - 제품 삭제기능
  
<br>

 ###### ▶️ 제품 업로드
 
![이미지업로드](https://user-images.githubusercontent.com/64240637/135295689-b66df4e8-b0cb-4b42-82c3-29e752c830cd.gif)     

<br>

 ###### ▶️ 제품 수정
![이미지수정](https://user-images.githubusercontent.com/64240637/135295668-78519fe3-2114-41e2-9617-b8314649b895.gif) 

<br>

 ###### ▶️ 제품 검색
![검색](https://user-images.githubusercontent.com/64240637/135297654-e5edc9b0-3abe-4062-addd-88e1b6674beb.gif)

<br>

- ### menubar 기능
  - 제품 전체보기(찜한 순, 댓글 많은 순, 내가 작성한 글 필터)
  - 제품 카테고리별 보기(세부 카테고리 필터)   

<br>

 ###### ▶️ 모든제품 필터 기능
![이미지필터링하기](https://user-images.githubusercontent.com/64240637/135295730-e7ef8b57-b457-4d8a-ab64-5bbcd02736c7.gif)   


<br>

 ###### ▶️ 카테고리별 필터 기능
![카테고리필터](https://user-images.githubusercontent.com/64240637/135295710-3b591929-91da-4b82-8059-b0487c501d93.gif) 

- ### social 기능
  - 댓글/대댓글(수정,삭제)    
  - 찜 기능   

<br>

###### ▶️ 찜한 제품

![찜한제품](https://user-images.githubusercontent.com/64240637/135295663-3c2b8e7e-0e5b-4010-ad80-cc0d0605f53a.gif)   

<br>

###### ▶️ 댓글/대댓글

![대댓글](https://user-images.githubusercontent.com/64240637/135299562-bbc7c7fa-31aa-4372-8157-bff0b6f337d2.gif)


<br>

## ERD
<!-- <p align="center"><img src="https://user-images.githubusercontent.com/64240637/134930266-fc5ddc21-ce41-485b-9d33-3553fb4f7bbd.png" width=600 height=500></p> -->
<img src="https://user-images.githubusercontent.com/64240637/134930266-fc5ddc21-ce41-485b-9d33-3553fb4f7bbd.png">


<br>

## History

### [WIKI](https://github.com/heejung-gjt/market/wiki)

[v1.0](https://github.com/heejung-gjt/market/wiki/v1.0)    
[v2.0](https://github.com/heejung-gjt/market/wiki/v2.0)   
