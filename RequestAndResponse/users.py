from typing import Optional
from pydantic import Field, BaseModel, ConfigDict


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: Optional[str] = None
    first_name: str
    last_name: str
    password: str = Field(min_length=3)

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'username': 'UserName',
                'email': 'a@a.com',
                'first_name': "firstName",
                'last_name': "lastName",
                'password': "password",
            }
        }
    )

class UserVerification(BaseModel):
    username: str = Field(min_length=3)
    password: str
    new_password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                'username': 'UserName',
                'password': 'password',
                'new_password': 'new_password',
            }
        }
    )
