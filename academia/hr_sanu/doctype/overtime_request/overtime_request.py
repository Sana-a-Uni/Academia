# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OvertimeRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.hr_sanu.doctype.overtime_request_employee.overtime_request_employee import (
			OvertimeRequestEmployee,
		)
		from frappe.types import DF

		amended_from: DF.Link | None
		default_shift: DF.Link
		description: DF.Text | None
		employees: DF.Table[OvertimeRequestEmployee]
		end_time: DF.Datetime
		request_created_by: DF.Link | None
		request_type: DF.Literal[
			"", "\u0625\u062f\u0627\u0631\u064a", "\u0623\u0643\u0627\u062f\u064a\u0645\u064a"
		]
		start_time: DF.Datetime
		status: DF.Literal["Draft", "Pending Approval", "Approved", "Rejected"]
		to_do: DF.Data
	# end: auto-generated types
	pass
