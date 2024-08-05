# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AcademicHourRate(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        academic_rank: DF.Link
        academic_term: DF.Link
        academic_year: DF.Link
        company: DF.Link | None
        currency: DF.Link | None
        faculty: DF.Link
        faculty_member: DF.Link | None
        hour_rate_list: DF.Link
        note: DF.Text | None
        rate: DF.Currency
        reference: DF.Data | None
        status: DF.Literal["Unoccupied", "occupied"]
        valid_from: DF.Date | None
        valid_upto: DF.Date | None
    # end: auto-generated types
    pass
