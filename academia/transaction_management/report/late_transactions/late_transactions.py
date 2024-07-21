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

    my_filters = {}
    my_filters["circular"] = 0
    my_filters["docstatus"] = 1
    
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

    for transaction in transactions:
        
        if transaction.start_with_company and transaction.start_with_department:
            try:
                setting = frappe.get_doc(
                    "Transaction Settings", 
                    {"company": transaction.start_with_company, "department": transaction.start_with_department}
                )
                if setting:
                    completion_duration = setting.completion_duration
                    completion_timedelta = timedelta(seconds=float(completion_duration))
                
                    submit_time= transaction.submit_time

                    if transaction.complete_time:
                        transaction_complete_time = transaction.complete_time

                        difference_time = transaction_complete_time - submit_time 

                        if difference_time > completion_timedelta:
                            duration_exceeded = difference_time - completion_timedelta
                            expected_time = format_timedelta(completion_timedelta)
                            real_time = format_timedelta(difference_time)

                            data.append([
                                transaction.name,
                                transaction.start_with_company,
                                transaction.start_with_department,
                                transaction.submit_time.strftime("%d/%m/%y (%H:%M)"),
                                "Yes",
                                expected_time,
                                real_time,
                            ])
                    
                    else:
                        time_now = datetime.now()
                        difference_time = time_now - submit_time

                        if difference_time > completion_timedelta:
                            duration_exceeded = difference_time - completion_timedelta
                            expected_time = format_timedelta(completion_timedelta)
                            real_time = format_timedelta(difference_time)

                            data.append([
                                transaction.name,
                                transaction.start_with_company,
                                transaction.start_with_department,
                                transaction.submit_time.strftime("%d/%m/%y (%H:%M)"),
                                "No",
                                expected_time,
                                real_time,
                            ])
                else:
                    continue

            except frappe.DoesNotExistError:
                # Handle the case where the Transaction Settings document is not found
                continue

        else:
            continue

    return columns, data