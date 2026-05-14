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

    def convertInt(integer): #backup function if i ever need it
        integer = int(integer)
        if integer == 1:
            return "monday"
        elif integer == 2:
            return "tuesday"
        elif integer == 3:
            return "wednesday"
        elif integer == 4:
            return "thursday"
        elif integer == 5:
            return "friday"
        elif integer == 6:
            return "saturday"
        elif integer == 7:
            return "sunday"