import uvicorn
import os
from app.main import app # For pyinstaller to find the app instance

def main():
    """Run the application for development."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=os.getenv("DEBUG", "false").lower() == "true")

if __name__ == "__main__":
    main()
