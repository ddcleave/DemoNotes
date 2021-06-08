from typing import Optional

from fastapi import FastAPI, Depends, status, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from src.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.dependencies import get_user

app = FastAPI()

app.include_router(api_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localtest.me:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
