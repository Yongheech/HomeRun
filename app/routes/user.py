from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.schema.user import NewUser
from app.service.user import UserService
from dbfactory import get_db

user_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 로그인 페이지를 렌더링하는 라우터 정의
@user_router.get('/', response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('/user/mainlogin.html', {'request': req})


@user_router.get('/join', response_class=HTMLResponse)
async def join(req: Request):
    return templates.TemplateResponse('/user/join.html', {'request': req})


@user_router.post('/join', response_class=HTMLResponse)
async def joinok(user: NewUser, db:Session = Depends(get_db)):
    try:
        if UserService.check_captcha(user):
            print(user)
            result = UserService.insert_user(db, user)
            print('처리결과:', result.rowcount)

        if result.rowcount > 0:
            return RedirectResponse(url='/user/login', status_code = 303)

        else:
         return RedirectResponse(url='user/error', status_code=303)

    except Exception as ex:
     print(f'▷▷▷ joinok 오류 발생 : {str(ex)}')
    return RedirectResponse(url='/user/error', status_code=303)



@user_router.get('/login', response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse('/user/login.html', {'request': req})


@user_router.get('/form', response_class=HTMLResponse)
async def form(req: Request):
    return templates.TemplateResponse('/user/form.html', {'request': req})


@user_router.get('/finds', response_class=HTMLResponse)
async def finds(req: Request):
    return templates.TemplateResponse('/user/finds.html', {'request': req})