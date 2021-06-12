from dataclasses import dataclass


@dataclass
class SignupDto():
  userid:str
  nickname:str
  password:str
  password_chk:str


@dataclass 
class SigninDto():
  userid:str
  password:str
  
@dataclass 
class UpdateUserDto():
  image:str
  nickname:str
  user_pk:str