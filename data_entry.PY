# WHY THIS FILE = SO THAT I HAVE A PLACE WHERE I CAN WRITE ALL THE FUNCTION RELATED GETTING THE INFORMATION FROM USER. SO THAT MAIN FILE STAYS LITTLE BIT CLEANER
# this file will collect  data from users and have all of our input statement and validate data.
from datetime import datetime 

date_format = "%d-%m-%Y"
CATEGORIES = { "I":  "Income", "E": "Expense"}

def  get_date(prompt, allow_default= False): # prompt ask user for input before they give us the date. allow defalut tells us if we should have a default value of today's date. I want to get todays date by just hit enter 
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format) # this will be returned in a situation where we are allowed the default and the user didnt type anything in.
    
    try:
        valid_date = datetime.strptime(date_str,date_format) # take the date string and use this format and try to connvert this into date time object(strp).thats valid
        return valid_date.strftime(date_format) # after we have get date time object we are converting back into string repersantation(strf). and this will make sure that it cleans the date user typed in and gives in the format we need 




    except ValueError:
        print("Invalid date format . Please enter the date in dd-mm-yyyy format")
        return get_date(prompt,allow_default) # this is called recursive function. we keep doing this until user input valid date

def get_amount():
    try:
        amount = float(input("Enter the amount : "))
        if amount <= 0:
            raise ValueError("Amount must be a non negative, non zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for income and 'E' for expense)")
    if category in CATEGORIES:
        return CATEGORIES[category] # returns value assigned to dict key
    
    print("Invalid category. Please enter ('I' for income and 'E' for expense)")
    return get_category()


def get_description():
    return input("Enter a description(OPTIONAL): ")