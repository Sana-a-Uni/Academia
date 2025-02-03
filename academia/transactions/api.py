import frappe

def get_allowed_employees():
    """Fetch employees that the current user is allowed to act on."""
    user = frappe.session.user

    # Get the Employee record for the current user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")

    if not employee:
        return []

    # Fetch all Employee Proxy records
    proxies = frappe.get_all("Employee Proxy", fields=["name", "employee"])

    allowed_employees = {employee}  # Use a set to avoid duplicates

    for proxy in proxies:
        # Fetch delegated employees (child table), using the correct field name
        delegated_employees = frappe.get_all(
            "Delegated Employees",  # Child table Doctype
            filters={"parent": proxy["name"]},  # Link to parent Employee Proxy
            fields=["delegated_employee"]  # Change to the correct field name
        )

        # Check if the current employee is in the delegated list
        for delegated in delegated_employees:
            if delegated["delegated_employee"] == employee:
                allowed_employees.add(proxy["employee"])  # Add main employee

    return list(allowed_employees)  # Convert set to list before returning


@frappe.whitelist()
def fetch_allowed_employees():
    """Public method that calls the reusable function"""
    return get_allowed_employees()
