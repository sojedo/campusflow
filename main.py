
import os
from campusflow.tickets import create_ticket
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
    print("1. Create Ticket (F1)")
    print("2. List All / View Ticket (F2)")
    print("3. Assign Ticket (F3) [Pending Engineer B]")
    print("4. Update Status Workflow (F4) [Pending Engineer B]")
    print("5. View Work Queue (F5) [Pending Engineer B]")
    print("6. View Reports (F6) [Pending Engineer B]")
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

        if choice == "1":
            print("\n--- CREATE TICKET ---")
            title = input("Enter title: ")
            category = input("Enter category (Network/Hardware/Software/Other): ")
            urgency = input("Enter urgency (low/medium/high): ")
            users_in = input("Enter affected users count: ")

            try:
                users_cnt = int(users_in)
                ticket = create_ticket(title, category, urgency, users_cnt, tickets)
                tickets.append(ticket)
                save_tickets(STORAGE_FILE, tickets)
                print(f"\nSUCCESS: Ticket created with ID {ticket['id']} and Priority [{ticket['priority'].upper()}].")
            except ValueError as ve:
                print(f"\nERROR: {ve}")

        elif choice == "2":
            print("\n--- LIST / VIEW TICKETS ---")
            if not tickets:
                print("No tickets found.")
                continue

            sub = input("Type 'ALL' to list all, or enter specific Ticket ID (e.g. T001): ").strip()
            if sub.upper() == "ALL":
                for t in tickets:
                    display_ticket(t)
            else:
                found = next((t for t in tickets if t["id"].upper() == sub.upper()), None)
                if found:
                    display_ticket(found)
                else:
                    print(f"Ticket '{sub}' not found.")

        elif choice in ("3", "4", "5", "6"):
            print("\n[INFO] This option will be enabled after Engineer B merges their workflow features.")

        elif choice == "7":
            save_tickets(STORAGE_FILE, tickets)
            print("\nData saved. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please pick between 1 and 7.")


if __name__ == "__main__":
    main()

