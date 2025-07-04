from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from models import all_todos, Todo, TodoCreate, TodoUpdate
from typing import List
from router import stock_routers

from repository import database
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

REQUEST_COUNT = Counter('app_request_total', 'Total Request Count', ['method', 'url'])
EXCEPTION_COUNT = Counter('app_exception_total', 'Total number of unhandled exceptions', ['url', 'exception_type'])
app.include_router(stock_routers.router)


@app.exception_handler(Exception)
async def catch_all(request: Request, e: Exception):
    EXCEPTION_COUNT.labels(url=request.url, exception_type=type(e).__name__).inc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(e).__name__}
    )

@app.get('/db-connection')
def db_connect_test():
    inserted_id = database.insert_one()
    return {'info': str(inserted_id)}

# @app.middleware("http")
# def count_request(request: Request):
#     REQUEST_COUNT.labels(method=request.method, url=request.url).inc()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.get("/todos")
def get_all_todos(first_n: int | None = None, response_model=List[Todo]):
    if first_n:
        return all_todos[:first_n]
    return {"result": all_todos}


@app.post("/todos")
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        description=todo.description,
        priority=todo.priority
    )
    all_todos.append(new_todo)

    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if todo_update.todo_name is not None:
                todo.todo_name = todo_update.todo_name
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for i, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            all_todos.pop(i)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get('/errors')
def raise_errors():
    raise Exception()