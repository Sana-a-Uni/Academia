import frappe
from datetime import datetime, timedelta



def format_timedelta(td):
    """Helper function to format a timedelta object into a string"""
    days, remainder = divmod(td.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"


def execute(filters=None):
    columns = [
        "Transaction", "Company", "Department","Start Time", "Is Complete", "Expected Time", "Real Difference"
    ]

    data = []

    my_filters = {"circular": 0, "docstatus": 1}
    
    if filters.filter_company:
        my_filters["start_with_company"] = filters.filter_company
    if filters.filter_department:
        my_filters["start_with_department"] = filters.filter_department

    # Fetch all relevant data
    transactions = frappe.db.get_all(
        "Transaction",
        filters=my_filters, 
        fields=["name", "start_with", "start_with_company", "start_with_department", "creation", "submit_time", "complete_time"],
        order_by="creation",
    )

    settings = frappe.get_all("Transaction Settings", fields=["company", "department", "completion_duration"])
    settings_map = {(setting.company, setting.department): setting.completion_duration for setting in settings}

    data = []
    for transaction in transactions:
        key = (transaction.start_with_company, transaction.start_with_department)
        if key in settings_map:
            completion_duration = settings_map[key]
            completion_timedelta = timedelta(seconds=float(completion_duration))
            submit_time = transaction.submit_time

            if transaction.complete_time:
                transaction_complete_time = transaction.complete_time
                difference_time = transaction_complete_time - submit_time
                is_complete = "Yes"
            else:
                difference_time = datetime.now() - submit_time
                is_complete = "No"

            if difference_time > completion_timedelta:
                expected_time = format_timedelta(completion_timedelta)
                real_time = format_timedelta(difference_time)
                data.append([
                    transaction.name,
                    transaction.start_with_company,
                    transaction.start_with_department,
                    submit_time.strftime("%d/%m/%y (%H:%M)"),
                    is_complete,
                    expected_time,
                    real_time,
                ])


    return columns, data