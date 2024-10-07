import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta

class PromotionRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.academic_arbitrators.academic_arbitrators import AcademicArbitrators
        from academia.academia.doctype.faculty_member_academic_publications.faculty_member_academic_publications import FacultyMemberAcademicPublications
        from frappe.types import DF

        academic_arbitrators: DF.Table[AcademicArbitrators]
        academic_publications: DF.TableMultiSelect[FacultyMemberAcademicPublications]
        amended_from: DF.Link | None
        certificate: DF.Attach | None
        company: DF.Data | None
        current_academic_rank: DF.Data
        date_of_obtaining_the_certificate: DF.Date
        date_of_obtaining_the_current_academic_rank: DF.Date
        department: DF.Data | None
        faculty: DF.Data | None
        faculty_member: DF.Link
        faculty_member_name: DF.Data | None
        naming_series: DF.Literal["PROMREQ-.YYYY.-.faculty_member_name.-"]
        scientific_degree: DF.Link
    # end: auto-generated types

    def validate(self):
        self.check_promotion_eligibility()
        self.check_promotion_eligibility_based_on_period()
        self.check_promotion_eligibility_based_on_scientific_degree()

    def check_promotion_eligibility(self):
        promotion_settings = frappe.get_all(
            "Promotion Settings",
            filters={"academic_rank": self.current_academic_rank},
            fields=["name", "publications_count", "required_period_for_promotion"]
        )

        if promotion_settings:
            promotion_setting = promotion_settings[0]
            required_publications_count = promotion_setting["publications_count"]
            actual_publications_count = len(self.academic_publications)

            if actual_publications_count < required_publications_count:
                frappe.throw(
                    _("You need at least {0} publications for the rank of {1}. You currently have {2}.").format(
                        required_publications_count, self.current_academic_rank, actual_publications_count
                    ),
                    title=_("Insufficient Publications")
                )
        else:
            frappe.throw(
                _("Promotion settings not found for <b>{}</b>. Please create appropriate settings.").format(self.current_academic_rank),
                title=_("Missing Promotion Settings")
            )

    def check_promotion_eligibility_based_on_period(self):
        promotion_settings = frappe.get_all(
            "Promotion Settings",
            filters={"academic_rank": self.current_academic_rank},
            fields=["required_period_for_promotion"]
        )

        if promotion_settings:
            promotion_setting = promotion_settings[0]
            required_period_for_promotion = promotion_setting.get("required_period_for_promotion", 0)

            if required_period_for_promotion is None or not required_period_for_promotion:
                required_period_for_promotion = 0
            else:
                required_period_for_promotion = int(required_period_for_promotion)

            if not self.date_of_obtaining_the_current_academic_rank:
                frappe.throw(
                    _("Date of obtaining the current academic rank is not set."),
                    title=_("Missing Date")
                )

            date_of_obtaining = datetime.strptime(self.date_of_obtaining_the_current_academic_rank, "%Y-%m-%d")
            required_date = date_of_obtaining + timedelta(days=required_period_for_promotion * 30)

            if datetime.now() < required_date:
                frappe.throw(
                    _("You cannot request a promotion yet. The required period of {0} months has not passed since {1}.").format(
                        required_period_for_promotion, self.date_of_obtaining_the_current_academic_rank
                    ),
                    title=_("Promotion Not Eligible")
                )
        else:
            frappe.throw(
                _("Promotion settings not found for <b>{}</b>. Please create appropriate settings.").format(self.current_academic_rank),
                title=_("Missing Promotion Settings")
            )

    def check_promotion_eligibility_based_on_scientific_degree(self):
        promotion_settings = frappe.get_all(
            "Promotion Settings",
            filters={"academic_rank": self.current_academic_rank},
            fields=["required_scientific_degree"]
        )

        if promotion_settings:
            promotion_setting = promotion_settings[0]
            required_scientific_degree = promotion_setting.get("required_scientific_degree")

            # Log the required and current scientific degrees
            frappe.log_error(f"Required scientific degree: {required_scientific_degree}", "Promotion Eligibility Check")
            frappe.log_error(f"Scientific degree in promotion request: {self.scientific_degree}", "Promotion Eligibility Check")

            if required_scientific_degree and self.scientific_degree != required_scientific_degree:
                frappe.throw(
                    _("You need a {0} for Promotion. You currently have {2}.").format(
                        required_scientific_degree, self.current_academic_rank, self.scientific_degree
                    ),
                    title=_("Insufficient Scientific Degree")
                )
        else:
            frappe.throw(
                _("Promotion settings not found for <b>{}</b>. Please create appropriate settings.").format(self.current_academic_rank),
                title=_("Missing Promotion Settings")
            )


