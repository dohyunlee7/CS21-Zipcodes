"""
Dohyun Lee
April 3rd, 2019
A search program for zip codes
"""
from boundaries import *

def main():
    printIntro()
    zipLst = readData()
    choice = menu()
    while choice != -1:
        if choice == 1:
            getZipCode(zipLst)
            choice = menu()
        elif choice == 2:
            getCity(zipLst)
            choice = menu()
        elif choice == 3:
            mapState(zipLst)
            choice = menu()
        elif choice == 4:
            mapCounty(zipLst)
            choice = menu()
        elif choice == 5:
            print("Thank you for using my ZIP code finder!")
            choice = -1
        else:
            print("Invalid choice. Please choose a valid option.")
            choice = menu()

def printIntro():
    """
    purpose: displays introduction to the program
    parameters: none
    returns: none
    """
    print("Welcome to the zipcode program!")
    print()

def readData():
    """
    purpose: opens the required text file and appends class objects to our
    list of data
    parameters: None
    returns: lst -- list of data
    """
    myfile = open("/usr/local/doc/zipcodes.txt", "r")
    lst = []
    for line in myfile:
        txt = line.strip().split(",") #get list of strings
        place = ZipCode(txt[0], float(txt[1]), float(txt[2]), txt[3], txt[4], txt[5], int(txt[6]))
        lst.append(place) #make a list of class objects
    myfile.close()
    return lst

def menu():
    """
    purpose: displays the menu of choices to pick from 1-5
    parameters: none
    returns: a positive integer from 1-5
    """
    print("Please select one of the following choices: ")
    print()
    print("""1. Find by ZIP code
2. Find by name
3. Map state
4. Map county
5. Quit""")
    print()
    choice = int(input("Choice? "))
    return choice

def getZipCode(info):
    """
    purpose: user enters a zip and searches for it using binary search
    paramters: info -- the text file containing the zipcodes
    returns: nothing
    """
    zip = input("Enter a 5-digit ZIP code: ")
    while len(zip) > 5 or len(zip) < 5 or zip.isdigit() == False:
        print("%s is not a valid ZIP code. Try again." % (zip))
        zip = input("Enter a 5-digit ZIP code: ")

    first = 0
    last = len(info) - 1
    found = False
    while first <= last and not found:
        mid = (first + last) // 2
        if info[mid].getZip() == zip:
            found = True
        else:
            if int(zip) < int(info[mid].getZip()):
                last = mid - 1
            else:
                first = mid + 1

    if found == True:
        print("%s, %s, %s" % (info[mid].getName(), info[mid].getState(), info[mid].getZip()))
        print("%s County"  % (info[mid].getCounty()))
        print("Population: %s" % (info[mid].getPopulation()))
    else:
        print("No info on this ZIP exists")

def getCity(info):
    """
    purpose: prompts user to enter a city, print out the city, state, ZIP code,
    and population of all cities that start with the city name the user typed.
    parameters: info -- text file containing the zipcodes
    returns: nothing
    """
    name = input("Enter a city prefix: ")
    while len(name) == 0:
        name = input("Please enter a city prefix: ")
    n = 0
    for i in info:
        if i.getName().startswith(name) == True:
            n = n + 1
            print("%s, %s %s Population: %s" % (i.getName(), i.getState(), i.getZip(), i.getPopulation()))
    if n == 0:
        print("Sorry... I can't find any info about that name...")


def mapState(info):
    """
    purpose: prompt user for state & population threshold, if valid program
    should draw the boundary of state and draw locations of cities in the state
    greater than or equal to p
    parameters: info -- text file containing zipcode, city, and state information
    returns: a graphic window of the state with cities plotted as points
    """
    state = input("Enter a two-letter state postal code: ")
    while len(state) == 0 or state.isdigit() == True:
        state = input("Please enter a two-letter state postal code: ")
    p = int(input("Enter a population threshold for big cities: "))
    while p < 0:
        print("This is not a valid threshold.")
        p = int(input("Enter a population threshold for big cities: "))
    win = getStateGraphWin(state)
    if win == None:
        print("No info for state %s found" % (state))
    else:
        pt1 = Point(50, 50)
        pt1.draw(win)
        for i in info:
            if i.getPopulation() >= p and i.getState() == state:
                pt2 = Point(i.getLongitude(),i.getLatitude())
                pt2.setFill("blue")
                pt2.draw(win)
            elif i.getState() == state:
                pt3 = Point(i.getLongitude(),i.getLatitude())
                pt3.setFill("magenta")
                pt3.draw(win)
        win.getMouse()
        win.close()

def mapCounty(info):
    """
    purpose: prompt user for valid ZIP code, search using binary search. draws
    a point for all cities in the same county as the found zip.
    parameters: info -- text file containing zipcode, city, and state information
    returns: a graphics window
    """
    zip = input("Enter a 5-digit ZIP code: ")
    while len(zip) > 5 or len(zip) < 5 or zip.isdigit() == False:
        print("%s is not a valid ZIP code. Try again." % (zip))
        zip = input("Enter a 5-digit ZIP code: ")
    first = 0
    last = len(info)
    found = False


    first = 0
    last = len(info) - 1
    found = False
    while first <= last and not found:
        mid = (first + last) // 2
        if info[mid].getZip() == zip:
            found = True
        else:
            if int(zip) < int(info[mid].getZip()):
                last = mid - 1
            else:
                first = mid + 1

    if found == True:
        print("%s, %s, %s" % (info[mid].getName(), info[mid].getState(), info[mid].getZip()))
        print("%s County" % (info[mid].getCounty()))
        print("Population: %s" % (info[mid].getPopulation()))
        win = getStateGraphWin(info[mid].getState())
        pt1 = Point(info[mid].getLongitude(), info[mid].getLatitude())
        pt1.setFill("black")
        pt1.draw(win)
        for i in info:
            if i.getCounty() == info[mid].getCounty() and i.getState() == info[mid].getState():
                pt2 = Point(i.getLongitude(),i.getLatitude())
                pt2.setFill("black")
                pt2.draw(win)
    else:
        print("No info on this ZIP exists")

main()
