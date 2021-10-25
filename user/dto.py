from dataclasses import dataclass


@dataclass
class SignupDto():
    userid:str
    nickname:str
    password:str
    password_chk:str
    address:str
    address_detail:str


@dataclass 
class SigninDto():
    userid:str
    password:str
  

@dataclass 
class UpdateUserDto():
    image:str
    nickname:str
    address:str
    address_detail:str
    user_pk:str


@dataclass
class UpdateUserAddressDto():
    address:str
    address_detail:str
    user:int


@dataclass
class KakaoUserInforDto():
    client_id:str
    code:str
    client_uri:str
    redirect_uri:str
    client_secret:str
