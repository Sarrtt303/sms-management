def validate_phone_number(phone):
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))