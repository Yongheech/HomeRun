from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


user_router = APIRouter()
templates = Jinja2Templates(directory='views/templates')

# 로그인 페이지를 렌더링하는 라우터 정의
@user_router.get('/join', response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse('/user/join.html', {'request': req})

@user_router.get('/join', response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse('/user/login.html', {'request': req})
        try:
            if userService.check_

