# 2025 Vibe Coding Todo App

A modern, full-featured todo list application built with FastAPI and Databricks Lakebase integration. Features a beautiful, responsive UI with real-time task management.

## Technologies Used

- **FastAPI**: High-performance web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application  
- **Python-dotenv**: Environment variable management
- **Databricks SDK**: Integration with Databricks services and Lakebase
- **PostgreSQL**: Database backend via psycopg2
- **HTML5/CSS3**: Modern, responsive frontend design

## Features

### 🎯 Core Functionality

- **Create Tasks**: Add new todo items with title and description
- **Mark Complete**: Toggle task completion status with checkboxes
- **Edit Tasks**: Click any task to open detailed editing modal
- **Delete Tasks**: Remove tasks permanently
- **Tab Navigation**: Switch between "Active Tasks" and "All Tasks" views

### 🎨 User Experience

- **Dark Mode Design**: Sleek black gradient background with Databricks orange accents
- **Modern UI**: Clean card-based layout with smooth animations
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Real-time Updates**: Instant UI updates without page refreshes
- **Loading States**: Visual feedback during API operations
- **Error Handling**: User-friendly error messages and recovery

### 🔒 Data Security

- **Schema Isolation**: User-specific database schemas based on email
- **Email Derivation**: Automatic schema creation from user identity
- **Input Validation**: Client and server-side validation
- **XSS Protection**: HTML escaping for user-generated content

## Getting Started

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up environment variables:

    - Copy `example.env` to `.env`
    - Fill in your actual Databricks credentials:
        - `DATABRICKS_HOST`
        - `DATABRICKS_CLIENT_ID`
        - `DATABRICKS_CLIENT_SECRET`
        - `LAKEBASE_INSTANCE_NAME`
        - `LAKEBASE_DB_NAME`
        - `MY_EMAIL` (your email for schema derivation)

3. Run the application:

    ```bash
    python app.py
    ```

4. Open your browser to `http://localhost:8000`

## Deployment

This app is configured for deployment on Databricks Apps using the `app.yaml` configuration file.

### Databricks Apps Deployment

The app includes an `app.yaml` file that configures:
- **Command**: Runs the FastAPI app with uvicorn on port 8080
- **Environment Variables**: Automatically injects required Databricks and Lakebase configuration

When deployed to Databricks, the app will:
- Authenticate automatically using the workspace identity
- Connect to the configured Lakebase instance
- Use the `X-Forwarded-Email` header to identify users
- Create user-specific tables based on email addresses

### Security & Secrets Management

🔒 **Secure by Design**: This app uses Databricks workspace identity for authentication:
- No credentials stored in configuration files
- OAuth tokens generated automatically by the platform
- User authentication via `X-Forwarded-Email` header
- No `CLIENT_ID` or `CLIENT_SECRET` needed in deployment

**Environment Variables in app.yaml**:
- All values in `app.yaml` are non-sensitive configuration (URLs, instance names)
- Secrets are never stored in the yaml file

**If you need to store secrets**, use Databricks Secret Scopes:
```yaml
env:
  - name: MY_SECRET
    valueFrom:
      secretKeyRef:
        scope: my-secret-scope
        key: my-secret-key
```

## API Endpoints

### Todo Management

- `POST /api/todos` - Create a new todo item
- `GET /api/todos` - List todo items (with optional `include_completed` parameter)
- `GET /api/todos/{id}` - Get a specific todo item
- `PUT /api/todos/{id}` - Update a todo item
- `PUT /api/todos/{id}/status` - Change todo status
- `DELETE /api/todos/{id}` - Delete a todo item

### System

- `GET /health` - Health check endpoint

## Database Architecture

### Schema Derivation

The app automatically creates user-specific database schemas based on email addresses:

- Email: `john.doe@company.com` → Schema: `john_doe`
- Tables are created as `{schema}_lists`

### Connection Management

- **Singleton Pattern**: Efficient connection pooling with automatic token refresh
- **OAuth Integration**: Seamless Databricks authentication
- **Token Refresh**: Automatic renewal every 59 minutes
- **Connection Pooling**: Optimized database connections

### Security Considerations

⚠️ **SECURITY WARNING**: This demo uses f-string SQL queries for simplicity. In production, always use parameterized queries to prevent SQL injection attacks.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS <prefix>_lists (
    id serial primary key,
    user_email TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);
```

Where `<prefix>` is derived from the user's email (e.g., `john_doe` for `john.doe@company.com`).
