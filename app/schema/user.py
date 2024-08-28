from datetime import date

from pydantic import BaseModel


class NewUser(BaseModel):
    userid: str
    passwd: str
    name : str
    email : str
    captcha: str


class BusinessUser(BaseModel):
     business_id: str
     business_pwd: str
     business_name: str
     business_no : str
     captcha: str