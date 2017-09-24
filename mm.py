from ged import compare_dates

#marriage before birth
def us02(ged):
    out = []
    if len(ged['families']) > 0:
        for key in ged['families']:
            fam = ged['families'][key]
            
            if not 'MARR' in fam or not 'HUSB' in fam or not 'WIFE' in fam:
                continue
            
            for person in ['HUSB','WIFE']:
                if fam[person] in ged['individuals']:
                    indi = ged['individuals'][fam[person]]
                
                    if 'BIRT' in indi:
                        cmpr = compare_dates(fam['MARR'], indi['BIRT'])
                        
                        if cmpr == -1:
                            out.append('Error US02: Birth date of {} ({}) occurs after {} marriage date'.format(indi['NAME'] if 'NAME' in indi else '<name not found>', fam[person], 'his' if person == 'HUSB' else 'her'))
    return out

#divorce before marriage
def us04(ged):
    out = []
    if len(ged['families']) > 0:
        for key in ged['families']:
            fam = ged['families'][key]

            if not 'DIV' in fam or not 'MARR' in fam or not 'HUSB' in fam or not 'WIFE' in fam:
                continue

            if compare_dates(fam['MARR'], fam['DIV']) == 1:
                husb = ged['individuals'][fam['HUSB']]['NAME'] if fam['HUSB'] in ged['individuals'] and 'NAME' in ged['individuals'][fam['HUSB']] else '<Husband not found>'
                wife = ged['individuals'][fam['WIFE']]['NAME'] if fam['WIFE'] in ged['individuals'] and 'NAME' in ged['individuals'][fam['WIFE']] else '<Wife not found>'

                out.append('Error US04: Divorce date of {} and {} ({}, {}) occurs before marriage date'.format(husb, wife, fam['HUSB'], fam['WIFE']))
    return out
