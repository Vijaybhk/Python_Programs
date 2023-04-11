# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lwPnOotufSYbNRDicHEHSrVx9SkDjXA6

Import Statements
"""

import csv

"""Existing ids list for records in final file transaction_records.csv"""

existing_ids = []

"""Function to seek response whenever needed to do further analyses or end the program"""


def seek_response():
    # seeking response from user. validates case and whitespaces.
    response_from_user = input("\nWould you like to run any further analyses (yes/no)? ").lower().strip()

    # If user response is yes, executes tracker function to take import or statistics input
    if response_from_user == "yes":
        return tracker()

    # If user response is no, ends to entire program
    elif response_from_user == "no":
        return

    # If user is response is not among yes or no, seeks user response again to proceed.
    else:
        print("Invalid Input. Enter only yes or no.")
        return seek_response()


"""Function to add transactions which takes an input file to add 
transactions to the final file transaction_records.csv"""


def add_transactions(read_file):
    # starting with no of new transactions for a new addition as 0
    new_transactions = 0

    # Opens input imported file in read mode
    with open(read_file, "r") as opener:
        reader = csv.reader(opener)
        for row in reader:
            transaction_id = int(row[0])

            # If transaction id already exists in transaction_records.csv, returns the transaction_id as already present
            if transaction_id in existing_ids:
                print("Data for ID", str(transaction_id), "already in transaction records.")

            else:

                # Add the transaction to existing ids list for future check
                existing_ids.append(transaction_id)

                # Increment of the number of new transactions added by 1
                new_transactions += 1

                # Else add the transaction details to the final file
                with open('transaction_records.csv', 'a', newline='') as app_opener:
                    appender = csv.writer(app_opener)
                    appender.writerow(row)

    # Outputs the number of transactions added at the end of addition and seeks response again
    print("{} transaction records successfully loaded.".format(new_transactions))
    seek_response()
    return


"""Function to perform steps for statistics or import"""


def tracker():
    # Take input whether user would like to import or check statistics
    input_from_user = input("\nWhat would you like to perform (import/statistics)? ").lower().strip()

    if input_from_user == "statistics":

        try:

            # If user inputs statistics, checks pending transactions amount and
            # number of transactions to print output

            with open("transaction_records.csv", "r") as read_opener:
                # Instantiate number of transactions in the final file as 0
                row_count = 0

                # Instantiate pending transaction amount as 0
                amount = 0.0

                reader = csv.reader(read_opener)
                for line in reader:
                    # Increment number of transactions by 1
                    row_count = row_count + 1

                    # Condition to check pending transactions
                    if line[2] == 'PENDING':
                        # Increment amount by pending transaction amount
                        amount = amount + float(line[4])
                print("Number of lifetime transactions: {}".format(row_count))
                print("Total dollar amount pending: {}".format(amount))
                seek_response()

        # If the file is not found or created yet, prints no data
        except:
            print("Sorry, no transaction data was loaded yet. Please try again.")
            seek_response()

    elif input_from_user == "import":

        # Takes file input to be imported
        file_input = input("Which file would you like to import? ").lower().strip()

        # If the file is among the list, transactions will be added
        if file_input in ["new_transactions1.csv", "new_transactions2.csv"]:
            add_transactions(file_input)

        # Else outputs a message that file not found and seeks response again
        else:
            print("Sorry, that file could not be found. Please try again.")
            seek_response()

    else:

        # If user input is not among import or statistics, prints invalid input and re-runs tracker function
        print("Invalid Input. Enter only import or statistics.")
        tracker()

    return


"""Main function to run the program"""


def main():
    print("Welcome to the transaction tracker: ")
    tracker()
    return


"""Condition to run the main function"""

if __name__ == "__main__":
    main()