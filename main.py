import os
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports
from campusflow.storage import load_tickets, save_tickets

STORAGE_FILE = os.path.join("data", "tickets.json")


def display_ticket(t: dict):
    assigned = t['assigned_to'] if t['assigned_to'] else 'Unassigned'
    print(f"[{t['id']}] {t['title']}")
    print(f"   Category: {t['category']} | Urgency: {t['urgency']} | Affected Users: {t['affected_users']}")
    print(f"   Priority: {t['priority'].upper()} | Status: {t['status']} | Assigned: {assigned}")
    print("-" * 65)


def print_menu():
    print("\n=================== CAMPUSFLOW CLI ===================")
    print("1. Create Ticket (F1) [Pending Engineer A]")
    print("2. List All / View Ticket (F2) [Pending Engineer A]")
    print("3. Assign Ticket (F3)")
    print("4. Update Status Workflow (F4)")
    print("5. View Work Queue (F5)")
    print("6. View Reports (F6)")
    print("7. Exit & Save (F7)")
    print("======================================================")


def main():
    try:
        tickets = load_tickets(STORAGE_FILE)
        print(f"Loaded {len(tickets)} tickets from {STORAGE_FILE}.")
    except Exception as e:
        print(f"Error loading tickets: {e}")
        tickets = []

    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice in ("1", "2"):
            print("\n[INFO] This option will be enabled after Engineer A merges their creation features.")

        elif choice == "3":
            print("\n--- ASSIGN TICKET ---")
            tid = input("Enter Ticket ID to assign: ").strip().upper()
            staff = input("Enter Staff Name: ").strip()
            try:
                ticket = assign_ticket(tickets, tid, staff)
                save_tickets(STORAGE_FILE, tickets)
                print(f"\nSUCCESS: Ticket {tid} assigned to '{ticket['assigned_to']}'.")
            except (KeyError, ValueError) as err:
                print(f"\nERROR: {err}")

        elif choice == "4":
            print("\n--- UPDATE STATUS ---")
            tid = input("Enter Ticket ID: ").strip().upper()
            st = input("Enter new status (open / in_progress / resolved): ").strip().lower()
            try:
                ticket = update_status(tickets, tid, st)
                save_tickets(STORAGE_FILE, tickets)
                print(f"\nSUCCESS: Ticket {tid} status updated to '{ticket['status']}'.")
            except (KeyError, ValueError) as err:
                print(f"\nERROR: {err}")

        elif choice == "5":
            print("\n--- WORK QUEUE (Sorted by Priority & ID) ---")
            queue = get_work_queue(tickets)
            if not queue:
                print("No unresolved tickets in queue.")
            else:
                for t in queue:
                    display_ticket(t)

        elif choice == "6":
            print("\n--- SYSTEM REPORT ---")
            report = generate_reports(tickets)
            print(f"Total Tickets: {report['total']}")
            print("Status Breakdown:")
            for k, v in report["status_breakdown"].items():
                print(f"  - {k}: {v}")
            print("Priority Breakdown:")
            for k, v in report["priority_breakdown"].items():
                print(f"  - {k}: {v}")

        elif choice == "7":
            save_tickets(STORAGE_FILE, tickets)
            print("\nData saved. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please pick between 1 and 7.")


if __name__ == "__main__":
    main()
