import frappe
from frappe.utils import getdate, today
from frappe import _
from frappe.model.document import Document
import weasyprint
import os


class AcademicEntitlementSlip(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academic_attendance.doctype.academic_entitlement_details.academic_entitlement_details import AcademicEntitlementDetails
        from frappe.types import DF

        academic_term: DF.Link
        academic_year: DF.Link
        amended_from: DF.Link | None
        company: DF.Link | None
        details: DF.Table[AcademicEntitlementDetails]
        end_date: DF.Date
        faculty: DF.Link
        hour_rate_list: DF.Link
        release_date: DF.Date | None
        start_date: DF.Date
    # end: auto-generated types
    @frappe.whitelist()
    def get_academic_entitlement_details(self):
        self.set("details", [])

        # Validate mandatory fields
        mandatory_fields = [
            ("faculty", _("Mandatory field - Faculty")),
            ("academic_year", _("Mandatory field - Academic Year")),
            ("academic_term", _("Mandatory field - Academic Term")),
            ("hour_rate_list", _("Mandatory field - Hour Rate List")),
            ("start_date", _("Mandatory field - From")),
            ("end_date", _("Mandatory field - To")),
        ]
        for field, message in mandatory_fields:
            if not getattr(self, field):
                frappe.throw(message)

        if self.start_date > self.end_date:
            frappe.throw(_("Enter valid Date - From is larger than To"))

        # Fetch academic entitlement details
        academic_entitlement = frappe.get_all(
            "Lesson Attendance",
            filters={
                "attendance_date": ["between", [self.start_date, self.end_date]],
                "academic_term": self.academic_term,
                "academic_year": self.academic_year,
                "faculty": self.faculty,
                "status": "Present",
                "docstatus": 1,
            },
            fields="*",
        )

        if not academic_entitlement:
            self.set("details", [])
            frappe.throw(_("No Entitlement Details Found"))

        for entitlement in academic_entitlement:
            faculty_member = entitlement["faculty_member"]
            academic_rank = frappe.get_all(
                "Faculty Member",
                filters={"name": faculty_member},
                pluck="academic_rank",
            )

            if not academic_rank:
                frappe.throw(_("No academic rank Found"))

            course_type = entitlement.get("course_type")
            academic_rank = academic_rank[0]

            if course_type == "Practical":
                academic_rank1 = "Teacher"
            else:
                academic_rank1 = academic_rank

            hour_rate_data = frappe.get_all(
                "Academic Hour Rate",
                filters={
                    "academic_term": self.academic_term,
                    "academic_year": self.academic_year,
                    "faculty": self.faculty,
                    "hour_rate_list": self.hour_rate_list,
                    "academic_rank": academic_rank1,
                    "status": "occupied",
                },
                pluck="rate",
            )

            if not hour_rate_data:
                frappe.throw(_("No academic Hour Rate Found"))

            rate = hour_rate_data[0]
            total = rate * entitlement.get("teaching_hours")

            child_entry = {
                "doctype": "details",
                "faculty_member": faculty_member,
                "faculty_member_name": entitlement.get("faculty_member_name"),
                "academic_rank": academic_rank,
                "course_type": entitlement.get("course_type"),
                "lesson_type": entitlement.get("lesson_type"),
                "program": entitlement.get("program"),
                "level": entitlement.get("level"),
                "group": entitlement.get("group"),
                "subgroup": entitlement.get("subgroup"),
                "course": entitlement.get("course"),
                "total_hours": entitlement.get("teaching_hours"),
                "academic_hour_rate": rate,
                "status": "occupied",
                "total": total,
                "total_lectures": 1,
            }

            self.append("details", child_entry)

        frappe.msgprint(_("Academic Entitlement Details Fetched Successfully..."))
        return {"entitlement_details": academic_entitlement}

    @frappe.whitelist()
    def generate_detailed_report(self):
        # Ensure the document is saved and submitted before generating the report
        if self.docstatus == 0:
            frappe.throw(_("You Should Save And Submit the document First to generate a detailed report."))

        # Group details by faculty member, course type, and course
        summary = {}
        total = 0
        for detail in self.details:
            key = (detail.faculty_member_name, detail.course_type, detail.course)
            if key not in summary:
                summary[key] = {
                    "total_hours": 0,
                    "total_amount": 0,
                    "total_lectures": 0,
                }
            summary[key]["total_hours"] += detail.total_hours
            summary[key]["total_amount"] += int(detail.total)
            summary[key]["total_lectures"] += detail.total_lectures
            summary[key]["academic_hour_rate"] = detail.academic_hour_rate
            summary[key]["subgroup"] = detail.subgroup
            total += int(detail.total)
        total_tax = total * 0.15
        total_net = total * 0.85
        # Group summary by faculty member
        faculty_summary = {}
        for (faculty_member_name, course_type, course), values in summary.items():
            if faculty_member_name not in faculty_summary:
                faculty_summary[faculty_member_name] = []
            faculty_summary[faculty_member_name].append(
                {
                    "program": detail.program,
                    "level": detail.level,
                    "group": detail.group,
                    "subgroup": values["subgroup"],
                    "status": detail.status,
                    "academic_rank": detail.academic_rank,
                    "faculty_member": faculty_member_name,
                    "course_type": course_type,
                    "total_hours": values["total_hours"],
                    "total_amount": values["total_amount"],
                    "total_lectures": values["total_lectures"],
                    "academic_hour_rate": values["academic_hour_rate"],
                    "course": course,
                    "total": total,
                    "total_tax": total_tax,
                    "total_net": total_net,
                }
            )

        # Calculate the total money for each faculty member
        for faculty_member_name, summaries in faculty_summary.items():
            total_money = sum(summary["total_amount"] for summary in summaries)
            for summary in summaries:
                summary["total1"] = total_money

        # Create HTML content for the detailed report
        html_content = frappe.render_template(
            "templates/detailed_report.html",
            {
                "faculty_summary": faculty_summary,
                "college_name": frappe.db.get_value("Company", self.company, "company_name"),
                "academic_year": self.academic_year,
                "academic_term": self.academic_term,
                "hour_rate_list": self.hour_rate_list,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "release_date": self.release_date,
                "logo": frappe.db.get_value("Faculty", self.faculty, "faculty_logo"),
            },
        )

        # Generate PDF
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Save PDF with versioning
        base_file_name = f"Detailed_report_{today()}"
        file_path = self._get_unique_file_path(base_file_name)
        with open(file_path, "wb") as f:
            f.write(pdf)

        frappe.msgprint(_("Detailed report generated successfully and saved to Downloads."))
        return file_path

    @frappe.whitelist()
    def generate_summary_report(self):
        # Ensure the document is saved and submitted before generating the report
        if self.docstatus == 0 :
            frappe.throw(_("You Should Save And Submit the document First to generate a Totaled report."))

        # Group details by faculty member, course type, and course
        summary = {}
        for detail in self.details:
            key = (detail.faculty_member_name, detail.course_type)
            if key not in summary:
                summary[key] = {
                    "total_hours": 0,
                    "total_amount": 0,
                    "total_lectures": 0,
                }
            summary[key]["total_hours"] += detail.total_hours
            summary[key]["total_amount"] += int(detail.total)
            summary[key]["total_lectures"] += detail.total_lectures
            summary[key]["academic_hour_rate"] = detail.academic_hour_rate

        # Group summary by faculty member
        faculty_summary = {}
        for (faculty_member_name, course_type), values in summary.items():
            if faculty_member_name not in faculty_summary:
                faculty_summary[faculty_member_name] = []
            faculty_summary[faculty_member_name].append(
                {
                    "status": detail.status,
                    "academic_rank": detail.academic_rank,
                    "faculty_member": faculty_member_name,
                    "course_type": course_type,
                    "total_hours": values["total_hours"],
                    "total_amount": values["total_amount"],
                    "total_lectures": values["total_lectures"],
                    "academic_hour_rate": values["academic_hour_rate"],
                }
            )

        # Calculate the total money for each faculty member
        for faculty_member_name, summaries in faculty_summary.items():
            total_money = sum(summary["total_amount"] for summary in summaries)
            for summary in summaries:
                summary["total1"] = total_money

        # Create HTML content for the summary report
        html_content = frappe.render_template(
            "templates/summary_report.html",
            {
                "faculty_summary": faculty_summary,
                "college_name": frappe.db.get_value(
                    "Company", self.company, "company_name"
                ),
                "academic_year": self.academic_year,
                "academic_term": self.academic_term,
                "hour_rate_list": self.hour_rate_list,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "release_date": self.release_date,
                "logo": frappe.db.get_value("Faculty", self.faculty, "faculty_logo"),
            },
        )

        # Generate PDF
        pdf = weasyprint.HTML(string=html_content).write_pdf()

        # Save PDF with versioning
        base_file_name = f"Totaled_report_{today()}"
        file_path = self._get_unique_file_path(base_file_name)
        with open(file_path, "wb") as f:
            f.write(pdf)

        frappe.msgprint(_("Totaled report generated successfully and saved to Downloads."))
        return file_path

    def _get_unique_file_path(self, base_file_name):
        directory = os.path.expanduser("~/Downloads")
        version = 1
        file_path = os.path.join(directory, f"{base_file_name}.pdf")
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_file_name}_v{version}.pdf")
            version += 1
        return file_path

    def before_save(self):
        if not self.details:
            frappe.throw(
                _("You Cannot save document without Getting Academic Entitlement Details.")
            )
