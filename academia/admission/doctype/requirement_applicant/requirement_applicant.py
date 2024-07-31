# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class RequirementApplicant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.admission.doctype.requirement_applicant_document_type.requirement_applicant_document_type import RequirementApplicantDocumentType
		from academia.admission.doctype.requirement_applicant_qualification_type.requirement_applicant_qualification_type import RequirementApplicantQualificationType
		from frappe.types import DF

		document_type: DF.TableMultiSelect[RequirementApplicantDocumentType]
		program_degree: DF.Link | None
		qualification_type: DF.TableMultiSelect[RequirementApplicantQualificationType]
	# end: auto-generated types
	pass
