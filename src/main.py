from fastapi import (
    FastAPI,
    Request,
    status,
    Depends,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import database
from auth.router import router as auth_router
from auth.token import verify_access_token
from signals.router import router as signals_router
from config import settings

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI(docs_url="", openapi_url="")

app.include_router(auth_router)
app.include_router(signals_router)
app.mount('/static', StaticFiles(directory=settings.STATIC_PATH))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=settings.TEMPLATES_PATH)


@app.get('/', response_class=HTMLResponse, dependencies=[Depends(verify_access_token)])
async def get_root_page(request: Request):
    return templates.TemplateResponse('app.html', {"request": request})


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_error_handler(_, __):
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@app.on_event('startup')
async def on_startup():
    await database.create_tables()
