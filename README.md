<h1>Todo List Manager</h2>

This is a Todo List Manager built with FastAPI, MongoDB, Jinja2 and htmx. Unlike many todo list app, this todo list manager is built with a calendar where anyone can add a todo in a specific (present or future) date. Also
todos can be editable and can be changed to any other date. Once a todo is deleted, it goes to archive list where it can be restored and set to any other date.

To run this app, you need to run this command:
python -m uvicorn api:app --reload

To run the application from docker container, use this command:
docker-compose up -d
