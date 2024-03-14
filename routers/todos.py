import sys

sys.path.append("..")
from fastapi import Depends, HTTPException, APIRouter, Request, Form, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from Classes.models import TodosClass
from .auth import get_current_user
from annotated import get_db, db_annotated_dependency

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

# It it just to test each static html file
"""
@router.get("/test-template")
async def test_tmpl(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
"""


def redirect_to_todos_home():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: db_annotated_dependency):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todos = db.query(TodosClass).filter(TodosClass.owner_id == user.get('id')).all()
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


# db type could be {Session = Depends(get_db)} OR {db_annotated_dependency}
# why every route function must pass request, because Jinja2 requires it
@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    new_todo = TodosClass()
    new_todo.title = title
    new_todo.description = description
    new_todo.priority = priority
    new_todo.complete = False
    new_todo.owner_id = user.get("id")

    db.add(new_todo)
    db.commit()

    return redirect_to_todos_home()


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_by_id(request: Request, todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    aimed_todo = db.query(TodosClass).filter(TodosClass.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": aimed_todo, "user": user})


# why use post, not put?
# why edit-todo.html form method is post?
# because Jinja2 html form only have 2 method GET and POST
# even delete will use GET
@router.post("/edit-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT,
             response_class=HTMLResponse)
async def edit_todo_by_id_post(request: Request, todo_id: int = Path(gt=0),
                               title: str = Form(...), description: str = Form(...),
                               priority: int = Form(...),
                               db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    existing_todo = db.query(TodosClass).filter(TodosClass.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    existing_todo.title = title
    existing_todo.description = description
    existing_todo.priority = priority

    db.add(existing_todo)
    db.commit()

    return redirect_to_todos_home()


@router.get("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(request: Request, db: db_annotated_dependency,
                            todo_id: int = Path(gt=0)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    existing_todo = db.query(TodosClass).filter(TodosClass.id == todo_id) \
        .filter(TodosClass.owner_id == user.get("id")).first()
    if existing_todo is None:
        return redirect_to_todos_home()

    db.query(TodosClass).filter(TodosClass.id == todo_id).delete()
    db.commit()

    return redirect_to_todos_home()


@router.get("/complete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def complete_todo_by_id(request: Request, db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    existing_todo = db.query(TodosClass).filter(TodosClass.id == todo_id).first()
    existing_todo.complete = not existing_todo.complete

    db.add(existing_todo)
    db.commit()
    return redirect_to_todos_home()
