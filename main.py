from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import RedirectResponse

from database import engine, Base
from routers import auth, todos, users

app = FastAPI()
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the correct origins in production to fix this error "Provisional headers are shown"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
