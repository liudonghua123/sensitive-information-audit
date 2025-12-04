-- Test database for sensitive information audit
-- This database contains sample data with various types of sensitive information

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    id_card TEXT,
    bank_card TEXT,
    password TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    mobile_phone TEXT,
    address TEXT,
    credit_card TEXT,
    ssn TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    card_number TEXT,
    transaction_date DATETIME,
    ip_address TEXT,
    description TEXT
);

-- Insert sample data with sensitive information
INSERT INTO users (username, email, phone, id_card, bank_card, password) VALUES
('zhang_san', 'zhangsan@example.com', '13812345678', '110101199001011234', '6222021234567890123', 'password123'),
('li_si', 'lisi@test.com', '13987654321', '310101198505051234', '6228481234567890123', 'mypassword'),
('wang_wu', 'wangwu@demo.com', '15912345678', '440101199212121234', '6225881234567890123', 'secret123');

INSERT INTO customers (name, email, mobile_phone, address, credit_card, ssn, notes) VALUES
('John Doe', 'john.doe@email.com', '13611112222', '123 Main St, Beijing', '4532123456789012', '123-45-6789', 'VIP customer'),
('Jane Smith', 'jane.smith@mail.com', '13722223333', '456 Park Ave, Shanghai', '5412345678901234', '987-65-4321', 'Regular customer'),
('Bob Johnson', 'bob@example.org', '13833334444', '789 Lake Rd, Guangzhou', '378282246310005', '456-78-9012', 'New customer');

INSERT INTO transactions (user_id, amount, card_number, transaction_date, ip_address, description) VALUES
(1, 1500.50, '6222021234567890123', '2024-01-15 10:30:00', '192.168.1.100', 'Online purchase'),
(2, 2300.00, '6228481234567890123', '2024-01-16 14:20:00', '10.0.0.50', 'Transfer'),
(3, 500.75, '6225881234567890123', '2024-01-17 09:15:00', '172.16.0.10', 'Payment');
