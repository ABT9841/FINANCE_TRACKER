import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime # we only need the datetime class from the datetime module
from data_entry import get_date,get_amount,get_description,get_category # type: ignore

class CSV:
    CSV_FILE = "finance_data.csv"  # its a class varaiable
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"
    # we are going to initialize a csv file means read it if exists . if not create it 
    @classmethod # it means it can have access to class itself(accessing class method and varaiables) and it wont have access to its instance.
    def initialize_csv(cls): # class methods recives cls (class itself) instead of self. cls is used to access class level varaiables witin a  methods. here class level varaibale is defiend so.  cls.CSV_FILE and CSV_FILE are same
        try:
            pd.read_csv(cls.CSV_FILE) # checks if we have file or not . if not create it
        except FileNotFoundError:
            # creating the csv file
            # data frame in python provides an effiecinet  and structure way to organize, manipulate and enter the data. it holds the data in the memory(RAM) and we can easily convert the data into csv file and load the data from csv to dataframe
            df =  pd.DataFrame(columns = cls.COLUMNS)  # We want to specify 4 different columns we want to have inside the csv file. here df = dataframe
            # data frame is an object within a pandas that allows us to easily access different rows and columns from a csv file here in this case. we can export Dataframe's into xlx,json,html
            # after creating. we are going to export the dataframe into a csv file.
            #By default Dataframes index is included as the first column.   Setting index=False ensures the index is not included in the output CSV since we don't need it.
            df.to_csv(cls.CSV_FILE, index = False) # converted into csv file. It is going to save a local file with this name(finance_data.csv) in the same directory
            # to_csv creates the file into csv if we dont have it 

#@) work of 2nd class method.  after we know that file exists we are going to add some entries to the files
# we created a new dictionary that contains all of the different data we want to add into csv file. we open csv file in append mode. using "with" syntax here is called context manager(auto close file and deal with any memory leaks)
# fieldnames that we have 
    @classmethod
    def add_entry(cls,date,amount,category,description): # these 4 thing we really need when we are adding new entry to the file.
    # restoring(or organizing) the  4 values(arguments) into a dictionary format. This makes it easier to add data to specific columns in CSV
        new_entry={
            "date": date,
            "amount":amount,
            "category":category,
            "description": description
        }
        with open(cls.CSV_FILE,"a",newline="") as csvfile: # we are opening this file in append mode. we are appending to the end of the file meaning we are opening and putting the cursor at the very end of the file..(not overwriting, deleting). newline ="" ensures no extra blank lines are introduced when adding new rows.    
    #"We are creating a DictWriter object, which allows us to write rows of data (in the form of dictionaries) into the CSV file. The fieldnames parameter specifies the column names in the CSV file, ensuring the keys in the dictionary map correctly to the corresponding columns. The csvfile we just opened in append mode ("a") is passed to the DictWriter."
            writer = csv.DictWriter(csvfile, fieldnames = cls.COLUMNS) 
            # this above line means that = we are creating an instance of the  csv.Dcitwriter class using csv  module.
            # using fieldnames specifies the order and  column(header) for your csv file ensuring that the dictwriter knows how to map the keys from your dictionary(new_entry) to the appropriate columns.( here using order of the keys defined in fieldnames newentry is mapped)
            writer.writerow(new_entry) # we have create this object above(writer)."Using the writer.writerow() method, we add a new row to the CSV file. The new_entry dictionary contains the data for the new row, and the DictWriter maps its keys to the corresponding column names (defined by fieldnames) to ensure the data is written in the correct order."
        print("Entry added successfully")

# 4th step(methods) creating a class method that gives all the transactions within a date range.
    @classmethod
    def get_transaction(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # now convert all of the dates inside of the date column to a date time object. so that we can use them to filter by different transaction
        # working iwth pandas I have ability to access the invidual row and columns
        df["date"] = pd.to_datetime(df["date"],format = CSV.FORMAT) #  df["date"] = this means that i am accessing all of the values inside date column . This line changes the value in the date column. csv.format cause we dont know what format will the date be stored in(here we have defined in data entry file)
        start_date = datetime.strptime(start_date, CSV.FORMAT) # start date will be string and we want to convert it into given format
        end_date = datetime.strptime(end_date, CSV.FORMAT)  # this means that we are taking a string and then parsing it as a DateTime object again, so that we can use the properties of date time object that allows us to filter by and search for differnet dates
        #MASK is something that we can apply to the differnet rows inside of a dateframe. to see if we should select that row or not
        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # this line applies to every single row inside of our data frame and its going to filter the different element according to the specific data range. (comparing) we couldnt do this before cause they were string . now we have it as object
        filtered_df = df.loc[mask] #returns a new filtered dataframe that only contains the rows where above line is true
        # &(bitwise and) this one is similar to and. only used when working with pandas dataframe or mask specificly.

        if filtered_df.empty:
            print("No transcation found in the given data range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}") # converting the datetime object back to string
            print(filtered_df.to_string(index = False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)})) # take the data frames (all of the entry inside of it)  and convert it to string. formatter to format any specific column. here kept column name as the key and takes function we want to apply as second arguments
            # working of this lambda x: x.strftime(CSV.FORMAT) =  this function will  be called with all of the entries from our date column. paremeter x is a dateTime objects beacuese we have converted all of the entries in the date column to a date time object. we are going to format them according to strftime. so we have a string.

            # finding total income and expense and print them out
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum() # this line is similar to use of mask.we are saying data frame to filter we are getting all of the rows in this dataframe where category = income and once i have all those rows i want to get all of the value in amount column and sum those values
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\n Summary :")
            print(f"Total Income : ${total_income:.2f}")
            print(f"Total Expense : ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}")


            return filtered_df # reason is we can create a plot or graph using dataframe now we have it filtered. 

# WORK OF 3RD METHOD ( after we import the function from data entry file)
# write a function that will call theese function in the oreder we want in oreder to collect our data

def add():
    CSV.initialize_csv() # after running it creates a csv file in the current directory. along with column names 
    date = get_date("Enter the date of the transcation(dd-mm-yyyy) or enter for todays date :", allow_default = True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    # after they have been validated by  data enrty function.
    CSV.add_entry(date, amount, category, description)

def plot_transaction(df): # data frame is going to contain all of the transaction that we are going to plot
#  inplace = True modifies the dataframe inplace
# the index is the way in which we locate and manipuate different rows .we are using date column thats how we are going to find different information. we want to sort by the date and to find the correct information based on the date and create a plot  
    df.set_index('date', inplace = True)  # this allows us to find differnet rows and enrty using date cloumn and have more efficicnt operation when we are working with date
#  now we ned to create a two seperate data frame = income data frame and expense data frame . the reason is that i want to have income and expense data frame in two seperate line  
  # this below line is filling in missing days  
    income_df = (
        df[df['category'] == 'Income']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0 )
        )
    
    expense_df = (
        df[df['category'] == 'Expense']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0 )
        )
    
    # created a plot using matplotlib using plt
    plt.figure(figsize=(10,5)) # figure is kinda of setting up the screen/canvas(graph) and we can specify the size
    plt.plot(income_df.index, income_df["amount"], label = "Inncome" , color = "g") # index as x axis and y axis as amount
    plt.plot(expense_df.index, expense_df["amount"], label = "expense" , color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend() # we are going to see label
    plt.grid(True) # so we can more easily where  our vlaues lies 
    plt.show() # takes the plot and shows on screen


     # we dont have sequence data input on easy day. so it creates a dissconnectec line . so to solve the problem .we are going to have all the empty days marked as zero . to see line without discontinution
    # resample filling in the additional rows and having our data stored in daily frequency and we are summing our values and aggregrate the rows that have the same date and add their amounts together and then we reindex to conform to this index .and we are filling any missing values with zero
#D stands for daily frequency . we are going to take the filtered data frame with all of the transaction we want and make sure that  we have now  row for every single day .it also allows us to aggregrate different value that are on the same days .
# sum is going to take all the values and add them all together  and reindex(df.index(df.index, fill_value = 0 )) this makes sure that index is correct after  weve applied  these  front different operations.
# main function. to use the command line and inreact with the user . instead of calling like this CSV.get_transaction("20-07-2024","22-12-2024")
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. view transation and a summary within a date range")
        print('3.Exit')
        choice = input ("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date  = get_date("Enter the end date (dd-mm-yyy2y): ")
            df = CSV.get_transaction(start_date,end_date)
            if input("Do you want to see the plot? (y/n)").lower() == "y" :
                plot_transaction(df)
        elif choice == "3":
            print("Exiting......")
            break
        else:
            print("Invalid choice. Enter 1,2,3.")

# this code is useed to protect the function to not run directly.
if __name__ == "__main__": # When we run this file directly the name will be set to main and  will run direclty wheras when we import this fie this file will not execute directly as name of the module will not be equal to main as it will be set to the file name without extention .py. 
    main()