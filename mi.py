from ged import compare_dates, date_difference

#Validation check for Marriage date before death date
#Individual cannot have died before they got married
def us05(ged):
    
    output = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]

        #Ensure that each tag is present 'families'
        if 'WIFE' in family and 'HUSB' in family and 'MARR' in family:
            
            #Search for 'HUSB' tag in 'individuals' present in 'families'
            if family['HUSB'] in ged['individuals']:
                individual = ged['individuals'][family['HUSB']]

                #check for an individual with a 'DEAT' tag 
                #who also has has their 'NAME' tage in 'individuals'
                if 'DEAT' in individual and 'NAME' in individual:

                	#compare date stored for 'MARR' with date for 'DEAT'
                    check = compare_dates(family['MARR'], individual['DEAT'])
                    
                    if check == 1:
                        output.append('Error US05: Death date of {} ({}) occurs before marriage date'
                                .format(individual['NAME'], family['HUSB']))

            #Search for 'WIFE' tag in 'individuals' present in 'families'
            if family['WIFE'] in ged['individuals']:
                individual = ged['individuals'][family['WIFE']]
                if 'DEAT' in individual and 'NAME' in individual:

                	#compare date stored for 'MARR' with date for 'DEAT'
                    check = compare_dates(family['MARR'], individual['DEAT'])

                    if check == 1:
                        output.append('Error US05: Death date of {} ({}) occurs before marriage date'
                                .format(individual['NAME'], family['WIFE']))

    
    return output

#Validation check to ensure that no marriages with a partner under 14 occur
def us10(ged):

    output = []
    for ID in ged['families']:
        family = ged['families'][ID]
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
