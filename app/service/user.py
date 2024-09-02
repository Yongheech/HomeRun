from datetime import date

import requests
from fastapi import Form
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.businessuser import BusinessUser
from app.model.user import User
from app.schema.user import NewBusinessUser, NewUser
from app.service.business_validation import validate_business_number


def get_user_data(
        userid: str = Form(...),
        passwd: str = Form(...),
        name: str = Form(...),
        email: str = Form(...),
        birth: date = Form(...),
        phone: str = Form(...),
        captcha: str = Form(...)
):
    return NewUser(
        userid=userid,
        passwd=passwd,
        name=name,
        email=email,
        birth=birth,
        phone=phone,
        captcha=captcha
    )

def get_business_user_data(
        business_id: str = Form(...),
        business_pwd: str = Form(...),
        business_name: str = Form(...),
        business_email: str = Form(...),
        business_phone: str = Form(...),
        business_birth: date = Form(...),
        business_uploadno: int = Form(...),
        captcha: str = Form(...)
):
    return NewBusinessUser(
        business_id=business_id,
        business_pwd=business_pwd,
        business_name=business_name,
        business_email=business_email,
        business_phone=business_phone,
        business_birth=business_birth,
        business_uploadno=business_uploadno,
        captcha=captcha
    )

class UserService:
    @staticmethod
    def insert_user(db, user):
        try:
            stmt = insert(User).values(
                userid=user.userid, passwd=user.passwd,
                name=user.name, email=user.email,
                birth=user.birth, phone = user.phone)
            result = db.execute(stmt)
            db.flush()
            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_user 오류발생: {str(ex)}')
            db.rollback()


    @staticmethod
    def insert_business_user(db: Session, business_user: NewBusinessUser):
        try:
            stmt = insert(BusinessUser).values(
                business_id=business_user.business_id,
                business_pwd=business_user.business_pwd,
                business_name=business_user.business_name,
                business_email=business_user.business_email,
                business_phone=business_user.business_phone,
                business_birth=business_user.business_birth,
                business_uploadno=business_user.business_uploadno
            )
            result = db.execute(stmt)
            db.commit()
            return result
        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_business_user 오류발생: {str(ex)}')
            db.rollback()



    @staticmethod
    def check_captcha(user):
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {
            'secret': '6LeKoCsqAAAAAOGQbslqQCwHU6shGBsPfmajiVh5',
            'response': user.captcha
        }

        res = requests.get(req_url, params=params)
        result = res.json()
        print('check => ', result)

        return result['success']

    @staticmethod
    def login_member(db, data):
        try:
            find_login = and_(User.userid == data.get('userid'),
                              User.passwd == data.get('passwd'))
            stmt = select(User.userid).where(find_login)
            result = db.execute(stmt).scalars().first()

            return result
        except SQLAlchemyError as ex:
            print(f' ▶▶▶ login_member 오류 발생 : {str(ex)}')
            db.rollback()
            return None


    @staticmethod
    def check_userid_exists(db, userid):
        try:
            stmt= select(User).where(User.userid == userid)
            result = db.execute(stmt).scalars().first()
            return result is not None # 아이디가 존재하면 True, 아니면 False 반환


        except SQLAlchemyError as ex:
            print(f'▶▶▶ check_userid_exists 오류 발생 : {str(ex)}')
            db.rollback()
            return False


    @staticmethod
    async def check_business_number(business_number: str) -> bool:
        try:
            result = await validate_business_number(business_number)
            # API 결과에 따라 'valid' 키가 존재할 경우 반환
            return result.get('valid', False)
        except Exception as ex:
            print(f'▷▷▷ check_business_number 오류 발생 : {str(ex)}')
            return False
