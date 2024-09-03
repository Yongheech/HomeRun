from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from app.schema.user import NewUser
from app.service.user import UserService
from app.service.business_validation import validate_business_number
from dbfactory import get_db

user_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 메인 페이지
@user_router.get('/', response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('/user/mainlogin.html', {'request': req})

# 가입 페이지
@user_router.get('/join', response_class=HTMLResponse)
async def join(req: Request):
    return templates.TemplateResponse('/user/join.html', {'request': req})


@user_router.post('/join', response_class=HTMLResponse)
async def joinok(user: NewUser, db: Session = Depends(get_db)):

    try:
        if UserService.check_captcha(user):
            if user.business_id:  # 비즈니스 사용자 처리
                result = UserService.insert_business_user(db, user)
            else:  # 일반 사용자 처리
                result = UserService.insert_user(db, user)

            if result is not None and result.rowcount > 0:
                return RedirectResponse(url='/user/login', status_code=303)
            else:
                print("Database insert operation failed or no rows affected.")
                return RedirectResponse(url='/user/error', status_code=303)
        else:
            return RedirectResponse(url='/user/error', status_code=303)

    except Exception as ex:
        print(f'▷▷▷ joinok 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/user/error', status_code=303)

@user_router.post('/business_join', response_class=HTMLResponse)
async def businessjoinok(user: NewUser, db: Session = Depends(get_db)):

    try:
        if UserService.check_captcha(user):
            result = UserService.insert_business_user(db, user)

            if result is not None and result.rowcount > 0:
                return RedirectResponse(url='/user/login', status_code=303)
            else:
                print("Database insert operation failed or no rows affected.")
                return RedirectResponse(url='/user/error', status_code=303)
        else:
            return RedirectResponse(url='/user/error', status_code=303)

    except Exception as ex:
        print(f'▷▷▷ businessjoinok 오류 발생 : {str(ex)}')
        return RedirectResponse(url='/user/error', status_code=303)



@user_router.post('/check_business_number', response_class=JSONResponse)
async def check_business_number(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    business_number = data.get('businessNumber')

    try:
        # 자체 유효성 검사 호출
        is_valid = UserService.check_business_number(business_number)

        if is_valid:
            return JSONResponse(content={'valid': True, 'message': '유효한 사업자 번호입니다.'})
        else:
            return JSONResponse(content={'valid': False, 'message': '유효하지 않은 사업자 번호입니다.'})

    except Exception as ex:
        print(f'▷▷▷ check_business_number 오류 발생 : {str(ex)}')
        return JSONResponse(content={'valid': False, 'message': '오류가 발생했습니다.'})

# 사용자 아이디 중복 체크
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

# 로그인 페이지
@user_router.get('/login', response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse('/user/login.html', {'request': req})

# 로그인 처리
@user_router.post('/login', response_class=HTMLResponse)
async def loginok(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    try:
        print('전송한 데이터: ', data)
        redirect_url = '/user/loginfail'

        if UserService.login_member(db, data):
            req.session['logined_uid'] = data.get('userid')
            redirect_url = '/user/test'

        return RedirectResponse(url=redirect_url, status_code=303)

    except Exception as ex:
        print(f'▷▷▷ loginok 오류 : {str(ex)}')
        return RedirectResponse(url='/user/error', status_code=303)

# 폼 페이지
@user_router.get('/form', response_class=HTMLResponse)
async def form(req: Request):
    return templates.TemplateResponse('/user/form.html', {'request': req})

# 찾기 페이지
@user_router.get('/finds', response_class=HTMLResponse)
async def finds(req: Request):
    return templates.TemplateResponse('/user/finds.html', {'request': req})

# 오류 페이지
@user_router.get('/error', response_class=HTMLResponse)
async def error(req: Request):
    return templates.TemplateResponse('/user/error.html', {'request': req})

# 테스트 페이지
@user_router.get('/test', response_class=HTMLResponse)
async def test(req: Request):
    return templates.TemplateResponse('/user/test.html', {'request': req})

