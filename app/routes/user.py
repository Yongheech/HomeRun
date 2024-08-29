from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates

from dbfactory import get_db
from app.schema.user import NewUser
from app.service.user import UserService

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
async def joinok(user: NewUser, db: Session = Depends(get_db)):

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


@user_router.post('/check_userid', response_class=JSONResponse)
async def check_userid(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    userid = data.get('userid')

    try:
        if UserService.check_userid_exists(db, userid):
            return JSONResponse(content={'exists': True, 'message': '아이디가 이미 존재합니다.'})
        else:
            return JSONResponse(content={'exists': False, 'message': '사용 가능한 아이디입니다.'})
    except Exception as ex:
        print(f'▷▷▷ check_userid 오류 발생 : {str(ex)}')
        return JSONResponse(content={'exists': False, 'message': '오류가 발생했습니다.'})



@user_router.get('/login', response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse('/user/login.html', {'request': req})

@user_router.post('/login',response_class=HTMLResponse)
async def loginok(req: Request, db: Session = Depends(get_db)):
    data = await req.json() # 클라이언트가 보낸 데이터를 request 객체로 받음
    try:
        print('전송한 데이터: ' ,data)
        redirect_url = '/user/loginfail' # 로그인 실패시 loginfail 로 이동

        if UserService.login_member(db, data): # 로그인 성공시
            req.session['logined_uid'] = data.get('userid') # 세션에 아이디 저장하고
            redirect_url = '/user/test'

        return RedirectResponse(url=redirect_url, status_code=303)

    except Exception as ex:
        print(f'▷▷▷ loginok 오류 : {str(ex)}')
        return RedirectResponse(url='/user/error', status_code=303)


@user_router.get('/form', response_class=HTMLResponse)
async def form(req: Request):
    return templates.TemplateResponse('/user/form.html', {'request': req})


@user_router.get('/finds', response_class=HTMLResponse)
async def finds(req: Request):
    return templates.TemplateResponse('/user/finds.html', {'request': req})


@user_router.get('/error',response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('/user/error.html', {'request':req})


@user_router.get('/test',response_class=HTMLResponse)
async def test(req: Request):
    return templates.TemplateResponse('/user/test.html', {'request':req})