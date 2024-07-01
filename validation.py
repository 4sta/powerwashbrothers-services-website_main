import re  # Module for validation

def validate_email(email):
    """Validate email format."""
    re_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(re_pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format."""
    re_pattern = r"^\+?\d{4,13}$"
    return re.match(re_pattern, phone) is not None

def validate_order_form(data):
    """Validate order form data."""
    required_fields = ['fullName', 'email', 'serviceType', 'workObjectDetails']
    for field in required_fields:
        if not data.get(field):
            return False, f"Field {field} is required."

    if not validate_email(data.get('email')):
        return False, "Invalid email format."

    if data.get('tel') and not validate_phone(data.get('tel')):
        return False, "Invalid phone number format."

    return True, ""