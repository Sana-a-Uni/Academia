import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    columns = [
        "Transaction", "Recipient", "Company", "Department", "Duration Exceeded", "Time Difference (Minutes)"
    ]

    data = []

    # Fetch all relevant data
    transactions = frappe.db.get_all("Transaction", fields=["name", "start_with", "start_with_company", "start_with_department"])
    redirected_actions = frappe.db.get_all("Transaction Action", filters={"type": "Redirected"}, fields=["transaction", "type", "owner", "from_company", "from_department", "creation"])
    actions = frappe.db.get_all("Transaction Action", fields=["transaction", "type", "owner", "from_company", "from_department", "creation"])
    settings = frappe.db.get_all("Transaction Settings", fields=["company", "department", "duration"])

    # Create a mapping of settings
    settings_map = {(s.company, s.department): s.duration for s in settings}

    for transaction in transactions:
        # Fetch all actions for the current transaction
        transaction_actions = [a for a in actions if a.transaction == transaction.name]

        # Group actions by recipient
        action_groups = {}
        for action in transaction_actions:
            if action.owner not in action_groups:
                action_groups[action.created_by] = []
            action_groups[action.created_by].append(action)

        # Process each group of actions per recipient
        for recipient, recipient_actions in action_groups.items():
            if recipient_actions:
                first_action = recipient_actions[0]
                subsequent_actions = recipient_actions[1:]
                for subsequent_action in subsequent_actions:
                    duration = settings_map.get((transaction.start_with_company, transaction.start_with_department), 0)
                    time_diff = subsequent_action.creation - first_action.creation
                    time_diff_minutes = int(time_diff.total_seconds() // 60)
                    duration_exceeded = time_diff > timedelta(seconds=duration)
                    data.append([
                        transaction.name,
                        recipient,
                        transaction.start_with_company,
                        transaction.start_with_department,
                        "Yes" if duration_exceeded else "No",
                        time_diff_minutes
                    ])

    return columns, data