from fastapi import APIRouter
from app.api.api_v1.endpoints import login, users, connections, rules, tasks, roles

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(connections.router, prefix="/connections", tags=["connections"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])

