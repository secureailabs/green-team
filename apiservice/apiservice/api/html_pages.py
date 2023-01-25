from api.authentication import get_current_user, get_password_hash
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.authentication import TokenData
from models.common import PyObjectId
from utils import background_couroutines

DB_COLLECTION_USERS = "users"
DB_COLLECTION_VIDEOS = "videos"
DB_COLLECTION_TEXTS = "texts"
router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get(path="/login", response_class=HTMLResponse)
async def html_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get(path="/profile/{user_id}", response_class=HTMLResponse)
async def html_profile(
    request: Request,
    user_id: str,
):
    return templates.TemplateResponse("profile.html", {"request": request, "id": user_id})


@router.get(path="/users", response_class=HTMLResponse)
async def html_all_users(
    request: Request,
):
    return templates.TemplateResponse("users.html", {"request": request})


@router.get(path="/register", response_class=HTMLResponse)
async def html_register_user(
    request: Request,
):
    return templates.TemplateResponse("register.html", {"request": request})
