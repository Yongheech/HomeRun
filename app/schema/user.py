from datetime import date

from pydantic import BaseModel


class NewUser(BaseModel):
    userid: str
    passwd: str
    name : str
    email : str
    birth : date
    phone : str
    captcha: str

class NewBusinessUser(BaseModel):
    business_id: str
    business_pwd: str
    business_name: str
    business_email: str
    business_phone: str
    business_birth: date
    business_uploadno: int
