from typing import Optional

from fastapi import Request


class LoginFormClass:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form_values = await self.request.form()
        self.username = form_values.get("email")
        self.password = form_values.get("password")
