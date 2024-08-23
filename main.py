from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


from app.routes.user import user_router, templates

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key='20240822110005')

templates = Jinja2Templates(directory="views/templates") # jinja2 설정
app.mount('/static', StaticFiles(directory='views/static'), name='static')

app.include_router(user_router,prefix='/user')

@app.get("/",response_class=HTMLResponse)
async def index(req:Request):
    return templates.TemplateResponse('/user/loginselect.html',{'request':req})




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)