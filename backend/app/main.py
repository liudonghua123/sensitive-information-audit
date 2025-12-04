from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
# Import all models to ensure they are registered
from app.db import models

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def init_db():
    from app.core.builtin_rules import BUILTIN_RULES
    from app.db.session import AsyncSessionLocal
    
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # For dev reset
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize built-in rules if they don't exist
    async with AsyncSessionLocal() as session:
        from sqlalchemy.future import select
        result = await session.execute(select(models.ScanRule).where(models.ScanRule.is_system == True))
        existing_rules = result.scalars().all()
        
        if len(existing_rules) == 0:
            # Add built-in rules
            for rule_data in BUILTIN_RULES:
                db_obj = models.ScanRule(**rule_data)
                session.add(db_obj)
            await session.commit()


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.api_v1.api import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files

# Ensure frontend/dist exists or handle it
static_dir = os.path.join(os.path.dirname(__file__), "public")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # API routes are already handled above
    if full_path.startswith("api"):
        return {"error": "Not found"}
    
    # Serve index.html for SPA
    if os.path.exists(static_dir):
        return FileResponse(os.path.join(static_dir, "index.html"))
    return {"message": "Frontend not built"}


