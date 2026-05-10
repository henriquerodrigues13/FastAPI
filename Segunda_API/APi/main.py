from contextlib import asynccontextmanager

from fastapi import FastAPI
from Segunda_API.APi.database import init_db
from Segunda_API.APi.routes import livros_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Segunda API", lifespan=lifespan)
app.include_router(livros_routes.router)

