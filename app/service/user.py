import requests
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.businessuser import BusinessUser
from app.model.user import User
from app.schema.user import NewBusinessUser


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
            print(f'▶▶▶ insert_member 오류발생: {str(ex)}')
            db.rollback()

    @staticmethod
    def insert_business_user(db: Session, business_user: NewBusinessUser):
        new_business_user = BusinessUser(
            business_id=business_user.business_id,
            business_pwd=business_user.business_pwd,
            business_name=business_user.business_name,
            business_email=business_user.business_email,
            business_phone=business_user.business_phone,
            business_birth=business_user.business_birth,
        )
        db.add(new_business_user)
        db.commit()
        return db.query(BusinessUser).filter(BusinessUser.business_id == business_user.business_id).first()

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