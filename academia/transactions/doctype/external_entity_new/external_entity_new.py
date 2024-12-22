# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ExternalEntityNew(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transactions.doctype.external_entity_designation_new.external_entity_designation_new import (
			ExternalEntityDesignationNew,
		)

		designations: DF.Table[ExternalEntityDesignationNew]
		external_entity: DF.Data | None
		is_group: DF.Check
		logo: DF.Attach | None
		parent_external_entity: DF.Link | None
	# end: auto-generated types
	pass
