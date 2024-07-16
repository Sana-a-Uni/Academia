import json
import os
import frappe
from frappe.utils import get_files_path

def after_install():

    # to add Transaction print format after install academia app

    # get the directory of the json file that have the print format
    current_dir = os.path.dirname(
        os.path.dirname(__file__)
    )

    json_file_path = os.path.join(
        current_dir, "templates/print_formats/transaction_print_format.json"
    )

    # Read the contents of the JSON file
    with open(json_file_path, 'r') as file:
        json_content = file.read()

    # Convert the JSON content to a dictionary
    json_data = json.loads(json_content)

    json_data["doctype"] = "Print Format"

    # Create the Print Format document
    print_format = frappe.get_doc(json_data)

    # Insert the Print Format document
    print_format.insert()