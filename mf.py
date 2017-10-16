# i pledge my honor that i have abided by the stevens Honor System ~MF
import ged
from datetime import date
from datetime import datetime

#print married
def US30(gedout):

    couples = []
    for key in gedout["families"]:
        entry = gedout["families"][key]
        couples.append([ entry["HUSB"], entry["WIFE"]])

    print(couples)

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

    print(couples)

    if len(couples) == 0:
        couples.append("US30: There are no married couples")
        return couples
    else:
        x = "US30: list of married couples - [  "
        ret = []
        for fams in couples:
            x += "[ "
            for peeps in fams:
                x += peeps + " "
            x += "] "
        x += " ]"
        ret.append(x)
        return ret

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

            print(tempDT[0] +"-" + tempDT[1] + "-"+ tempDT[2])

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

        print(currdate)
        print(tempD)
        diff = delta.days
        print(diff)
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