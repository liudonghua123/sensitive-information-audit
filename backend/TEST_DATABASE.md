# Test Database for Audit System

This SQLite database (`test_audit.db`) contains sample data with various types of sensitive information for testing the audit system.

## Database Schema

### Tables

1. **users**
   - id (INTEGER PRIMARY KEY)
   - username (TEXT)
   - email (TEXT)
   - phone (TEXT)
   - id_card (TEXT) - Chinese ID card numbers
   - bank_card (TEXT) - Bank card numbers
   - password (TEXT)
   - created_at (DATETIME)

2. **customers**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT)
   - email (TEXT)
   - mobile_phone (TEXT)
   - address (TEXT)
   - credit_card (TEXT) - Credit card numbers
   - ssn (TEXT) - US Social Security Numbers
   - notes (TEXT)

3. **transactions**
   - id (INTEGER PRIMARY KEY)
   - user_id (INTEGER)
   - amount (REAL)
   - card_number (TEXT)
   - transaction_date (DATETIME)
   - ip_address (TEXT)
   - description (TEXT)

## Sample Data

The database contains:
- 3 user records with Chinese phone numbers, ID cards, and bank cards
- 3 customer records with email addresses, credit cards, and SSNs
- 3 transaction records with card numbers and IP addresses

## How to Use

1. **Add Connection in the UI:**
   - Connection Name: `Test Audit DB`
   - Database Type: `SQLite`
   - Host / Path: `D:\code\python\sensitive-information-audit\backend\test_audit.db` (use your actual path)
   - Leave other fields empty for SQLite

2. **Test the Connection:**
   - Click "Test Connection" button to verify
   - Should show success message

3. **Run a Scan:**
   - Go to Tasks page
   - Click "New Scan"
   - Select the test database connection
   - Click "Start Scan"

4. **View Results:**
   - Wait for scan to complete
   - Click on the completed task
   - View detected sensitive information

## Expected Detections

The built-in rules should detect:
- ✅ Email addresses (in users and customers tables)
- ✅ Chinese mobile phone numbers (11 digits)
- ✅ Chinese ID card numbers (18 digits)
- ✅ Bank card numbers (16-19 digits)
- ✅ Credit card numbers (Visa/MasterCard/AmEx)
- ✅ SSN numbers (XXX-XX-XXXX format)
- ✅ IPv4 addresses
- ✅ Password keyword

## Regenerating the Database

If you need to recreate the database:

```bash
cd backend
sqlite3 test_audit.db ".read test_data.sql"
```

This will drop existing tables and recreate them with fresh sample data.
