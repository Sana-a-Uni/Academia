# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _

class AcademicPublication(Document):
    def validate(self):
        if self.date_of_publish:
            if self.date_of_publish > frappe.utils.today():
                frappe.throw(_("Date of publish must be less than or equal to today's date"))



    # def is_valid_date(self, selected_date_str, date_of_publish):
    #     selected_date = date.fromisoformat(selected_date_str)
    #     today_date = date.today()
    #     if selected_date > today_date:
    #         return False, f"{date_of_publish} must be less than or equal to today's date"
    #     else:
    #         return True, None

	        
	
	 
			
			
           
				
                
                
				
                     
       
          



