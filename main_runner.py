import os
import json
import requests

#These are currently filled with dummy data but are expected to be filled with actual zendesk credentials
username = "username@email.com"
password = "123456"
subdomain = "zccdhyey"
auth = (username, password)

allTicketData = {}

#This method calls the api to get all of the tickets.
def getAll():
    url = "https://" + subdomain + ".zendesk.com/api/v2/tickets.json"
    params = {"per page": 25, "page": 1}
    stuff = requests.get(url=url, params=params, auth=auth)
    if stuff.status_code == 200:
        return json.loads(stuff.text)
    else:
        print("The tickets could not be loaded up. Sorry :(")
        return None

#This method calls the api to get one specific ticket through the id.
def getOne(id:str):
    url = "https://" + subdomain + ".zendesk.com/api/v2/tickets/" + id + ".json"
    params = {"per page": 25, "page": 1}
    stuff = requests.get(url=url, params=params, auth=auth)
    if stuff.status_code == 200:
        return json.loads(stuff.text)
    else:
        print("The ticket you wanted was not able to be loaded. Sorry :(")
        return None

#This method prints the home menu from where the first decisions are made
def printMenu():
    os.system("cls||clear")
    print("WELCOME TO YOUR VERY OWN TICKET VIEWER! :) \n")
    print("Type ALL (case insensitive) to view ALL THE TICKETS!!!")
    print("OR" + ("." * 10))
    print("Type the specific ticket id (numeric) of the ticket you want to see to see just that one ticket.")
    print("OR" + ("." * 10))
    print("Just type q (case insensitive) if you're done seeing tickets. \n")
    userInput = input("Enter Input: ")
    if userInput.isnumeric():
        data = getOne(userInput)
        printOne(data)
    elif userInput.lower() == "all":
        global allTicketData
        allTicketData = getAll()
        printAll(1)
    elif userInput.lower() == "q":
        print("Bye, hope to see you again soon!")
    else:
        print("\nIt seems you didn't follow the directions in the menu.")
        callWhenProblem()

#this method handles calling the methods to print different pages and what tickets to print
# a more appropriate name here would be print page with the other method being print helper as it really only prints one page
def printAll(page):
    if allTicketData == None:
        print("There seemed to have been a problem and no data was received.")
        callWhenProblem()
        return
    
    numTickets = allTicketData['count']
    tickets = allTicketData['tickets']
    ticketStart = (25 * page) - 25
    ticketEnd = 25 * page

    if ticketEnd > numTickets and ticketStart == 0:
        ticketEnd = numTickets
    
    printPage(page, tickets[ticketStart:ticketEnd])
    paginationOptions(page, ticketStart, ticketEnd, numTickets)

#This method lists off and handles the options to move between pages or exit
def paginationOptions(page, ticketStart, ticketEnd, numTickets):
    print("\nn for next page.")
    print("p for previous page.")
    print("h to go back to the main menu options.")
    print("q to quit.")
    userInput = input("Enter Next Input: ").lower()
    if userInput == "h":
        printMenu()
    elif userInput == "q":
        print("\nBye, hope to see you again soon!\n")
    elif userInput == "n":
        if ticketStart + 25 >= numTickets:
            print("\nYou have reached the last page. There are no more pages of tickets.")
            paginationOptions(page, ticketStart, ticketEnd, numTickets)
        else:
            printAll(page + 1)
    elif userInput == "p":
        if page == 1:
            print("\nThis is the first page. There are no previous pages of tickets.")
            paginationOptions(page, ticketStart, ticketEnd, numTickets)
        else:
            printAll(page - 1)
    else:
        print("\nYou didn't type in one of the input options try again.")
        paginationOptions(page, ticketStart, ticketEnd, numTickets)

#As explained before a more fitting name here would be printPageHelper
def printPage(page, tickets):
    os.system("clear||cls")
    print("Page #" + str(page))
    printHeader()
    for ticket in tickets:
        printTicket(ticket)

#This prints individual tickets for the printPage method
def printTicket(ticket):
    id = str(ticket["id"])
    subject = ticket["subject"]
    assignee = str(ticket["assignee_id"])
    status = ticket["status"]
    datetime = str(ticket["updated_at"])
    date = datetime[0:10]
    time = datetime[11:19]
    
    if len(id) > 10:
        id = id[0:7] + "..."
    if len(subject) > 15:
        subject = subject[0:13] + "..."
    if len(assignee) > 14:
        assignee = assignee[0:10] + "..."
    
    print(id.ljust(12) + subject.ljust(17) + assignee.ljust(16) + status.ljust(11) + date + "    " + time)

#This prints one ticket when only one ticket has been requested.
def printOne(data):
    if data == None:
        print("There seemed to have been a problem and no data was received.")
        callWhenProblem()
        return
    
    ticket = data["ticket"]
    if ticket == None:
        print("Sorry, there was no ticket found with this id.")
        callWhenProblem()
        return
    
    id = str(ticket["id"])
    subject = ticket["subject"]
    assignee = str(ticket["assignee_id"])
    status = ticket["status"]
    datetime = str(ticket["updated_at"])
    date = datetime[0:10]
    time = datetime[11:19]
    
    printHeader()

    if len(id) > 10:
        id = id[0:7] + "..."
    if len(subject) > 15:
        subject = subject[0:13] + "..."
    if len(assignee) > 14:
        assignee = assignee[0:10] + "..."
    
    print(id.ljust(12) + subject.ljust(17) + assignee.ljust(16) + status.ljust(11) + date + "    " + time)

    callWhenProblem()

#This method prints the header for which 
def printHeader():
    print("")
    print("ID" + (" "*10) + "SUBJECT" + (" " * 10) + "ASSIGNEE ID" + (" "*5) + "STATUS" + (" " * 5) + "DATE UPDATED  TIME UPDATED")

#more accurate name would be call when done with current task
def callWhenProblem():
    print("\nq to quit.")
    print("h to go back to the main menu options.")
    userInput = input("Enter Next Input: ").lower()
    if userInput == "h":
        printMenu()
    elif userInput == "q":
        print("\nBye, hope to see you again soon!\n")
    else:
        print("\nYou can only type 'h' or 'q'")
        callWhenProblem()

printMenu()
