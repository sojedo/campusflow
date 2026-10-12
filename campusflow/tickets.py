"""
Handles input validation, string normalization, priority calculation, 
and unique ID generation for helpdesk tickets.
"""

def validate_ticket_input(title: str, category: str, urgency: str, affected_users: int) -> dict:
    """
    Validates data types, ranges, and contents. Normalizes string inputs.
    Raises Error for any invalid data.
    """
    if not isinstance(title, str):
        raise ValueError("Title must be a text string.")
    
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Title must not be blank.")

    if not isinstance(category, str):
        raise ValueError("Category must be a text string.")
        
    clean_category = category.strip().capitalize()
    allowed_categories = ["Network", "Hardware", "Software", "Other"]
    if clean_category not in allowed_categories:
        raise ValueError(f"Invalid category. Allowed: {', '.join(allowed_categories)}")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be a text string.")
        
    clean_urgency = urgency.strip().lower()
    allowed_urgencies = ["low", "medium", "high"]
    if clean_urgency not in allowed_urgencies:
        raise ValueError(f"Invalid urgency. Allowed: {', '.join(allowed_urgencies)}")

    
    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a whole integer number.")
        
    if affected_users <= 0:
        raise ValueError("Affected users must be a positive integer greater than zero.")

    return {
        "title": clean_title,
        "category": clean_category,
        "urgency": clean_urgency,
        "affected_users": affected_users
    }


def calculate_priority(urgency: str, affected_users: int) -> str:
    """
    Calculates ticket priority exactly per business rules in strict top-down order.
    Assumes inputs are already validated and normalized.
    """
    
    if urgency == "high" and affected_users >= 10:
        return "critical"
        
    
    elif urgency == "high" or affected_users >= 10:
        return "high"
        
    
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
        
    
    else:
        return "low"


def generate_next_id(existing_tickets):
    # Support both list and dictionary ticket stores
    if isinstance(existing_tickets, dict):
        ticket_ids = existing_tickets.keys()
    elif isinstance(existing_tickets, list):
        ticket_ids = [t.get("id") or t.get("ticket_id") for t in existing_tickets if isinstance(t, dict)]
    else:
        ticket_ids = []

    # Extract numbers from IDs like "TICK-001"
    ids = []
    for tid in ticket_ids:
        if tid and isinstance(tid, str) and "-" in tid:
            try:
                ids.append(int(tid.split("-")[-1]))
            except ValueError:
                pass
                
    next_num = max(ids, default=0) + 1
    return f"TICK-{next_num:03d}"


def create_ticket(existing_tickets: dict, title: str, category: str, urgency: str, affected_users: int) -> dict:
    """
    Coordinator Function: Runs validations, calculates the priority,
    creates a unique ID, and returns a fully initialized ticket record.
    """
    validated_data = validate_ticket_input(title, category, urgency, affected_users)
    
    priority = calculate_priority(validated_data["urgency"], validated_data["affected_users"])
    
    new_id = generate_next_id(existing_tickets)
    
    new_ticket = {
        "id": new_id,
        "title": validated_data["title"],
        "category": validated_data["category"],
        "urgency": validated_data["urgency"],
        "affected_users": validated_data["affected_users"],
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }
    
    return new_ticket
