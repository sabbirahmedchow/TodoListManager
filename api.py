from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from db import save_todos, get_todo_list, delete_todo, get_archive_todos, get_datewise_todos

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")


# This is the main route to show the add todo page with the required parameters based on add, update or archive a todo.
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, date: str = None, q: str = None, todo_id: str = None):
    if q and not date:
        return templates.TemplateResponse("index.html", {"request": request, "q": q, "todo_id": todo_id})
    if q and date:
        return templates.TemplateResponse("index.html", {"request": request, "q": q, "date": str(date), "todo_id": todo_id})
    return templates.TemplateResponse("index.html", {"request": request})


# This route is to add the todos as well as update a todo.
@app.post("/add_todo", response_class=HTMLResponse)
async def add_todo(request: Request, todo: str = Form(...), todo_date: str = Form(...), todo_id: Optional[str] = Form(None)):
    try:
        save_todos(todo,todo_date,todo_id)
        if todo_id:
            return templates.TemplateResponse("confirm.html", {"request": request, "message": "Item updated succussfully.", "title": "Update Todo"})
        return templates.TemplateResponse("confirm.html", {"request": request, "message": "Item added succussfully.", "title": "Add Todo"})
    except Exception as e:
        return templates.TemplateResponse("confirm.html", {"request": request, "message": e})
    
# This troute is to fetch the todos when the todo list page is loaded.
@app.get("/get_todos", response_class=HTMLResponse)
async def get_todos(request: Request):
    try:
        todos = get_todo_list()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Todo List of Today", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e})

# This routes is to delete a todo which is basically change the status of a todo to list them as archived.
@app.delete("/delete_todo/{date}/{id}", response_class=HTMLResponse)   
async def update_todo(request: Request, date: str, id: str):
    try:
        todos = delete_todo(id, date)
        return templates.TemplateResponse("includes/card.html", {"request": request, "todos": todos, "title": f"Todo List of {date}", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("includes/card.html", {"request": request, "message": e})

# This route is to get the list of archived todos.
@app.get("/get_archive_todos", response_class=HTMLResponse)
async def get_archived_todos(request: Request):
    try:
        todos = get_archive_todos()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Archived Todos", "status": 0})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e}) 

# This route is to get the todos by date while selecting from the calendar in todo list.
@app.get("/get_todos_by_day", response_class=HTMLResponse) 
async def get_todos_by_date(request: Request, date: str = None):
    try:
        todos_by_date = get_datewise_todos(date)
        return templates.TemplateResponse("includes/card.html", {"request": request, "todos": todos_by_date, "title": f"Todo List of {date}", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("includes/card.html", {"request": request, "message": e})     
