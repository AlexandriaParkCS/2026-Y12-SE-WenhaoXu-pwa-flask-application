class timeconvert:
    def convertDate(weekday):
        if weekday.casefold() == "monday":
            return 0
        elif weekday.casefold() == "tuesday":
            return 1
        elif weekday.casefold() == "wednesday":
            return 2
        elif weekday.casefold() == "thursday":
            return 3
        elif weekday.casefold() == "friday":
            return 4
        elif weekday.casefold() == "saturday":
            return 5
        elif weekday.casefold() == "sunday":
            return 6

    def convertInt(integer):
        integer = int(integer)
        if integer == 0:
            return "Monday"
        elif integer == 1:
            return "Tuesday"
        elif integer == 2:
            return "Wednesday"
        elif integer == 3:
            return "Thursday"
        elif integer == 4:
            return "Friday"
        elif integer == 5:
            return "Saturday"
        elif integer == 6:
            return "Sunday"

    def convertMeridiem(time_hour, meridiem):
        # converting 12hr time to 24hr for database storing
        if meridiem.casefold() == "pm":
            time_hour = int(time_hour) + 12

        return time_hour

    def convertTupleList(tup):
        count = 0
        # SQL returns list(tuple), but weekdays are stored as integers.
        # tuples cannot be edited, so this converts the tuple inside into a list
        for item in tup:
            mylist = list(item)
            tup[count] = mylist
            count = count + 1
        # using list means items can be changed
        # changing to actual weekday for display
        for item in tup:
            item[2] = timeconvert.convertInt(item[2])
        # SQL integers cannot store 01, and so this will change any 1,2,3 to 01,02,03 for display
        for item in tup:
            if int(item[4])<10:
                item[4] = f"0{item[4]}"

        return tup

# Testing
'''
hour = 4
ampm = "pm"
testing1 = timeconvert.convertMeridiem(hour, ampm)
print(testing1)
'''