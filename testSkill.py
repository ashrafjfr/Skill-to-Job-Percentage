import csv
import json

# converting proj skills json into dictionary
proj_skills = open("projectskills-infinitysr1.json")
proj_skills_dict = json.load(proj_skills)


def rating_mod(rating):
    if rating == 10:
        return 3
    elif rating == 5:
        return 2
    elif rating == 1:
        return 1
    else:
        return 0


def make_tal_skills(taltext):
    taldata = json.loads(taltext)
    tal = {}
    for index in range(0, len(taldata['data']['skills'])):
        tal[taldata['data']['skills'][index]['skill']] = taldata['data']['skills'][index]['rating']
    return tal


def score(talentkey, jobkey):
    sumEssential = len(proj_skills_dict[jobkey]['essentials']) * 3
    sumElective = len(proj_skills_dict[jobkey]['electives']) * 3
    talEssential = 0
    talElective = 0
    for i in range(0, len(proj_skills_dict[jobkey]['essentials'])):
        skill = proj_skills_dict[jobkey]['essentials'][i]
        if skill in tal_skills_dict[talentkey]:
            talEssential += rating_mod(tal_skills_dict[talentkey][skill])
        else:
            talEssential += 0
    for j in range(0, len(proj_skills_dict[jobkey]['electives'])):
        skill = proj_skills_dict[jobkey]['electives'][j]
        if skill in tal_skills_dict[talentkey]:
            talElective += rating_mod(tal_skills_dict[talentkey][skill])
        else:
            talElective += 0
    try:
        ratioEssential = talEssential / sumEssential
    except ZeroDivisionError:
        ratioEssential = 0
    try:
        ratioElective = talElective / sumElective
    except ZeroDivisionError:
        ratioElective = 0
    try:
        final_score = (ratioEssential * 2 + ratioElective) * 100 / 3
    except ZeroDivisionError:
        final_score = 0

    return final_score


with open("proj_choices_inf_1.csv") as tal_data:
    tal_skills = csv.reader(tal_data)
    next(tal_skills)
    tal_proj_dict = {rows[0]: rows[1:6] for rows in tal_skills}

with open("inf1talents.txt") as tal_data:
    tal_skills = csv.reader(tal_data, delimiter='\t')
    next(tal_skills)
    tal_skills_dict = {rows[0]: make_tal_skills(rows[1]) for rows in tal_skills}


with open('inf_1_scores.csv', 'w', newline='') as outputcsv:
    headers = ['Talent ID', 'Project ID', 'Score']
    csvwriter = csv.DictWriter(outputcsv, fieldnames=headers)
    csvwriter.writeheader()
    for key in tal_proj_dict.keys():
        talentkey = key
        for i in range(0,5):
            jobkey = tal_proj_dict[talentkey][i]
            if jobkey == 'NIL':
                csvwriter.writerow({'Talent ID': talentkey, 'Project ID': jobkey, 'Score': 0})
                continue
            else:
                csvwriter.writerow({'Talent ID':talentkey, 'Project ID': jobkey, 'Score': round(score(talentkey,jobkey),1)})

# for key in tal_proj_dict.keys():
#     talentkey = key
#     for i in range(0, 5):
#         jobkey = tal_proj_dict[talentkey][i]
#         if jobkey == 'NIL':
#             print(talentkey, end=' ')
#             print(jobkey, end=' ')
#             print(0)
#             continue
#         else:
#             print(talentkey, end=' ')
#             print(jobkey, end=' ')
#             print(round(score(talentkey, jobkey), 1))

# test for push