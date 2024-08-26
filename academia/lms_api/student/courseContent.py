import frappe

@frappe.whitelist(allow_guest=True)
def get_course_content_summary(course_name="DS-2024-04-08", course_type="Lab"):
    try:
        # Fetch course contents based on filters
        course_contents = frappe.get_all("Course Content", filters={
            'course': course_name,
            'course_type': course_type
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
def get_course_content_details(content_name="71856e9f42"):
    try:
        # Fetch the detailed document for the course content
        course_content_doc = frappe.get_doc("Course Content", content_name)
        
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

    except Exception as e:
        frappe.log_error(message=f"An error occurred while fetching course content details: {str(e)}", title="Course Content Details Fetch Error")
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching course content details: {str(e)}"
        })
        return frappe.response["message"]
