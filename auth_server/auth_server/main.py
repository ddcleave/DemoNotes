from fastapi import FastAPI
from auth_server.api.api import api_router
from auth_server.db.database import database
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(api_router)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localtest.me:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
