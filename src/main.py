from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.router import api
from core.db import init_db

origins = [
    "http://localhost:9005"
]

app = FastAPI(
    title="Reviews",
    docs_url="/docs",
    openapi_url="/api/openapi.json",
    openapi_prefix="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api.router)

@app.on_event("startup")
def startup():
    init_db()