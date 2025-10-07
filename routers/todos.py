import os
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from services import lists_service


router = APIRouter(prefix="/api/todos", tags=["todos"])


class TodoCreate(BaseModel):
    title: str
    description: str = ""


class TodoUpdate(BaseModel):
    title: str
    description: str = ""


class StatusChange(BaseModel):
    status: str


def get_user_email(request: Request) -> str:
    """Get user email from header or environment variable"""
    email = request.headers.get("X-Forwarded-Email") or os.getenv("MY_EMAIL")
    if not email:
        raise HTTPException(status_code=400, detail="User email not found")
    return email


@router.post("")
async def create_todo(todo: TodoCreate, request: Request):
    """Create a new to-do item"""
    try:
        user_email = get_user_email(request)
        result = lists_service.create_todo(user_email, todo.title, todo.description)
        return {"success": True, "todo": result}
    except Exception as e:
        return {"error": str(e)}


@router.get("")
async def list_todos(request: Request, include_completed: bool = False):
    """List to-do items"""
    try:
        user_email = get_user_email(request)
        todos = lists_service.list_todos(user_email, include_completed)
        return {"success": True, "todos": todos}
    except Exception as e:
        return {"error": str(e)}


@router.get("/{todo_id}")
async def get_todo(todo_id: int, request: Request):
    """Get a specific to-do item"""
    try:
        user_email = get_user_email(request)
        todo = lists_service.get_todo(user_email, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"success": True, "todo": todo}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate, request: Request):
    """Update a to-do item's title and description"""
    try:
        user_email = get_user_email(request)
        result = lists_service.update_todo(user_email, todo_id, todo.title, todo.description)
        if not result:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"success": True, "todo": result}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.put("/{todo_id}/status")
async def change_todo_status(todo_id: int, status_change: StatusChange, request: Request):
    """Change a to-do item's status"""
    try:
        user_email = get_user_email(request)
        result = lists_service.change_status(user_email, todo_id, status_change.status)
        if not result:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"success": True, "todo": result}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, request: Request):
    """Delete a to-do item (soft delete)"""
    try:
        user_email = get_user_email(request)
        result = lists_service.delete_todo(user_email, todo_id)
        if not result:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"success": True, "message": "Todo deleted"}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

