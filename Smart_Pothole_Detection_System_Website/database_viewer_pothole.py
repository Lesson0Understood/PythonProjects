import prettytable as pt
from prettytable import PrettyTable
import os
import sqlite3
from termcolor import colored
from art import text2art
import inquirer
from datetime import datetime


MAIN_DIRECTORY = os.path.dirname(__file__)
ERROR_MESSAGES_COLOR = "red"
SUCCESS_MESSAGE_COLOR = "green"


error_messages = {
    "pothole_Not_Exist" : "pothole Does Not Exist",
    "Invalid_Syntax" : "Invalid Syntax",
    "pothole_Details_Not_Exist" : "pothole Details Does Not Exist",
    "No_pothole" : "No Available pothole",
    "No_pothole_Details" : "No Available Details For pothole",
    "No_Tasks" : "No Tasks Available",
    "No_Tags" : "No Tags Available",
    "No_Tasks_For_Tag" : "No Tasks Available For This Tag",
    "No_Tags_For_Task" :"No Tags Available For This Task",
    "Task_Not_Exist" : "Task Does Not Exist",
    "Tag_Not_Exist" : "Tag Does Not Exist",
    "Tag_Already_Assigned" : "Tag Is Already Assigned",
}


def notify_message(message, color="white"):
    # Print big colored messages
    print(colored(text2art(message), color=color))


def print_table(table,rows):
    # Choose table style
    table.set_style(pt.SINGLE_BORDER)
    
    if type(rows) == tuple: # Printing if there is only 1 row
        table.add_row(rows)
        print(table,"\n")
        return
    for row in rows: # Printing if there are multiple rows
        table.add_row(row)
    print(table,"\n")


def validate_id(pothole_input):
    # Check if ID is correct (positive integer)
    if pothole_input.isdigit() and int(pothole_input) >= 1:
        return int(pothole_input)
    
    # Error message
    notify_message("Invalid Syntax",ERROR_MESSAGES_COLOR)
    print("Please enter a valid integer greater than 0\n")
    return None


def validate_date(pothole_input):
    try:
        # Check if format is correct
        datetime.strptime(pothole_input, "%Y-%m-%d")
        return pothole_input
    
    except ValueError:
        # Error message
        notify_message("Invalid Syntax",ERROR_MESSAGES_COLOR)
        print("Please enter the date in the correct format (YYYY-MM-DD)\n")
        return None


def validate_phone(pothole_input):
    # Remove unnecessary characters
    pothole_input = pothole_input.replace("+", "").replace("-", "").replace(" ", "")
    
    # Check if the format is correct
    if pothole_input.isdigit() and len(pothole_input) == 10:
        return pothole_input
    
    # Error message
    notify_message("Invalid Syntax",ERROR_MESSAGES_COLOR)
    print("Please enter a valid phone number (10 digits)\n")
    return None


def get_inputs(*args):
    validators = {
        "id": validate_id,
        "date": validate_date,
        "phone": validate_phone,
        "text": lambda x : x, # no need for special validation
    }
    # format of returned inputs {<name_of_variable> : <validated_input>,...}
    inputs = {}
    
    # Start Validation process by looping through arguments
    for name, type, message in args:
        # Get inputs
        pothole_input = input(message)
        
        # Check if pothole input is empty
        if not pothole_input:
            notify_message("Invalid Syntax",ERROR_MESSAGES_COLOR)
            print("Empty Fields Are Not Allowed\n")
            return None
        
        # Select validator type
        validator = validators.get(type)
        
        # Validate
        validated_input = validator(pothole_input)
        if not validated_input:
            return None
        
        # Add validated input to the inputs dictionary
        inputs[name] = validated_input
        
    return inputs


def get_connection():
    try:
        conn = sqlite3.connect(os.path.join(MAIN_DIRECTORY, "../instance/site.db"))
        return conn
    
    except sqlite3.Error as e:
        notify_message(f"Database connection error: {e}", ERROR_MESSAGES_COLOR)
        return None
    

def search_pothole(pothole_id):
    try:
        # Get pothole from database
        conn = get_connection()
        pothole = conn.execute("SELECT * FROM pothole WHERE id = ?", (pothole_id,)).fetchone()
        return pothole
    
    except sqlite3.Error as e:
        notify_message(f"Database error: {e}", ERROR_MESSAGES_COLOR)
    finally:
        conn.close()
        
        
def print_pothole():
    try:
        # Get pothole from database
        conn = get_connection()
        pothole = conn.execute("SELECT * FROM pothole").fetchall()
        
        # Check if no pothole are in database
        if not pothole:
            notify_message(error_messages["No_pothole"], ERROR_MESSAGES_COLOR)
            return
        
        # Print all pothole
        print_table(PrettyTable(["ID", "location", "severity", "image"]), pothole)
    
    except sqlite3.Error as e:
        notify_message(f"Database error: {e}", ERROR_MESSAGES_COLOR)
    finally:
        conn.close()
        
        
def delete_pothole():
    # Get pothole ID
    inputs = get_inputs(["pothole_id", "id", "Enter pothole ID: "])
    if not inputs:
        return
    
    # Check if pothole exists
    if not search_pothole(inputs["pothole_id"]):
        notify_message(error_messages["pothole_Not_Exist"], ERROR_MESSAGES_COLOR)
        return
    
    try:
        # Delete pothole from database
        conn = get_connection()
        conn.execute("DELETE FROM pothole WHERE id = ?", (inputs["pothole_id"],))
        conn.commit()
        notify_message("pothole Deleted!", SUCCESS_MESSAGE_COLOR)
    
    except sqlite3.Error as e:
        notify_message(f"Database error: {e}", ERROR_MESSAGES_COLOR)
    finally:
        conn.close()


def main():
    while True:
        menu = [
            "View Database",
            "Delete Pothole",
            "Exit",
        ]
        # Take user input
        action = inquirer.prompt([inquirer.List("Actions", message="What do you want to do?", choices=menu)])["Actions"]

        if action == "Exit":
            notify_message("Bye!", "blue")
            break
        # All possible actions
        
        

        
        
        actions = {
            "View Database" : print_pothole,
            "Delete Pothole" : delete_pothole,
        }
        
        actions[action]()
if __name__ == "__main__":
    main()