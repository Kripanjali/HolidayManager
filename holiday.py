from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

from config import loadJsonLoc
from config import saveJsonLoc

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

class Holiday:

    """Holiday class"""
      
    def __init__(self,name,date):
        self.__name = name
        self.__date = date

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,new_name):
        self.__name = new_name

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self,new_date):
        self.__date = new_date
 
    def __str__ (self):
        output = (f"{self.name} ({self.date.strftime('%Y-%m-%d')})")
        return output
                  
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:

    """HolidayList class"""

    def __init__(self):
       self.innerHolidays = []
   
    def addHoliday(self,holidayObj):
        if (type(holidayObj) == Holiday):
            self.innerHolidays.append(holidayObj)
            print(f'We have added {holidayObj}')
        else:
            print('Enter a Holiday Object.')

        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

    def findHoliday(self,HolidayName, Date):
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName and holiday.date == Date:
                return holiday
        else:
            return False

        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName, Date):
        holiday = self.findHoliday(HolidayName, Date)

        if holiday != False:
            for hol in self.innerHolidays:
                if HolidayName == hol.name and Date == hol.date:
                    print(f"{HolidayName} has been removed from the holiday list.")
                    self.innerHolidays.remove(hol)
                    return True
        else:
            print(f"{HolidayName} not found.")
            return False

        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

    def read_json(self, filelocation):
        with open(filelocation, 'r') as f:
            data = json.load(f)['holidays']
            
        for k in range(0,len(data)):
            date = datetime.strptime(data[k]['date'], '%Y-%m-%d')
            if self.findHoliday(data[k]['name'],date) != False:
                newHoliday = Holiday(data[k]['name'],date)
                self.innerHolidays.append(newHoliday)

        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        with open(filelocation,'w') as f:
            holDict = {}
            holList = []
            for k in self.innerHolidays:
                holiday = {'name':k.name, 'date':k.date.strftime('%Y-%m-%d')}
                holList.append(holiday)
            holDict['holidays'] = holList
            formattedJSON = json.dumps(holDict, indent=1)
            f.write(formattedJSON)

        # Write out json file to selected file.
        
    def scrapeHolidays(self):

        for k in range(2020,2025):
            url = 'https://www.timeanddate.com/holidays/us/{}?hol=33554809'.format(k)
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('table',attrs = {'id':'holidays-table'})
            table_data = table.find('tbody')

            for row in table_data.find_all('tr', class_ = 'showrow'):
                date = row.find('th').text
                dateYear = (f'{k} {date}')
                holidayDate = datetime.strptime(dateYear, "%Y %b %d")
                name = row.find_all("td")[1].text

                holidayFound = self.findHoliday(name, holidayDate)
                if holidayFound == False:
                    newHoliday = Holiday(name, holidayDate)
                    self.innerHolidays.append(newHoliday)

        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        holidayNum = len(self.innerHolidays)
        return holidayNum
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        # filter by year
        yearFilter = list(filter(lambda holiday: (holiday.date.year == year), self.innerHolidays))
        # filter by week number
        holidays_by_week = list(filter(lambda holiday: (holiday.date.isocalendar()[1] == week_number), yearFilter))
        return holidays_by_week
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self,holidayList):
       for k in holidayList:
            print(str(k))
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    #def getWeather(weekNum):

        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        current = datetime.now()
        todayWeek = current.isocalendar()[1]
        todayYear = current.isocalendar()[0]

        filteredList = self.filter_holidays_by_week(todayYear, todayWeek)
        self.displayHolidaysInWeek(filteredList)

        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

def main():
    global loadJsonLoc
    global saveJsonLoc
    
    mainList = HolidayList()
    mainList.read_json(loadJsonLoc)
    mainList.scrapeHolidays()
    mainMenu = True
    save = False

    print("Holiday Management")
    print("===================")
    print(f"There are {mainList.numHolidays()} holidays stored in the system.")
    
    
    while mainMenu:
        print("Holiday Menu")
        print("===================")
        print("1. Add a Holiday")
        print("2. Remove a holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        menu = int(input("Please type the menu option number you'd like to go to: "))
        if menu == 1:
            print("Add a Holiday")
            print("===================")
            holiday = str(input("Holiday: "))
            dateStr = str(input("Date (YYYY-MM-DD): "))
            date = datetime.strptime(dateStr,'%Y-%m-%d')
            mainList.addHoliday(Holiday(holiday, date))
        elif menu == 2:
            print("Remove a Holiday")
            print("===================")
            holidayName = str(input("Holiday Name: "))
            holidayDate = str(input("Input the date in YYYY-MM-DD format: "))
            searchDate = datetime.strptime(holidayDate,'%Y-%m-%d')
            mainList.removeHoliday(holidayName, searchDate)
        elif menu == 3:
            print("Saving Holiday List")
            print("===================")
            wantSave = str(input("Save your changes? [y/n]: "))
            if wantSave == "y":
                mainList.save_to_json(saveJsonLoc)
                print("Success! Your changes have been saved!")
                save= True
            else:
                print("Changes were not saved.")
        elif menu == 4:
            print("View Holidays")
            print("===================")
            year = input("Which year?: ")
            week = input("Which week? [1-52, leave blank for current week]: ")
            if week == "":
                mainList.viewCurrentWeek()
            else:
                print(f"These are the holidays for {year} week {week}:")
                mainList.displayHolidaysInWeek(mainList.filter_holidays_by_week(int(year), int(week)))
        elif menu == 5:
            if save == True:
                exit = input("Are you sure you want to exit? [y/n]: ")
                if exit == 'y':
                    print('Goodbye!')
                    break
                elif exit == 'n':
                    continue
            elif save == False:
                no_save_Exit = input("Are you sure you want to exit? Your changes will be lost! [y/n]: ")
                if no_save_Exit == 'y':
                    print("Goodbye!")
                    break
                elif no_save_Exit == 'n':
                    continue

    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 4. Create while loop for user to keep adding or working with the Calender
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main()

# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.
