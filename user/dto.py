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
  
