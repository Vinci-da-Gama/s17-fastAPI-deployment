import sys

sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from Classes.models import UsersClass
from database import engine, SessionLocal, Base
from .auth import get_current_user, verify_password, get_password_hash
from RequestAndResponse.users import UserVerification
from annotated import db_annotated_dependency

users_string = "users"

router = APIRouter(
    prefix=f"/{users_string}",
    tags=[users_string],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}}
)

templates = Jinja2Templates(directory="templates")


@router.get("/edit-password", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
def edit_user_view(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user})


@router.post("/edit-password", response_class=HTMLResponse)
async def change_user_password(request: Request, db: db_annotated_dependency,
                               username: str = Form(...), password: str = Form(...),
                               password2: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(UsersClass) \
        .filter(UsersClass.id == user.get("id") and UsersClass.username == username).first()

    msg = "Invalid username or password"

    if user_data is not None:
        if user_data.username == username and verify_password(password, user_data.hashed_password):
            user_data.hashed_password = get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password update"

    return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user, "msg": msg})
