


# from hijri_converter import Hijri, Gregorian
# import frappe


# def enToArNumb(number): 
#     dic = { 
#         '0': '۰', 
#         '1': '١', 
#         '2': '٢', 
#         '3': '۳', 
#         '4': '۴', 
#         '5': '۵', 
#         '6': '۶', 
#         '7': '۷', 
#         '8': '۸', 
#         '9': '۹', 
#     }
#     converted = ''
#     for digit in number:
#         converted += dic.get(digit, digit) 
#     return converted

# def convert_to_hijri(date):
#     # Convert the date string to Hijri date
#     # hijri_date = convert.Gregorian(date_string).to_hijri()


#     # # Convert a Hijri date to Gregorian
#     # g = Hijri(1403, 2, 17).to_gregorian()

#     # Convert a Gregorian date to Hijri

#     hijri_date = Gregorian(1982, 12, 2).to_hijri()
#     # frappe.msgprint(hijri_date)
#     # ar_numbers = [enToArNumb(num) for num in numbers]
#     # print(type(hijri_date.day))
#     ar_numbers=""
#     # ar_numbers += [enToArNumb(num) for num in str(hijri_date.day)]
    
    
#     year=enToArNumb(str(hijri_date.year))
#     year +=  hijri_date.notation('ar')


    
#     # return f"{enToArNumb(str(hijri_date.day))} {enToArNumb(str(hijri_date.year))} {hijri_date.month_name('ar') } {hijri_date.notation('ar')} "
#     # return f"{enToArNumb(str(hijri_date.day))} {hijri_date.notation('ar')} {hijri_date.month_name('ar') } {enToArNumb(str(hijri_date.year))}  "
#     return f"{enToArNumb(str(hijri_date.day))} {hijri_date.month_name('ar')} {year} "