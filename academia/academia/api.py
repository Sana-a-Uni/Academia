# /home/frappe/frappe-bench/apps/academia/academia/academia/api.py

# import frappe

# @frappe.whitelist()
# def calculate_probation_end_date(academic_rank, date_of_joining_in_university):
#     print(f"Calculating for academic rank: {academic_rank}, date of joining: {date_of_joining_in_university}")
#     probation_period_end_date = None
#     is_eligible_for_granting_tenure = 0

#     # Fetch all settings
#     settings_list = frappe.get_all('Faculty Member Settings', fields=['name'])

#     for setting in settings_list:
#         settings_doc = frappe.get_doc('Faculty Member Settings', setting.name)
#         for period in settings_doc.probation_periods:
#             if period.academic_rank == academic_rank:
#                 probation_period = int(period.probation_period)
#                 valid_from = period.valid_from
#                 valid_upto = period.valid_upto

#                 if valid_from <= date_of_joining_in_university <= valid_upto:
#                     probation_period_end_date = frappe.utils.add_months(date_of_joining_in_university, probation_period)
#                     print(f"Probation period end date calculated: {probation_period_end_date}")
#                     if frappe.utils.nowdate() >= probation_period_end_date:
#                         is_eligible_for_granting_tenure = 1
#                     break

#     return {
#         'probation_period_end_date': probation_period_end_date,
#         'is_eligible_for_granting_tenure': is_eligible_for_granting_tenure
#     }
