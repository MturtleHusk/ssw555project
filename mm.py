from ged import compare_dates

#marriage before birth
def us02(ged):
    out = []
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

    for key in ged['families']:
        fam = ged['families'][key]

        if not 'DIV' in fam or not 'MARR' in fam or not 'HUSB' in fam or not 'WIFE' in fam:
            continue

        if compare_dates(fam['MARR'], fam['DIV']) == 1:
            husb = ged['individuals'][fam['HUSB']]['NAME'] if fam['HUSB'] in ged['individuals'] and 'NAME' in ged['individuals'][fam['HUSB']] else '<Husband not found>'
            wife = ged['individuals'][fam['WIFE']]['NAME'] if fam['WIFE'] in ged['individuals'] and 'NAME' in ged['individuals'][fam['WIFE']] else '<Wife not found>'

            out.append('Error US04: Divorce date of {} and {} ({}, {}) occurs before marriage date'.format(husb, wife, fam['HUSB'], fam['WIFE']))
    
    return out

#duplicate IDs
def us22(ged):
    out = []

    for type in ['individuals', 'families']:
        for key in ged[type]:
            if 'dup' in ged[type][key] and len(ged[type][key]['dup']) > 0:
                out.append('Error US22: Duplicate ID {} in {}'.format(key, type))
            
    return out

#duplicate name/birthday pairs
def us23(ged):
    out = []

    store = []
    ids = []

    for id in ged['individuals']:
        indi = ged['individuals'][id]

        if not 'NAME' in indi or not 'BIRT' in indi:
            continue

        cstr = '{} {}'.format(indi['NAME'], indi['BIRT'])
        
        if cstr in store:
            out.append('Error US23: Duplicate name/birthday pair (IDs {} and {})'.format(ids[store.index(cstr)], id))
        else:
            store.append(cstr)
            ids.append(id)
    
    return out

#no more than 5 births at the same time
def us14(ged):
    out = []
    store = {}

    for id in ged['individuals']:
        indi = ged['individuals'][id]

        if not 'FAMC' in indi:
            continue

        cstr = '{} {}'.format(indi['FAMC'], indi['BIRT'])

        if not cstr in store:
            store[cstr] = 1
        else:
            store[cstr] += 1
            
            if store[cstr] > 5:
                out.append('Anomaly US14: Family {} contains more than five siblings born on the same day'.format(indi['FAMC']))

    return out

#no more than 15 siblings in a single family
def us15(ged):
    out = []

    for id in ged['families']:
        fam = ged['families'][id]
        if not 'CHIL' in fam:
            continue
        
        if len(fam['CHIL']) > 15:
            out.append('Anomaly US15: Family {} contains more than 15 siblings'.format(id))

    return out
