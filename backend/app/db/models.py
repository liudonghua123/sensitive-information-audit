from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    roles = relationship("Role", secondary="user_roles", back_populates="users")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False) # e.g. "user:create"
    description = Column(String, nullable=True)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    permissions = relationship("Permission", secondary="role_permissions", backref="roles")
    users = relationship("User", secondary="user_roles", back_populates="roles")

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

class DbType(str, enum.Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    ORACLE = "oracle"

class DbConnection(Base):
    __tablename__ = "db_connections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    db_type = Column(String, nullable=False) # Store as string, validate with enum in Pydantic
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    password_encrypted = Column(String, nullable=True) # Simple encryption
    db_name = Column(String, nullable=True)
    
    tasks = relationship("ScanTask", back_populates="connection")

class RuleType(str, enum.Enum):
    REGEX = "regex"
    KEYWORD = "keyword"

class ScanRule(Base):
    __tablename__ = "scan_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    rule_type = Column(String, nullable=False, default=RuleType.REGEX)
    content = Column(Text, nullable=False) # The regex or keyword
    is_system = Column(Boolean, default=False) # Built-in rules
    description = Column(String, nullable=True)

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ScanTask(Base):
    __tablename__ = "scan_tasks"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("db_connections.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, default=TaskStatus.PENDING)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    summary = Column(Text, nullable=True) # Error messages
    selected_tables = Column(Text, nullable=True) # JSON array of table names
    scan_summary = Column(Text, nullable=True) # JSON summary statistics
    selected_rules = Column(Text, nullable=True) # JSON array of rule IDs to use
    
    connection = relationship("DbConnection", back_populates="tasks")
    results = relationship("ScanResult", back_populates="task")

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("scan_tasks.id"))
    table_name = Column(String, nullable=False)
    column_name = Column(String, nullable=False)
    sensitive_content_masked = Column(String, nullable=True) # Masked value
    rule_name = Column(String, nullable=True) # Name of the rule matched

    task = relationship("ScanTask", back_populates="results")


class LogLevel(str, enum.Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False, default=LogLevel.INFO)
    action = Column(String, nullable=False) # e.g., "user_login", "task_created", "scan_executed"
    message = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    target_type = Column(String, nullable=True) # e.g., "task", "connection", "user"
    target_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True) # JSON for extra details like SQL executed
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
