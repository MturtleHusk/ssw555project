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
            # print("Error US17: {} ({}) marries her descendants."
            #       .format(ged["individuals"][wife_id]["NAME"], wife_id))
        if wife_id in get_descendants(husband_id):
            out.append("Error US17: {} ({}) marries his descendants."
                       .format(ged["individuals"][husband_id]["NAME"], husband_id))
            # print("Error US17: {} ({}) marries his descendants."
            #       .format(ged["individuals"][husband_id]["NAME"], husband_id))

    return out


# US18: siblings should not marry
def us18(ged):
    out = []

    # retrieve all the siblings' IDs of the individual
    def get_siblings(ind):
        siblings = []

        # get the parents' IDs
        # father_id = ""
        # mother_id = ""
        # for f_id in ged["families"]:
        #     family = ged["families"][f_id]
        #     if ind in family["CHIL"]:
        #         father_id = family["HUSB"]
        #         mother_id = family["WIFE"]
        #         break
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
        # print("Error US18: {} ({}) should not marry {} ({}), because they are siblings."
        #     .format(ged["individuals"][husband_id]["NAME"], husband_id, ged["individuals"][wife_id]["NAME"], wife_id))

    return out
