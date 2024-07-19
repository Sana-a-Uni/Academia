# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime
import frappe
from frappe import _  # Import the translation function

class FacultyMemberSettings(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        academic_rank: DF.Link | None
        naming_series: DF.Literal["ACAD-FM-S-.YYYY.-.MM.-.####."]
        probation_period: DF.Data | None
        valid_from: DF.Date
        valid_upto: DF.Date | None
    # end: auto-generated types
    
    def validate(self):
        self.validate_date_range()

    def validate_date_range(self):
        if self.valid_from and self.valid_upto:
            valid_from_date = datetime.strptime(self.valid_from, "%Y-%m-%d")
            valid_upto_date = datetime.strptime(self.valid_upto, "%Y-%m-%d")

            if valid_from_date >= valid_upto_date:
                frappe.throw(
                    _("The 'Valid From' date must be lesser than the 'Valid Upto' date."),
                    title=_("Invalid Date Range")
                )
