from os import listdir
from os.path import isfile, join
from prettytable import PrettyTable
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import traceback
import yl

#All valid records. Format is [string level, string tag, string[] valid parent records]
records = [
    ["0","INDI",[""]],
    ["1","NAME",["INDI"]],
    ["1","SEX",["INDI"]],
    ["1","BIRT",["INDI"]],
    ["1","DEAT",["INDI"]],
    ["1","FAMC",["INDI"]],
    ["1","FAMS",["INDI"]],
    ["0","FAM",[""]],
    ["1","MARR",["FAM"]],
    ["1","HUSB",["FAM"]],
    ["1","WIFE",["FAM"]],
    ["1","CHIL",["FAM"]],
    ["1","DIV",["FAM"]],
    ["2","DATE",["BIRT","DEAT","DIV","MARR"]],
    ["0","HEAD",[""]],
    ["0","TRLR",[""]],
    ["0","NOTE",[""]]
]
#Tags that can have multiple values go here
multi = ["CHIL"]





#Given a tag name, returns the record entry
def record_from_tag(tag):
    for record in records:
        if record[1] == tag:
            return record

    return []





#Returns an int value signifying the comparison between two dates
#-1 = first date before second date, 0 = dates are equal, 1 = first date after second date, -2 = error parsing dates
def compare_dates(d1, d2, form="%d %b %Y"):
    try:
        dt1 = datetime.strptime(d1, form)
        dt2 = datetime.strptime(d2, form)

        return -1 if dt1 < dt2 else (0 if dt1 == dt2 else 1)
    except Exception as e:
        traceback.print_exc()
        return -2




#Prints the contents of a .ged file in a directory (default current working directory)
def read_ged(filename='test.ged'):
    if len(filename) == 0:
        for file in listdir('./'):
            if not isfile(file):
                continue
            if file.split('.')[-1] == 'ged':
                return open(file, 'r').read()
    else:
        if not isfile(filename):
            return ''

        if filename.split('.')[-1] == 'ged':
            ged = open(filename, 'r').read()
            return ged
    
    return ''






#Parse GEDCOM input into a usable format
def parse_ged(gedlines):
    if len(gedlines) == 0:
        return

    #Parses a single GEDCOM line, returns an array with the info in the form [level, tag, arguments]
    def parse_line(gedline):
        if len(gedline) == 0:
            return

        level = ""
        tag = ""
        args = ""
        
        attr = gedline.split(" ")
        if attr[0] == "0" and (attr[-1] == "INDI" or attr[-1] == "FAM"):
            level = "0"
            tag = attr[-1]
            args = " ".join(attr[1:-1])
        else:
            level = attr[0]
            tag = attr[1]
            args = " ".join(attr[2:])
            
        return [level, tag, args]

    #Given a line number, scans the previous lines to find the parent record (i.e. the first record with a level of 1 less than the current)
    def find_parent(linenum):
        if linenum < 0 or linenum >= len(gedlines):
            return

        info = parse_line(gedlines[linenum])

        for i in range(linenum-1, -1, -1):
            if int(parse_line(gedlines[i])[0]) == int(info[0]) - 1:
                return gedlines[i]

        return gedlines[linenum]

    #Given a line number, scans the previous lines to find the first with level 0
    def find_level0(linenum):
        if linenum < 0 or linenum >= len(gedlines):
            return
        for i in range(linenum-1, -1, -1):
            if (parse_line(gedlines[i])[0] == "0"):
                return gedlines[i]
        
        return gedlines[linenum]



    output = {
        "individuals": {},
        "families": {}
    }
    check = [[a[0], a[1]] for a in records]


    
    for i in range(0, len(gedlines)):
        line = gedlines[i]
        if len(line) == 0:
            continue
        
        current = parse_line(line)

        if current[0] == "0":
            if current[1] != "INDI" and current[1] != "FAM":
                continue
            
            ind = "individuals" if current[1] == "INDI" else "families"
            output[ind][current[2]] = {}
        elif current[0] == "1" or current[0] == "2":
            parent = parse_line(find_parent(i))

            if current[0] == "1":
                ind = "individuals" if parent[1] == "INDI" else "families"

                #Make sure that the entry is valid and under a correct valid parent record
                if (not [current[0], current[1]] in check) or (not parent[1] in record_from_tag(current[1])[2]) or (parent[1] != "INDI" and parent[1] != "FAM"):
                    continue

                #For some reason, the 0 <> INDI/FAM record didn't initialize an entry in the dictionary
                if not parent[2] in output[ind]:
                    continue
                
                #If there can be multiple entries of the same tag, we store them in an array
                if current[1] in multi:
                    if current[1] in output[ind][parent[2]]:
                        output[ind][parent[2]][current[1]].append(current[2])
                    else:
                        output[ind][parent[2]][current[1]] = [current[2]]
                else:
                    output[ind][parent[2]][current[1]] = current[2]
            elif current[0] == "2":
                zero = parse_line(find_level0(i))
                ind = "individuals" if zero[1] == "INDI" else "families"

                if not [current[0], current[1]] in check:
                    continue

                output[ind][zero[2]][parent[1]] = current[2]
    return output





def validate_ged(ged):
    if not 'individuals' in ged or not 'families' in ged:
        return

    out = []

    #check us02 and us04
    import mm 
    out += mm.us02(ged)
    out += mm.us04(ged)

    # check us17
    out += yl.us17(ged)

    # check us18
    out += yl.us18(ged)


    #---------------#
    # add code here #
    #---------------#

    return out






#Pretty print the GEDCOM after parsing
def pretty_print(gedout):
    if "individuals" in gedout and len(gedout["individuals"]) > 0:
        ix = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        rows = []

        for key in gedout["individuals"]:
            entry = gedout["individuals"][key]

            row_id = key
            row_name = entry["NAME"] if "NAME" in entry else "N/A"
            row_gender = entry["SEX"] if "SEX" in entry else "N/A"
            row_child = ("{'" + entry["FAMC"] + "'}") if "FAMC" in entry else "N/A"
            row_spouse = ("{'" + entry["FAMS"] + "'}") if "FAMS" in entry else "N/A"
            row_alive = "False" if "DEAT" in entry else "True"

            row_bday = "N/A"
            row_age = "N/A"
            row_death = "N/A"

            if "BIRT" in entry:
                try:
                    #Format birthday to YYYY-MM-DD
                    bday_time = datetime.strptime(entry["BIRT"], "%d %b %Y")
                    row_bday = bday_time.strftime("%Y-%m-%d")

                    #Calculate age
                    row_age = relativedelta(datetime.combine(date.today(), datetime.min.time()), bday_time).years

                except:
                    pass
            if "DEAT" in entry:
                try:
                    #Format death date to YYYY-MM-DD
                    death_time = datetime.strptime(entry["DEAT"], "%d %b %Y")
                    row_death = death_time.strftime("%Y-%m-%d")
                except:
                    pass

            rows.append([row_id, row_name, row_gender, row_bday, row_age, row_alive, row_death, row_child, row_spouse])
        
        #Sort the rows by their IDs and then add them to the PrettyTable object
        sorted(rows,key=lambda row: int(row[0][1:]))
        for row in rows:
            ix.add_row(row)

        print("Individuals")
        print(ix)
        

    if "families" in gedout and len(gedout["families"]) > 0:
        fx = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
        rows = []

        for key in gedout["families"]:
            entry = gedout["families"][key]

            row_id = key
            row_husband_id = entry["HUSB"] if "HUSB" in entry else "N/A"
            row_wife_id = entry["WIFE"] if "WIFE" in entry else "N/A"
            
            row_children = "N/A"
            if "CHIL" in entry:
                row_children = "{"
                for child in entry["CHIL"]:
                    row_children += "'{}',".format(child)
                row_children = row_children[:-1]
                row_children += "}"
            
            row_husband_name = "N/A"
            if row_husband_id != "N/A":
                if row_husband_id in gedout["individuals"] and "NAME" in gedout["individuals"][row_husband_id]:
                    row_husband_name = gedout["individuals"][row_husband_id]["NAME"]
            
            row_wife_name = "N/A"
            if row_wife_id != "N/A":
                if row_wife_id in gedout["individuals"] and "NAME" in gedout["individuals"][row_wife_id]:
                    row_wife_name = gedout["individuals"][row_wife_id]["NAME"]

            row_married = "N/A"
            if "MARR" in entry:
                try:
                    marr_time = datetime.strptime(entry["MARR"], "%d %b %Y")
                    row_married = marr_time.strftime("%Y-%m-%d")
                except:
                    pass
            
            row_divorced = "N/A"
            if "DIV" in entry:
                try:
                    div_time = datetime.strptime(entry["DIV"], "%d %b %Y")
                    row_divorced = div_time.strftime("%Y-%m-%d")
                except:
                    pass
            rows.append([row_id, row_married, row_divorced, row_husband_id, row_husband_name, row_wife_id, row_wife_name, row_children])

        #Sort the rows by their IDs and then add them to the PrettyTable object
        sorted(rows,key=lambda row: int(row[0][1:]))
        for row in rows:
            fx.add_row(row)

        print('Families')
        print(fx)

#credit to dideler from https://gist.github.com/dideler/2395703
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts
    
#Main function 
if __name__ == "__main__":
    filename = ''

    from sys import argv
    args = getopts(argv)
    
    if len(args) > 0 and '-f' in args:
        filename = args['-f']
    
    raw = read_ged() if len(filename) == 0 else read_ged(filename)

    if len(raw) > 0:
        rawlines = raw.split('\n')
        ged = parse_ged(rawlines)
        errs = validate_ged(ged)

        pretty_print(ged)
        print('')
        
        if len(errs) > 0:
            print('Errors/Anomalies:')
            for s in errs:
                print(' ' + s)
        else:
            print('No errors/anomalies.')
