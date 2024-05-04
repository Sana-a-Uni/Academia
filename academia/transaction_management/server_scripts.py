import frappe

@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},
                                    )
    #frappe.msgprint(f"requirements {requirements}")
    

    return requirements