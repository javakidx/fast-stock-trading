from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enums import Priority

    
class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=1, max_length=512, description='Name of the todo item')
    description: Optional[str] = Field(..., description='Description of the todo item')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo item')
    
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description='Unique identifier for the todo item')

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=1, max_length=512, description='Name of the todo item')
    description: Optional[str] = Field(None, description='Description of the todo item')
    priority: Optional[Priority] = Field(None, description='Priority of the todo item')

all_todos: List[Todo] = [
    Todo(todo_id=1, todo_name='Sports', description='Go to the gym', priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name='Chores', description='Clean the house', priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name='Reading', description='Finish the book', priority=Priority.HIGH),
    Todo(todo_id=4, todo_name='Shop', description='Go shopping', priority=Priority.LOW),
    Todo(todo_id=5, todo_name='Meditate', description='Meditate for 10 minutes', priority=Priority.MEDIUM)
]

class Stock(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10, description='Symbol of the stock')
    name: str = Field(..., min_length=1, max_length=100, description='Name of the stock')
    market_type: str = Field(..., min_length=1, max_length=100, description='Market type of the stock')
    industry: str = Field(..., min_length=1, max_length=50, description='Industry of the stock')
    issue_date: Optional[str] = Field(None, description='Issue date of the stock')
