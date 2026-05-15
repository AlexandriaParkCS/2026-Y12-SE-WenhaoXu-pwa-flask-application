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

    def convertTupleList(tup):
        count = 0
        for item in tup:
            mylist = list(item)
            tup[count] = mylist
            count = count + 1

        for item in tup:
            item[2] = timeconvert.convertInt(item[2])

        return tup