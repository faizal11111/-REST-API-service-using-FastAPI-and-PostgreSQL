from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine, Base
from .api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan, title="Showbay Assessment API")
app.include_router(router)
