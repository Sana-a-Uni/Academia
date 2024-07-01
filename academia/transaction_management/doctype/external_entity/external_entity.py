# Copyright (c) 2024, SanU Development Team and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExternalEntity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transaction_management.doctype.external_entity_designation.external_entity_designation import ExternalEntityDesignation
		from frappe.types import DF

		company: DF.Link | None
		designation: DF.Table[ExternalEntityDesignation]
		external_entity: DF.Data | None
		is_group: DF.Check
		parent_external_entity: DF.Link | None
	# end: auto-generated types
	pass
