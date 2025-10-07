import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routers import todos
from services.lakebase import Lakebase

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Vibe Coding Todo App")

# Include routers
app.include_router(todos.router)

# Mount static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    try:
        return FileResponse("frontend/index.html")
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/setup-permissions")
async def setup_permissions(request: Request):
    """
    Setup database permissions for the user's table sequence.
    This should be called once after table creation.
    """
    try:
        # Get user email
        email = request.headers.get("X-Forwarded-Email") or os.getenv("MY_EMAIL")
        if not email:
            return {"error": "User email not found"}
        
        email_lower = email.lower()
        prefix = email_lower.split('@')[0].replace('.', '_')
        sequence_name = f"{prefix}_lists_id_seq"
        
        # Grant permissions on the sequence
        sql = f'GRANT USAGE, SELECT ON SEQUENCE {sequence_name} TO "2025_vibe_coding";'
        
        Lakebase.query(sql)
        
        return {
            "success": True,
            "message": f"Permissions granted on sequence {sequence_name}",
            "sequence": sequence_name
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

