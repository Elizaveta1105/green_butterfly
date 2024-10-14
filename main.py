import redis.asyncio as redis
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse

from src.routes import auth, section, spending, images
from fastapi_limiter import FastAPILimiter
from src.config.config import config
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import secrets

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(section.router, prefix='/api')
app.include_router(spending.router, prefix='/api')
app.include_router(images.router, prefix='/api')

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(16))


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, password=config.REDIS_PASSWORD, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
