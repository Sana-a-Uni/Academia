from typing import Dict, Any,List
from datetime import datetime
import frappe

@frappe.whitelist(allow_guest=True)
def get_assignments_by_course(course_name: str="00", student_id: str="EDU-STU-2024-00001") -> Dict[str, Any]:
    try:
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Fetch assignments for the given course that are available to the student
        assignments: List[Dict[str, Any]] = frappe.get_all(
            "LMS Assignment",
            fields=['name', 'assignment_title', 'to_date'],
            filters={
                'course': course_name,
                'make_the_assignment_availability': 1,
                'from_date': ['<=', today]
            },
            order_by='from_date asc'
        )

        # Construct the response
        frappe.response.update({
            "status_code": 200,
            "message": "Assignments fetched successfully",
            "data": assignments
        })
        
        return frappe.response["message"]
    
    # Construct the error response
    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignments: {str(e)}"
        })
        
    return frappe.response["message"]
