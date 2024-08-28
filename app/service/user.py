import requests
from sqlalchemy import insert, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.user import User


class UserService:
    @staticmethod
    def insert_user(db, user):
        try:
            stmt = insert(User).values(
                userid=user.userid, passwd=user.passwd,
                name=user.name, email=user.email)
            result = db.execute(stmt)
            db.flush()
            db.commit()
            return result

        except SQLAlchemyError as ex:
            print(f'▶▶▶ insert_member 오류발생: {str(ex)}')
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




