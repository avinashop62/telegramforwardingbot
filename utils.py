def validate_phone(phone):
    return phone.startswith("+") and phone[1:].isdigit() and len(phone) >= 10
