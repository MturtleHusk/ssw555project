from datetime import date
from datetime import datetime


# US17: no marriage to descendant
def us17(ged):
    out = []

    for f_id in ged["families"]:
        # get the husband and wife ID
        family = ged["families"][f_id]
        husband_id = family["HUSB"]
        wife_id = family["WIFE"]

        # check if the husband of wife is the descendant of another
        if husband_id in get_descendants(ged, wife_id):
            out.append("Error US17: {} ({}) marries her descendants."
                       .format(ged["individuals"][wife_id]["NAME"], wife_id))
        if wife_id in get_descendants(ged, husband_id):
            out.append("Error US17: {} ({}) marries his descendants."
                       .format(ged["individuals"][husband_id]["NAME"], husband_id))

    return out


# US18: siblings should not marry
def us18(ged):
    out = []

    for f_id in ged["families"]:
        # get the husband and wife ID
        family = ged["families"][f_id]
        husband_id = family["HUSB"]
        wife_id = family["WIFE"]

        if is_siblings(ged, husband_id, wife_id):
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

    # get aunts or uncles
    def get_relatives(ind, relative):
        conversion = {"aunts": "F", "uncles": "M"}
        relatives = []

        # find parents' sisters or brothers
        parents = get_parents(ged, ind)
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


# us19: First cousins should not marry one another
def us19(ged):
    out = []

    for _, family, in ged["families"].items():
        husband = family["HUSB"]
        wife = family["WIFE"]

        # get husband's and wife's parents
        h_parents = get_parents(ged, husband)
        w_parents = get_parents(ged, wife)

        # check if one of husband's parents and one of wife's parents are siblings
        if (not h_parents) or (not w_parents):
            continue

        if (is_siblings(ged, h_parents[0], w_parents[0])
                or is_siblings(ged, h_parents[0], w_parents[1])
                or is_siblings(ged, h_parents[1], w_parents[0])
                or is_siblings(ged, h_parents[1], w_parents[1])):
            out.append("Anomaly US19: {} ({}) marries his first cousin {} ({})."
                       .format(ged["individuals"][husband]["NAME"], husband, ged["individuals"][wife]["NAME"], wife))

    return out


# us28: List siblings in families by decreasing age, i.e. oldest siblings first
def us28_list(ged):
    out = []

    for f_id, family in ged["families"].items():
        if "CHIL" not in family:
            continue
        children = []
        for child in family["CHIL"]:
            children.append([child, ged["individuals"][child]["NAME"], ged["individuals"][child]["BIRT"]])

        children.sort(
            key=lambda child: datetime.strptime(child[2], "%d %b %Y").date()
        )
        out.append([f_id] + children)

    return ["US28: List siblings in families by decreasing age:", out]


# check if two dates are in the given limitation
def dates_within(dt1, dt2, limit, units):
    conversion = {'days': 1, 'months': 30.4, 'years': 365.25}
    return (abs((dt1 - dt2).days) / conversion[units]) <= limit


# get parents
def get_parents(ged, ind):
    for _, family in ged["families"].items():
        if ("CHIL" in family) and (ind in family["CHIL"]):
            return [family["HUSB"], family["WIFE"]]
    return None


# retrieve the children's IDs of the individual
def get_children(ged, ind):
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
def get_descendants(ged, ind):
    descendants = [ind]
    i = 0
    while i < len(descendants):
        descendants += get_children(ged, descendants[i])
        i += 1
    return descendants


# retrieve all the siblings' IDs of the individual
def get_siblings(ged, ind):
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


# check if two individuals are siblings
def is_siblings(ged, ind1, ind2):
    for _, family, in ged["families"].items():
        if ("CHIL" in family) and (ind1 in family["CHIL"] and ind2 in family["CHIL"]):
            return True

    return False
