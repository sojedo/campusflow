def generate_reports(tickets: list) -> dict:
    report = {
        "total": len(tickets),
        "status_breakdown": {"open": 0, "in_progress": 0, "resolved": 0},
        "priority_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
    }

    for ticket in tickets:
        st = ticket.get("status")
        pr = ticket.get("priority")
        if st in report["status_breakdown"]:
            report["status_breakdown"][st] += 1
        if pr in report["priority_breakdown"]:
            report["priority_breakdown"][pr] += 1

    return report