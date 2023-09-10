from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import save_todos, get_todo_list, delete_todo, get_archive_todos

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="template")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = None):
    if q:
        return templates.TemplateResponse("index.html", {"request": request, "q": q})
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/add_todo", response_class=HTMLResponse)
async def add_todo(request: Request, todo: str = Form(...), todo_date: str = Form(...)):
    try:
       save_todos(todo,todo_date)
       return templates.TemplateResponse("confirm.html", {"request": request, "message": "Item inserted succussfully."})
    except Exception as e:
       return templates.TemplateResponse("confirm.html", {"request": request, "message": e})
    
@app.get("/get_todos", response_class=HTMLResponse)
async def get_todos(request: Request):
    try:
        todos = get_todo_list()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "All Active Todos", "status": 1})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e})

@app.delete("/delete_todo/{id}", response_class=HTMLResponse)   
async def update_todo(request: Request, id: str):
    print(id)
    try:
        todos = delete_todo(id)
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e})

@app.get("/get_archive_todos", response_class=HTMLResponse)
async def get_archived_todos(request: Request):
    try:
        todos = get_archive_todos()
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Archived Todos", "status": 0})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e}) 

@app.get("/get_todos_by_day", response_class=HTMLResponse) 
async def get_todos_by_date(request: Request, q: str = None):
    try:
        todos_by_date = get_datewise_todos(q)
        return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos, "title": "Archived Todos", "status": 0})
    except Exception as e:
        return templates.TemplateResponse("todo_list.html", {"request": request, "message": e})     




       