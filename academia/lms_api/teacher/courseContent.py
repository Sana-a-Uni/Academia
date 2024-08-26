import frappe
import json
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_course_content_summary(course_name="DS-2024-04-08", course_type="Lab"):
    try:
        # Get the current user ID from the session
        user_id = frappe.session.user
        # Retrieve faculty member ID
        faculty_member_id = get_faculty_member_from_user(user_id)
        
        # Fetch course contents based on filters
        course_contents = frappe.get_all("Course Content", filters={
            'course': course_name,
            'course_type': course_type,
            'faculty_member': faculty_member_id
        }, fields=["name", "title"])

        # Prepare the response list
        course_content_list = []

        for content in course_contents:
            course_content_list.append({
                "name": content.name,
                "title": content.title
            })

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Course content summary fetched successfully",
            "data": course_content_list
        })
        return frappe.response["message"]

    except Exception as e:
        frappe.log_error(message=f"An error occurred while fetching course content summary: {str(e)}", title="Course Content Summary Fetch Error")
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching course content summary: {str(e)}"
        })
        return frappe.response["message"]

@frappe.whitelist(allow_guest=True)
def add_course_content():
    user_id = frappe.session.user  # Get the current user ID from the session
    faculty_member_id = get_faculty_member_from_user(user_id)  # Retrieve faculty member ID
    data = json.loads(frappe.request.data)
    
    try:
        content_doc = frappe.get_doc({
            'doctype': 'Course Content',
            'title': data.get('title'),
            'topic': data.get('topic'),
            'faculty_member': faculty_member_id,
            'course': data.get('course'),
            'course_type': data.get('course_type')
        })
        content_doc.insert()

        attachments = data.get('attachments')
        if attachments:
            for attachment in attachments:
                attachment_content = attachment.get('attachment')
                attachment_name = attachment.get('attachment_name')
                if attachment_content and attachment_name:
                    try:
                        file_doc = frappe.get_doc({
                            "doctype": "File",
                            "file_name": attachment_name,
                            "attached_to_doctype": "LMS Assignment",
                            "attached_to_name": content_doc.name,
                            "content": attachment_content,
                            "decode": True
                        })
                        file_doc.insert()
                        content_doc.append("attachment_file", {
                            "attachment_file": file_doc.file_url
                        })
                    except Exception as e:
                        frappe.throw(f"Failed to upload attachment {attachment_name}: {str(e)}")

        frappe.db.commit()
        return {'status': 'success', 'message': _('Course Content added successfully')}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _('Error in add_course_content'))
        return {'status': 'error', 'message': str(e)}

def get_faculty_member_from_user(user_id):
    """
    Retrieve the faculty member ID linked to a user ID.

    :param user_id: The user ID to retrieve the faculty member for
    :return: The faculty member ID
    """
    employee_id = frappe.get_value("Employee", {"user_id": user_id}, "name")
    if not employee_id:
        raise frappe.ValidationError("Employee not found for the user.")
    
    faculty_member_id = frappe.get_value("Faculty Member", {"employee": employee_id}, "name")
    if not faculty_member_id:
        raise frappe.ValidationError("Faculty member not found for the employee.")
    
    return faculty_member_id

@frappe.whitelist(allow_guest=True)
def get_course_content_details(content_name):
    try:
        # Get the current user ID from the session
        user_id = frappe.session.user
        
        # Retrieve faculty member ID
        faculty_member_id = get_faculty_member_from_user(user_id)
        
        # Fetch the detailed document for the course content
        course_content_doc = frappe.get_doc("Course Content", content_name)
        
        # Verify if the faculty member is associated with the course content
        if course_content_doc.faculty_member != faculty_member_id:
            frappe.response.update({
                "status_code": 403,
                "message": "You are not authorized to access this content."
            })
            return frappe.response["message"]

        # Prepare course content details
        course_content = {
            "title": course_content_doc.title,
            "topic": course_content_doc.topic,
            "attachment_files": [],
        }

        # Fetch attached files from the 'File' table
        attached_files = frappe.get_all('File', filters={
            'attached_to_doctype': 'Course Content',
            'attached_to_name': content_name
        }, fields=['file_name', 'file_url'])

        for file in attached_files:
            course_content["attachment_files"].append({
                "file_name": file['file_name'],
                "file_url": file['file_url']
            })

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Course content details fetched successfully",
            "data": course_content
        })
        return frappe.response["message"]

    except frappe.ValidationError as e:
        frappe.response.update({
            "status_code": 404,
            "message": str(e)
        })
        return frappe.response["message"]

    except Exception as e:
        frappe.log_error(message=f"An error occurred while fetching course content details: {str(e)}", title="Course Content Details Fetch Error")
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching course content details: {str(e)}"
        })
        return frappe.response["message"]