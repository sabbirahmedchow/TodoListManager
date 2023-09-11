from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from db import save_todos, get_todo_list, delete_todo, get_archive_todos, get_datewise_todos

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, date: str = None, q: str = None):
    if q and not date:
        return templates.TemplateResponse("index.html", {"request": request, "q": q})
    if q and date:
        return templates.TemplateResponse("index.html", {"request": request, "q": q, "date": str(date)})
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add_todo", response_class=HTMLResponse)
async def add_todo(request: Request, todo: str = Form(...), todo_date: str = Form(...), todo_id: Optional[str] = Form(None)):
    print(todo_id)
    try:
       save_todos(todo,todo_date,todo_id)
       return templates.TemplateResponse("confirm.html", {"request": request, "message": "Item inserted succussfully."})
    except Exception as e:
       return templates.TemplateResponse("confirm.html", {"request": request, "message": e})
    
@app.get("/get_todos", response_class=HTMLResponse)
async def get_todos(request: Request):
    try:
        todos = get_todo_list()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Todo List of Today", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e})

@app.delete("/delete_todo/{date}/{id}", response_class=HTMLResponse)   
async def update_todo(request: Request, date: str, id: str):
    try:
        todos = delete_todo(id, date)
        return templates.TemplateResponse("includes/card.html", {"request": request, "todos": todos, "title": f"Todo List of {date}", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("includes/card.html", {"request": request, "message": e})

@app.get("/get_archive_todos", response_class=HTMLResponse)
async def get_archived_todos(request: Request):
    try:
        todos = get_archive_todos()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Archived Todos", "status": 0})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e}) 

@app.get("/get_todos_by_day", response_class=HTMLResponse) 
async def get_todos_by_date(request: Request, date: str = None):
    try:
        todos_by_date = get_datewise_todos(date)
        return templates.TemplateResponse("includes/card.html", {"request": request, "todos": todos_by_date, "title": f"Todo List of {date}", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("includes/card.html", {"request": request, "message": e})     




       