from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.db.models import DbType, RuleType, TaskStatus

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None

# User
class UserBase(BaseModel):
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str
    role_ids: List[int] = []

class UserUpdate(UserBase):
    password: Optional[str] = None
    role_ids: Optional[List[int]] = None

class User(UserBase):
    id: int
    roles: List['Role'] = []
    class Config:
        from_attributes = True

# Permission
class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class Permission(PermissionBase):
    id: int
    class Config:
        from_attributes = True

# Role
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class Role(RoleBase):
    id: int
    permissions: List[Permission] = []
    class Config:
        from_attributes = True

# Update forward references
User.model_rebuild()

# Connection
class ConnectionBase(BaseModel):
    name: str
    db_type: DbType
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    db_name: Optional[str] = None

class ConnectionCreate(ConnectionBase):
    password: Optional[str] = None

class ConnectionTest(ConnectionCreate):
    id: Optional[int] = None

class ConnectionUpdate(ConnectionBase):
    password: Optional[str] = None

class Connection(ConnectionBase):
    id: int
    # password is not returned
    class Config:
        from_attributes = True

# Rule
class RuleBase(BaseModel):
    name: str
    rule_type: RuleType
    content: str
    description: Optional[str] = None
    is_system: Optional[bool] = False

class RuleCreate(RuleBase):
    pass

class RuleUpdate(RuleBase):
    pass

class Rule(RuleBase):
    id: int
    class Config:
        from_attributes = True

# Task
class TaskBase(BaseModel):
    connection_id: int

class TaskCreate(TaskBase):
    table_names: Optional[List[str]] = None
    rule_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    summary: Optional[str] = None
    selected_tables: Optional[str] = None
    scan_summary: Optional[str] = None
    selected_rules: Optional[str] = None
    class Config:
        from_attributes = True

# Result
class ResultBase(BaseModel):
    table_name: str
    column_name: str
    sensitive_content_masked: Optional[str] = None
    rule_name: Optional[str] = None

class Result(ResultBase):
    id: int
    task_id: int
    class Config:
        from_attributes = True

# Database Metadata
class ColumnMetadata(BaseModel):
    name: str
    type: str
    nullable: bool

class TableMetadata(BaseModel):
    name: str
    type: str  # 'table' or 'view'
    row_count: Optional[int] = None
    size_bytes: Optional[int] = None
    columns: List[ColumnMetadata] = []

class DatabaseMetadata(BaseModel):
    tables: List[TableMetadata]
