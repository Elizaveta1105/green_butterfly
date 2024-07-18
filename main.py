import redis.asyncio as redis
from fastapi import FastAPI
from src.routes import auth, section, spending
from fastapi_limiter import FastAPILimiter
from src.config.config import config

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(section.router, prefix='/api')
app.include_router(spending.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"Hello": "World"}
