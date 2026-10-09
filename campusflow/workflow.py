ALLOWED_STATUSES = {"open", "in_progress", "resolved"}
PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def assign_ticket(tickets: list, ticket_id: str, staff_name: str) -> dict:
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name cannot be empty.")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name.strip()
            return ticket

    raise KeyError(f"Ticket ID '{ticket_id}' not found.")


def update_status(tickets: list, ticket_id: str, new_status: str) -> dict:
    clean_status = new_status.strip().lower() if isinstance(new_status, str) else ""
    if clean_status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status '{new_status}'. Allowed: open, in_progress, resolved.")

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            current_status = ticket["status"]

            if current_status == "resolved" and clean_status != "open":
                raise ValueError("Resolved tickets can only be modified by reopening to 'open'.")

            # Cannot move to in_progress if unassigned
            if clean_status == "in_progress" and not ticket["assigned_to"]:
                raise ValueError("Cannot move an unassigned ticket into 'in_progress'. Assign staff first.")

            ticket["status"] = clean_status
            return ticket

    raise KeyError(f"Ticket ID '{ticket_id}' not found.")


def get_work_queue(tickets: list) -> list:
    unresolved = [t for t in tickets if t["status"] != "resolved"]

    def sort_key(ticket):
        p_rank = PRIORITY_RANK.get(ticket["priority"], 99)
        raw_id = ticket["id"]
        num_id = int(raw_id[1:]) if raw_id.startswith("T") and raw_id[1:].isdigit() else 999999
        return (p_rank, num_id)

    return sorted(unresolved, key=sort_key)