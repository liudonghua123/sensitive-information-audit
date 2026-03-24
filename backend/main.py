import uvicorn
import os
import webbrowser
import threading
import time
from app.core.config import settings

def open_browser():
    """Open browser after server starts."""
    time.sleep(1)  # Wait for server to start
    url = f"http://{settings.HOST}:{settings.PORT}"
    webbrowser.open(url)

def main():
    """Run the application for development."""
    host = os.getenv("HOST", settings.HOST)
    port = int(os.getenv("PORT", settings.PORT))

    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run("app.main:app", host=host, port=port, reload=os.getenv("DEBUG", "false").lower() == "true")

if __name__ == "__main__":
    main()
