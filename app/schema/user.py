from pydantic import BaseModel


class NewUser(BaseModel):
    userid: str
    passwd: str
    name : str
    email : str
    captcha: str