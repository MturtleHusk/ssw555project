from ged import compare_dates, date_difference
#sprint 1: stories 5 and 10
#sprint 2: stories 6 and 9


#Validation check for Marriage date before death date
#Individual cannot have died before they got married
def us05(ged):
    out = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]
        
        #Ensure that each tag is present 'families'
        if not 'HUSB' in family or not 'WIFE' in family or not 'MARR' in family:
            continue

        #Search for HUSB or WIFE tag in family lib
        for person in ['HUSB','WIFE']:

            #check if family member is apart of lib for individuals
            if family[person] in ged['individuals']:
                individual = ged['individuals'][family[person]]
                if 'DEAT' in individual:

                    #compare date stored for 'MARR' with date for 'DEAT'
                    compare = compare_dates(family['MARR'], individual['DEAT'])

                    if compare == 1:
                        out.append('Error US05: Death date of {} ({}) occurs before marriage date'
                                   .format(individual['NAME'],family[person]))
    return out

#Validation Check to ensure divorce date happens before death
def us06(ged):
    out = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]
        
        #check for appropriate tags
        if not 'HUSB' in family or not 'WIFE' in family or not 'DIV' in family or not 'DIV' in family:
            continue

        #chech for Husb and Wife tags
        for person in ['HUSB','WIFE']:

            #check if family member is apart of lib for individuals
            if family[person] in ged['individuals']:
                individual = ged['individuals'][family[person]]
                if 'DEAT' in individual:

                    #compare date stored for 'DIV' with date for 'DEAT'
                    compare = compare_dates(family['DIV'], individual['DEAT'])

                    if compare == 1:
                        out.append('Error US05: Death date of {} ({}) occurs before divorce date'
                                   .format(individual['NAME'],family[person]))
    return out

#Validation check to ensure borth date takes place before death date
def us09(ged):
    out = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]
        
        #check for appropriate tags
        if not 'HUSB' in family or not 'WIFE' in family or not 'DIV' in family:
            continue

        #chech for Husb and Wife tags
        for person in ['HUSB','WIFE']:

            if family[person] in ged['individuals']:
                individual = ged['individuals'][family[person]]

                if 'DEAT' in individual:

                    #compare date stored for 'BIRT' with date for 'DEAT'
                    compare = compare_dates(family['BIRT'], individual['DEAT'])

                    if compare == 1:
                        out.append('Error US05: Death date of {} ({}) occurs before birth date'
                                   .format(individual['NAME'],family[person]))
    return out

#Validation check to ensure that no marriages occur with a partner under 14 occur
def us10(ged):

    output = []
    for ID in ged['families']:
        family = ged['families'][ID]

        if not family['HUSB'] in ged['individuals'] or not family['WIFE'] in ged['individuals']:
            continue

        husband = ged['individuals'][family['HUSB']]['NAME'] 
        wife = ged['individuals'][family['WIFE']]['NAME'] 
            
        #check for a marriage
        if husband is not None and wife is not None and 'MARR' in family:

            for person in ['HUSB','WIFE']:
                if family[person] in ged['individuals']:
                    individual = ged['individuals'][family[person]]

                    if 'BIRT' in individual:
                    #finds number of days between marriage date and birth date of individual
                        date_diff = date_difference(individual['BIRT'], family['MARR'])

                    #14 years = 5110 days
                        if date_diff < 5110:
                            output.append('Error US10: Marriage of {} and {} ({}, {}) occurs with a parter under age 14'
                                          .format(husband, wife, family['HUSB'], family['WIFE']))

    return output
