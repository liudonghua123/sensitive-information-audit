-- Migration script for RBAC tables

CREATE TABLE permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    code VARCHAR NOT NULL UNIQUE,
    description VARCHAR
);

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    description VARCHAR
);

CREATE TABLE role_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles (id),
    FOREIGN KEY (permission_id) REFERENCES permissions (id)
);

CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

-- Create indexes
CREATE INDEX ix_permissions_id ON permissions (id);
CREATE INDEX ix_permissions_name ON permissions (name);
CREATE INDEX ix_permissions_code ON permissions (code);
CREATE INDEX ix_roles_id ON roles (id);
CREATE INDEX ix_roles_name ON roles (name);

-- Seed initial data
-- Create Admin role
INSERT INTO roles (name, description) VALUES ('Admin', 'Administrator with full access');
INSERT INTO roles (name, description) VALUES ('User', 'Standard user with limited access');

-- Create Permissions
-- User Management
INSERT INTO permissions (name, code, description) VALUES ('View Users', 'user:read', 'View user list and details');
INSERT INTO permissions (name, code, description) VALUES ('Create Users', 'user:create', 'Create new users');
INSERT INTO permissions (name, code, description) VALUES ('Update Users', 'user:update', 'Update user details');
INSERT INTO permissions (name, code, description) VALUES ('Delete Users', 'user:delete', 'Delete users');
INSERT INTO permissions (name, code, description) VALUES ('Manage Roles', 'role:manage', 'Manage roles and permissions');

-- Task/Scan Management
INSERT INTO permissions (name, code, description) VALUES ('View Tasks', 'task:read', 'View scan tasks and results');
INSERT INTO permissions (name, code, description) VALUES ('Create Tasks', 'task:create', 'Create new scan tasks');

-- Connection Management
INSERT INTO permissions (name, code, description) VALUES ('View Connections', 'connection:read', 'View database connections');
INSERT INTO permissions (name, code, description) VALUES ('Manage Connections', 'connection:manage', 'Create, update, delete connections');

-- Assign all permissions to Admin role
INSERT INTO role_permissions (role_id, permission_id) 
SELECT (SELECT id FROM roles WHERE name = 'Admin'), id FROM permissions;

-- Assign basic permissions to User role
INSERT INTO role_permissions (role_id, permission_id)
SELECT (SELECT id FROM roles WHERE name = 'User'), id FROM permissions WHERE code IN ('task:read', 'task:create', 'connection:read');

-- Assign Admin role to existing superusers (assuming id 1 is superuser or we can check is_superuser)
-- For this migration, we'll just assign Admin role to the first user if they exist, typically the admin.
-- Better approach: Assign Admin role to all users where is_superuser is 1
INSERT INTO user_roles (user_id, role_id)
SELECT id, (SELECT id FROM roles WHERE name = 'Admin') FROM users WHERE is_superuser = 1;
