# i pledge my honor that i have abided by the stevens Honor System ~MF
import ged
from datetime import date
from datetime import datetime

#print upcomingBdays
def US39(gedout):
    retval = []
    currdate = str(datetime.today().strftime('%d-%m-%Y'))
    tcurrdate = str(currdate).split("-")

    for key in gedout["families"]:
        dt = gedout["families"][key]['MARR'];
        tempD = manipulateDates(dt)

        currdate = date(int(tcurrdate[2]), int(tcurrdate[1]), int(tcurrdate[0]))
        tempD = date(int(tempD[2]), int(tempD[1]), int(tempD[0]))


        delta = currdate - tempD

        diff = delta.days

        if diff <= 30 and diff > 0:
            retval.append(key)


    if len(retval) == 0:
        retval.append("US39: no upcoming anniversaries")
        return retval
    else:
        x = []
        ret = "US39: upcoming anniversaries - "
        for i in retval:
            ret += i + " "
        x.append(ret)
        return x

def US38(gedout):
    retval = []
    currdate = str(datetime.today().strftime('%d-%m-%Y'))
    tcurrdate = str(currdate).split("-")

    for key in gedout["individuals"]:
        dt = gedout["individuals"][key]['BIRT'];
        tempD = manipulateDates(dt)

        currdate = date(int(tcurrdate[2]), int(tcurrdate[1]), int(tcurrdate[0]))
        tempD = date(int(tempD[2]), int(tempD[1]), int(tempD[0]))
        delta = currdate - tempD

        diff = delta.days

        if diff <= 30 and diff > 0:
            retval.append(key)

    if len(retval) == 0:
        retval.append("US38: no upcoming birthdays")
        return retval
    else:
        x = []
        ret = "US38: upcoming birthdays - "
        for i in retval:
            ret += i + " "
        x.append(ret)
        return x


#print married
def US30_list(gedout):

    couples = []
    for key in gedout["families"]:
        entry = gedout["families"][key]
        couples.append([ entry["HUSB"], entry["WIFE"]])

    #print(couples)

    retval = "List of families \n"
    x = gedout["individuals"].__len__()

    # remove any couples of which any partner is dead
    famsToRemove = []
    for key in gedout["individuals"]:
        for fams in couples:
            for peeps in fams:
                if peeps == key:
                    if 'DEAT' in gedout["individuals"][key]:
                        couples.remove(fams)

    #print(couples)

    if len(couples) == 0:
        return ["US30: No married couples", []]
    else:
        return ["US30: list of married couples:", couples]

def manipulateDates(dt):
    tempDT = dt.split(" ")
    months = ['1', "JAN", '2', "FEB", '3', "MAR", '4', "APR", '5', "MAY", '6', "JUN", '7', "JUL", '8', "AUG", '9',
              "SEP", '10', "OCT", '11',
              "NOV", '12', "DEC"]
    for i in range(months.__len__()):
        if tempDT[1] == months[i]:
            tempDT[1] = months[i - 1]

    return tempDT

def compareDates(bt, dt):
    tempBT = bt.split(" ")
    tempDT = dt.split(" ")


    months = ['1', "JAN", '2', "FEB", '3', "MAR", '4',  "APR", '5', "MAY", '6', "JUN", '7', "JUL", '8', "AUG", '9', "SEP", '10', "OCT", '11',
              "NOV", '12', "DEC"]
    for i in range(months.__len__()):
        if tempBT[1] == months[i]:
            tempBT[1] = months[i-1]

        if tempDT[1] == months[i]:
            tempDT[1] = months[i - 1]

            #print(tempDT[0] +"-" + tempDT[1] + "-"+ tempDT[2])

    # compare years born
    if (int(tempBT[2]) > int(tempDT[2])):
        return False
    # compare months born (if in same year)
    if (int(tempBT[1]) > int(tempDT[1])):
        return False
    # compare days born (if in same year and month )
    if (int(tempBT[0]) > int(tempDT[0])):
        return False

    # if BT < DT, return true
    return True

# no birth before death
def US03(gedout):
    badPeeps = []
    for key in gedout["individuals"]:
        if 'DEAT' in gedout["individuals"][key]:
            dt = gedout["individuals"][key]['DEAT'];
            bt = gedout["individuals"][key]['BIRT'];

            # bt > death if false
            if compareDates(bt, dt) == False:
                badPeeps.append(key)

    if len(badPeeps) == 0:
        badPeeps.append("US03: no one has died before they were born")
        return badPeeps
    else:
        x = []
        ret = "Error US03: Users [ "
        for i in badPeeps:
            ret += i + " "
        ret += "] have died before being born"
        x.append(ret)
        return x
    return badPeeps


#list recent births
def US35(gedout):
    retval = []
    currdate=str(datetime.today().strftime('%d-%m-%Y'))
    tcurrdate = str(currdate).split("-")

    for key in gedout["individuals"]:
        dt = gedout["individuals"][key]['BIRT'];
        tempD = manipulateDates(dt)

        currdate = date(int(tcurrdate[2]), int(tcurrdate[1]), int(tcurrdate[0]))
        tempD = date(int(tempD[2]), int(tempD[1]), int(tempD[0]))
        delta = currdate - tempD



        diff = delta.days

        if diff <= 30 and diff > 0:
            retval.append(key)

    if len(retval) == 0:
        retval.append("US35: no recent births")
        return retval
    else:
        x = []
        ret = "US35: recent births - "
        for i in retval:
            ret += i + " "
        x.append(ret)
        return x

#list recent Deaths
def US36(gedout):

    retval = []
    currdate=str(datetime.today().strftime('%d-%m-%Y'))
    tcurrdate = str(currdate).split("-")

    for key in gedout["individuals"]:
        if 'DEAT' in gedout["individuals"][key]:
            dt = gedout["individuals"][key]['DEAT'];
            tempD = manipulateDates(dt)

            currdate = date(int(tcurrdate[2]), int(tcurrdate[1]), int(tcurrdate[0]))
            tempD = date(int(tempD[2]), int(tempD[1]), int(tempD[0]))
            delta = currdate - tempD

            diff = delta.days
            if diff <= 30 and diff > 0:
                retval.append(key)

    if len(retval) == 0:
        retval.append("US36: no recent deaths")
        return retval
    else:
        x = []
        ret = "US36: recent deaths - "
        for i in retval:
            ret += i + " "
        x.append(ret)
        return x

def doesDateneedModification(dt):
    dt = dt.split(" ")
    if dt.__len__() != 3:
        return True
    return False

def canDateBeUsed(dt):
    dt = dt.split(" ")
    if dt.__len__() == 3:
        return True
    if dt.__len__() == 1: # must be year data only
        try:
            yr = int(dt[0])
            return True
        except ValueError:
            return False
    elif  dt.__len__() == 2: #must be a year and month only
        try:
            yr = int(dt[1])
            months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
            if dt[0] in months:
                return True
            return False
        except ValueError:
            return False
#fix any valid dates
def fixDates(dt):
    #if no day - make 10th day of month
    #if no  month - mkae first month of year

    dt = dt.split(" ")
    if(dt.__len__() == 3):
        return dt[0] + ' ' + dt[1] + ' ' + dt[2]
    if(dt.__len__() == 1):
        t = '10 JAN ' + dt[0]
        return t
    elif(dt.__len__() == 2):
        t = '10 ' + dt[0] + ' ' + dt[1]
        return t


def US41_list(gedout):
    fixedDates =[]
    indvBD = []
    famBD = []
    for key in gedout["individuals"]:
        if 'BIRT' in gedout["individuals"][key]:
            if doesDateneedModification(gedout["individuals"][key]['BIRT']):
                 indvBD.append([key, fixDates(gedout["individuals"][key]['BIRT'])])

        if 'DEAT' in gedout["individuals"][key]:
            if doesDateneedModification(gedout["individuals"][key]['DEAT']):
                 indvBD.append([key, fixDates(gedout["individuals"][key]['DEAT'])])

    for key in gedout["families"]:
        if doesDateneedModification(gedout["families"][key]['MARR']):
            famBD.append([key, fixDates(gedout["families"][key]['MARR'])])

    if (indvBD.__len__() >0 or famBD.__len__() >0):
        fixedDates.append('US41: All Dates Made Valid:')
    if (indvBD.__len__() >0):
        fixedDates.append(indvBD)

    if (famBD.__len__() >0):
        fixedDates.append(famBD)

    if fixedDates.__len__() == 0:
        fixedDates.append("US41: All Dates Already Valid")

    return fixedDates;

def isLeapYear(yr):
    if (yr % 400) == 0:
        return True
    if (yr % 100) == 0:
        return False
    if (yr % 4) == 0:
        return True
    return False;

def checkDates(date):
    dayinMonths = ['31', "JAN", '31', "MAR",
                   '30', "APR", '31', "MAY",
                   '30', "JUN", '31', "JUL",
                   '31', "AUG", '30', "SEP",
                   '31', "OCT", '30', "NOV",
                   '31', "DEC"]

    tempDT = date.split(" ")
    if tempDT[1] != "FEB":
        for i in range(dayinMonths.__len__()):
            if tempDT[1] == dayinMonths[i]:
                if (int(tempDT[0]) > 0 and int(tempDT[0]) <= int(dayinMonths[i - 1])):
                    return True

    elif isLeapYear(int(tempDT[2])):
        if (int(tempDT[0]) > 0 and int(tempDT[0]) <= 29):
            return True
    else:
        if (int(tempDT[0]) > 0 and int(tempDT[0]) <= 28):
            return True
    return False


#check all dates are allowed
def US42_list(gedout):
    badDates = []
    indvBD = []
    famBD = []
    for key in gedout["individuals"]:
        if 'BIRT' in gedout["individuals"][key]:
            if checkDates(gedout["individuals"][key]['BIRT']) == False:
                indvBD.append([key, gedout["individuals"][key]['BIRT']])

        if 'DEAT' in gedout["individuals"][key]:
            if checkDates(gedout["individuals"][key]['DEAT']) == False:
                indvBD.append([key, gedout["individuals"][key]['DEAT']])

    for key in gedout["families"]:
        if checkDates(gedout["families"][key]['MARR']) == False:
            famBD.append([key, gedout["families"][key]['MARR']])

    if (indvBD.__len__() >0 or famBD.__len__() >0):
        badDates.append('US42: Invalid dates:')
    if (indvBD.__len__() >0):
        badDates.append(indvBD)

    if (famBD.__len__() >0):
        badDates.append(famBD)

    if (badDates.__len__() == 0):
        badDates.append("US42: All Dates Valid")
    return badDates



