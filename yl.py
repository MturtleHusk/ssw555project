from datetime import date
from datetime import datetime

# US17: no marriage to descendant
def us17(ged):
    out = []

    # retrieve the children's IDs of the individual
    def get_children(ind):
        children = []
        for f_id in ged["families"]:
            f = ged["families"][f_id]
            if f["HUSB"] != ind and f["WIFE"] != ind:
                continue
            if "CHIL" not in f:
                continue
            children += f["CHIL"]
        return children

    # retrieve the descendants' IDs of the individual
    def get_descendants(ind):
        descendants = [ind]
        i = 0
        while i < len(descendants):
            descendants += get_children(descendants[i])
            i += 1
        return descendants

    for f_id in ged["families"]:
        # get the husband and wife ID
        family = ged["families"][f_id]
        husband_id = family["HUSB"]
        wife_id = family["WIFE"]

        # check if the husband of wife is the descendant of another
        if husband_id in get_descendants(wife_id):
            out.append("Error US17: {} ({}) marries her descendants."
                       .format(ged["individuals"][wife_id]["NAME"], wife_id))
        if wife_id in get_descendants(husband_id):
            out.append("Error US17: {} ({}) marries his descendants."
                       .format(ged["individuals"][husband_id]["NAME"], husband_id))

    return out


# US18: siblings should not marry
def us18(ged):
    out = []

    # retrieve all the siblings' IDs of the individual
    def get_siblings(ind):
        siblings = []

        for f_id in ged["families"]:
            family = ged["families"][f_id]
            if "CHIL" not in family:
                continue
            if ind in family["CHIL"]:
                for child in family["CHIL"]:
                    if child == ind:
                        continue
                    siblings.append(child)

        return siblings

    for f_id in ged["families"]:
        # get the husband and wife ID
        family = ged["families"][f_id]
        husband_id = family["HUSB"]
        wife_id = family["WIFE"]

        if husband_id in get_siblings(wife_id):
            out.append("Error US18: {} ({}) should not marry {} ({}), because they are siblings."
                       .format(ged["individuals"][husband_id]["NAME"], husband_id,
                               ged["individuals"][wife_id]["NAME"], wife_id))

    return out


# US07: less than 150 years old
def us07(ged):
    out = []

    for ind_id, individual in ged["individuals"].items():
        birth_date = datetime.strptime(individual["BIRT"], "%d %b %Y").date()
        death_date = (datetime.strptime(individual["DEAT"], "%d %b %Y").date()
                      if "DEAT" in individual else date.today())
        if not dates_within(birth_date, death_date, 150, 'years'):
            out.append("Anomaly US07: {} ({}) is more than 150 years old."
                       .format(individual["NAME"], ind_id))

    return out


# US08: birth before marriage of parents
def us08(ged):
    out = []

    for f_id, family in ged["families"].items():
        # if there is no child in this family
        if "CHIL" not in family:
            continue

        # get the marriage date and divorce date (if divorced) of this family
        marriage_date = datetime.strptime(family["MARR"], "%d %b %Y").date()
        divorce_date = None
        if "DIV" in family:
            divorce_date = datetime.strptime(family["DIV"], "%d %b %Y").date()

        for child in family["CHIL"]:
            # get the birth date of this child
            birth_date = datetime.strptime(ged["individuals"][child]["BIRT"], "%d %b %Y").date()

            if birth_date < marriage_date:
                out.append("Anomaly US08: {} ({}) was born before marriage of parents.".
                           format(ged["individuals"][child]["NAME"], child))
            elif divorce_date and (not dates_within(birth_date, divorce_date, 9, "months")):
                out.append("Anomaly US08: {} ({}) was born after more than 9 months of divorce of parents.".
                           format(ged["individuals"][child]["NAME"], child))

    return out


# US16: All male members of a family should have the same last name
def us16(ged):
    out = []

    for f_id, family in ged["families"].items():
        # get all members in this family
        members = [family["HUSB"], family["WIFE"]]
        if "CHIL" in family:
            members += family["CHIL"]

        family_last_name = None
        for m in members:
            individual = ged["individuals"][m]
            if individual["SEX"] != "M":
                continue
            last_name = individual["NAME"].split(" ")[-1]
            if not family_last_name:
                family_last_name = last_name
                continue
            if last_name == family_last_name:
                continue
            out.append("Anomaly US16: Not all male members of family {} have the same last name."
                       .format(f_id))

    return out


# US20: Aunts and uncles should not marry their nieces or nephews
def us20(ged):
    out = []

    # get parents
    def get_parents(ind):
        for _, family in ged["families"].items():
            if ("CHIL" in family) and (ind in family["CHIL"]):
                return [family["HUSB"], family["WIFE"]]
        return None

    # get aunts or uncles
    def get_relatives(ind, relative):
        conversion = {"aunts": "F", "uncles": "M"}
        relatives = []

        # find parents' sisters or brothers
        parents = get_parents(ind)
        if not parents:
            return relatives
        for parent in parents:
            for _, family in ged["families"].items():
                if ("CHIL" in family) and (parent in family["CHIL"]):
                    for child in family["CHIL"]:
                        if child == parent:
                            continue
                        if ged["individuals"][child]["SEX"] == conversion[relative]:
                            relatives.append(child)

        return relatives

    for f_id, family in ged["families"].items():
        husband = family["HUSB"]
        wife = family["WIFE"]

        if wife in get_relatives(husband, "aunts"):
            out.append("Anomaly US20: {} ({}) marries her nephew {} ({})"
                       .format(ged["individuals"][wife]["NAME"], wife, ged["individuals"][husband]["NAME"], husband))

        if husband in get_relatives(wife, "uncles"):
            out.append("Anomaly US20: {} ({}) marries his nieces {} ({})"
                       .format(ged["individuals"][husband]["NAME"], husband, ged["individuals"][wife]["NAME"], wife))

    return out


def dates_within(dt1, dt2, limit, units):

    '''
    return True if dt1 and dt2 are within limit units, where:
    dt1, dt2 are instances of datetime
    limit is a number units is a string in ('days', 'months', 'years')
    '''

    conversion = {'days':1, 'months':30.4, 'years':365.25}
    return (abs((dt1 - dt2).days) / conversion[units]) <= limit
