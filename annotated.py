from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

db_annotated_dependency = Annotated[Session, Depends(get_db)]
oauth2_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
# oauth2_token_dependency = Annotated[str, Depends(oauth2_bearer)]
