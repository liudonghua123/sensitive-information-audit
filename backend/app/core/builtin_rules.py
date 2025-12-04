"""Built-in scan rules for common sensitive data patterns"""

BUILTIN_RULES = [
    {
        "name": "Email Address",
        "rule_type": "regex",
        "content": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "description": "Detects email addresses",
        "is_system": True,
    },
    {
        "name": "Chinese Mobile Phone",
        "rule_type": "regex",
        "content": r"1[3-9]\d{9}",
        "description": "Detects Chinese mobile phone numbers (11 digits starting with 1)",
        "is_system": True,
    },
    {
        "name": "Chinese ID Card (18 digits)",
        "rule_type": "regex",
        "content": r"[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]",
        "description": "Detects Chinese 18-digit ID card numbers",
        "is_system": True,
    },
    {
        "name": "Chinese Bank Card",
        "rule_type": "regex",
        "content": r"\d{16,19}",
        "description": "Detects bank card numbers (16-19 digits)",
        "is_system": True,
    },
    {
        "name": "Credit Card (Visa/MasterCard/AmEx)",
        "rule_type": "regex",
        "content": r"(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})",
        "description": "Detects Visa, MasterCard, and American Express credit card numbers",
        "is_system": True,
    },
    {
        "name": "IPv4 Address",
        "rule_type": "regex",
        "content": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        "description": "Detects IPv4 addresses",
        "is_system": True,
    },
    {
        "name": "Social Security Number (SSN)",
        "rule_type": "regex",
        "content": r"\b\d{3}-\d{2}-\d{4}\b",
        "description": "Detects US Social Security Numbers (XXX-XX-XXXX format)",
        "is_system": True,
    },
    {
        "name": "URL/Website",
        "rule_type": "regex",
        "content": r"https?://[^\s]+",
        "description": "Detects HTTP/HTTPS URLs",
        "is_system": True,
    },
    {
        "name": "Password (keyword)",
        "rule_type": "keyword",
        "content": "password",
        "description": "Detects the keyword 'password'",
        "is_system": True,
    },
]
