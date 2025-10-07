"""
Lists service for managing to-do items in Lakebase.

⚠️ SECURITY WARNING ⚠️
THIS CODE USES F-STRING SQL QUERIES INSTEAD OF PARAMETERIZED QUERIES.
THIS IS VULNERABLE TO SQL INJECTION ATTACKS AND SHOULD NOT BE USED IN PRODUCTION.
THIS IS ACCEPTABLE FOR THIS DEMO ONLY.
"""

from services.lakebase import Lakebase


def get_table_name(user_email: str) -> str:
    """Derive table name from user email"""
    email_lower = user_email.lower()
    prefix = email_lower.split('@')[0].replace('.', '_')
    return f"public.{prefix}_lists"


def create_todo(user_email: str, title: str, description: str):
    """
    Create a new to-do item
    
    Args:
        user_email: User's email address (will be lowercased)
        title: Title of the to-do item
        description: Description of the to-do item
        
    Returns:
        The created to-do item row
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    sql = f"""
        INSERT INTO {table_name} (user_email, title, description, status, created_at, updated_at)
        VALUES ('{email_lower}', '{title}', '{description}', 'pending', now(), now())
        RETURNING *;
    """
    
    rows = Lakebase.query(sql)
    return rows[0] if rows else None


def update_todo(user_email: str, todo_id: int, title: str, description: str):
    """
    Update a to-do item's title and description
    
    Args:
        user_email: User's email address (will be lowercased)
        todo_id: ID of the to-do item
        title: New title
        description: New description
        
    Returns:
        The updated to-do item row
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    sql = f"""
        UPDATE {table_name}
        SET title = '{title}', description = '{description}', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email_lower}'
        RETURNING *;
    """
    
    rows = Lakebase.query(sql)
    return rows[0] if rows else None


def change_status(user_email: str, todo_id: int, status: str):
    """
    Change the status of a to-do item
    
    Args:
        user_email: User's email address (will be lowercased)
        todo_id: ID of the to-do item
        status: New status (e.g., 'pending', 'completed', 'deleted')
        
    Returns:
        The updated to-do item row
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    sql = f"""
        UPDATE {table_name}
        SET status = '{status}', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email_lower}'
        RETURNING *;
    """
    
    rows = Lakebase.query(sql)
    return rows[0] if rows else None


def list_todos(user_email: str, include_completed: bool = False):
    """
    List to-do items for a user
    
    Args:
        user_email: User's email address (will be lowercased)
        include_completed: If True, include completed and deleted items
        
    Returns:
        List of to-do item rows
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    if include_completed:
        sql = f"""
            SELECT * FROM {table_name}
            WHERE user_email = '{email_lower}'
            ORDER BY created_at DESC;
        """
    else:
        sql = f"""
            SELECT * FROM {table_name}
            WHERE user_email = '{email_lower}' AND status != 'deleted'
            ORDER BY created_at DESC;
        """
    
    rows = Lakebase.query(sql)
    return rows


def delete_todo(user_email: str, todo_id: int):
    """
    Delete a to-do item (soft delete by marking as 'deleted')
    
    Args:
        user_email: User's email address (will be lowercased)
        todo_id: ID of the to-do item
        
    Returns:
        The deleted to-do item row
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    sql = f"""
        UPDATE {table_name}
        SET status = 'deleted', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email_lower}'
        RETURNING *;
    """
    
    rows = Lakebase.query(sql)
    return rows[0] if rows else None


def get_todo(user_email: str, todo_id: int):
    """
    Get a specific to-do item
    
    Args:
        user_email: User's email address (will be lowercased)
        todo_id: ID of the to-do item
        
    Returns:
        The to-do item row or None
    """
    email_lower = user_email.lower()
    table_name = get_table_name(email_lower)
    
    # ⚠️ USING F-STRING FOR SQL - NOT SAFE FOR PRODUCTION ⚠️
    sql = f"""
        SELECT * FROM {table_name}
        WHERE id = {todo_id} AND user_email = '{email_lower}';
    """
    
    rows = Lakebase.query(sql)
    return rows[0] if rows else None

