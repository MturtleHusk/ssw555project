from os import listdir
from os.path import isfile, join

directory = "."
ged = ""

for file in listdir(directory):
    if not isfile(join(directory, file)):
        continue
    
    if file.split(".")[-1] == "ged":
        ged = open(file,"r").read()
        break

if len(ged) > 0:
    gedlines = ged.split("\n")
    records = [["0","INDI"],["1","NAME"],["1","SEX"],["1","BIRT"],["1","DEAT"],["1","FAMC"],["1","FAMS"],["0","FAM"],["1","MARR"],["1","HUSB"],["1","WIFE"],["1","CHIL"],["1","DIV"],["2","DATE"],["0","HEAD"],["0","TRLR"],["0","NOTE"]]
    
    for line in gedlines:
        if len(line) == 0:
            continue
        
        level = ""
        tag = ""
        valid = ""
        args = ""
        
        attr = line.split(" ")
        
        if attr[0] == "0" and (attr[-1] == "INDI" or attr[-1] == "FAM"):
            level = 0
            tag = attr[-1]
            valid = "Y"
            args = " ".join(attr[1:-1])
        else:
            level = attr[0]
            tag = attr[1]
            valid = "Y" if ([level,tag] in records) else "N"
            args = " ".join(attr[2:])
            
        print("--> {}".format(line))
        print("<-- {}|{}|{}|{}".format(level, tag, valid, args))
        
