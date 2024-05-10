# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class CouncilMemo(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		council: DF.Link
		description: DF.TextEditor | None
		originating_assignment: DF.Link
		resultant_assignment: DF.Link | None
		sent_date: DF.Date | None
		status: DF.Literal["Draft", "Verified", "Accepted", "Rejected"]
		title: DF.Data | None
	# end: auto-generated types
	def autoname(self):
        # Check if the originating assignment field is set
		if self.originating_assignment:
            # Fetch the 'council' field value from the linked 'OriginatingAssignment'
			council = frappe.get_value('Topic Assignment', self.originating_assignment, 'council')
            
            # Use the current date and the fetched council name for naming, if council is available
			if council:
				self.name = f'{today()}-{council}-Memo'
			else:
                # Fallback naming convention if council is not available
				self.name = f'{today()}-Memo'