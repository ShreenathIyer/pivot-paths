'''

Reduce the extracted data to a tractable size

'''


import json
import sys
import random

sys.setrecursionlimit(3000)

# Reading from the dump file to reduce data
with open('singleauthordump-1.json') as reader:
    val = json.load(reader)

newrec = [{}, {}, {}, []]
allowed_pap = set()
allowed_con = set()
allowed_auth = set()
search_auth = set()

total_count = 0
referred = set()
cited = set()
already_added = set()

overall_citations = {}

# def keep_on_adding(each, orig, dupl, count):
#     if count <= 10:
#         print(each)
#         for it in orig:
#             if it == each and each not in already_added:
#                 new_dict = {}
#                 new_dict[it] = orig[it].copy()
#                 new_dict[it]["tags"] = {}
#                 new_dict[it]["authors"] = {}
#                 new_dict[it]["items"] = {}
#                 new_dict[it]["refs_"] = {}
#                 new_dict[it]["cites_"] = {}
#
#                 for auth in orig[it]["authors"]:
#                     if auth in allowed_auth:
#                         new_dict[it]["authors"][auth] = 1
#
#                 for tag in orig[it]["tags"]:
#                     if tag in allowed_con:
#                         new_dict[each]["tags"][tag] = 1
#
#                 refcount = 0
#                 moreref = set()
#                 for refer in orig[it]["refs_"]:
#                     moreref.add(refer)
#                     new_dict[it]["refs_"][refer] = 1
#                     if refcount == 5:
#                         break
#
#                 for cite in orig[it]["cites_"]:
#                     moreref.add(cite)
#                     new_dict[it]["cites_"][cite] = 1
#                     if refcount == 10:
#                         break
#
#                 newrec[1].update(new_dict)
#                 already_added.add(new_dict[it]["id"])
#                 allowed_pap.add(new_dict[it]["id"])
#
#                 refcount = 0
#                 for every in moreref:
#                     refcount = keep_on_adding(every, orig, dupl, refcount)
#                     # if refcount == 10:
#                     #     break
#
#                 print(count)
#                 print(each)
#     return count + 1


# Iterate over all authors
for each in val[0]:
    if len(val[0][each]["items"]) > 1:
        new_dict = dict()
        new_dict[each] = val[0][each].copy()
        new_dict[each]["tags"] = {}
        new_dict[each]["authors"] = {}
        new_dict[each]["items"] = {}
        search_auth.add(each)

        authcount = 0
        for auth in val[0][each]["authors"]:
            allowed_auth.add(each)
            new_dict[each]["authors"][auth] = 1
            authcount += 1
            if authcount > 10:
                break

        papcount = 0
        for paper in val[0][each]["items"]:
            allowed_pap.add(paper)
            new_dict[each]["items"][paper] = 1
            papcount += 1
            if papcount > 10:
                break

        concount = 0
        for tag in val[0][each]["tags"]:
            allowed_con.add(tag)
            new_dict[each]["tags"][tag] = 1
            concount += 1
            if concount > 3:
                break

        new_dict[each]["count"] = len(new_dict[each]["items"])

        newrec[0].update(new_dict)

        total_count += 1
        if total_count > 6000:
            break

# print(len(allowed_pap))

#Iterate over papers
for each in val[1]:
    if each in allowed_pap:
        new_dict = dict()
        new_dict[each] = val[1][each].copy()
        new_dict[each]["tags"] = {}
        new_dict[each]["authors"] = {}
        new_dict[each]["refs_"] = {}
        new_dict[each]["cites_"] = {}
        new_dict[each]["cites"] = 0
        new_dict[each]["refs"] = 0

        counted = 0
        for auth in val[1][each]["authors"]:
            if auth in allowed_auth:
                new_dict[each]["authors"][auth] = 1
                counted += 1
                newrec[0][auth]["items"][each] = 1

        if counted == 1:
            for j in range(0, 2):
                randauth = random.sample(allowed_auth, 1)
                new_dict[each]["authors"][randauth[0]] = 1
                newrec[0][randauth[0]]["items"][each] = 1
                newrec[0][randauth[0]]["count"] += 1

        for tag in val[1][each]["tags"]:
            if tag in allowed_con:
                new_dict[each]["tags"][tag] = 1

        addedrefs = set()
        for i in range(0, 3):
            ran = random.sample(allowed_pap, 1)
            if ran[0] != each:
                new_dict[each]["refs_"][ran[0]] = 1
                new_dict[each]["refs"] += 1
                addedrefs.add(ran[0])
                if ran[0] not in overall_citations:
                    overall_citations[ran[0]] = []
                overall_citations[ran[0]].append(each)

        # addedcites = set()
        # for i in range(0, 3):
        #     ran = random.sample(allowed_pap, 1)
        #     if ran[0] != each and ran[0] not in addedrefs:
        #         new_dict[each]["cites_"][ran[0]] = 1
        #         new_dict[each]["cites"] += 1
        #         if ran[0] not in overall_citations:
        #             overall_citations[ran[0]] = []
        #         overall_citations[ran[0]].append(each)

                # refcount = 0
        # for refer in val[1][each]["refs_"]:
        #     referred.add(refer)
        #     new_dict[each]["refs_"][refer] = 1
        #     if refcount == 5:
        #         break
        #     refcount += 1
        #
        # for cite in val[1][each]["cites_"]:
        #     referred.add(cite)
        #     new_dict[each]["cites_"][cite] = 1
        #     if refcount == 10:
        #         break
        #     refcount += 1

        newrec[1].update(new_dict)
        already_added.add(val[1][each]["id"])

# refcount = 0
# for each in referred:
#     refcount = keep_on_adding(each, val[1], newrec[1], refcount)
#     # if refcount == 10:
#     #     break
# Iterating over citations
for each in overall_citations:
    for reff in overall_citations[each]:
        if reff not in newrec[1][each]["cites_"]:
            newrec[1][each]["cites_"][reff] = 1
            newrec[1][each]["cites"] += 1

# Iterating over tags
for each in val[2]:
    if each in allowed_con:
        new_dict = dict()
        new_dict[each] = val[2][each].copy()
        new_dict[each]["tags"] = {}
        new_dict[each]["authors"] = {}
        new_dict[each]["items"] = {}

        authcount = 0
        for auth in val[2][each]["authors"]:
            if auth in allowed_auth:
                new_dict[each]["authors"][auth] = 1
                authcount += 1
                if authcount > 10:
                    break

        papcount = 0
        for paper in val[2][each]["items"]:
            if paper in allowed_pap:
                new_dict[each]["items"][paper] = 1
                papcount += 1
                if papcount > 10:
                    break

        concount = 0
        for tag in val[2][each]["tags"]:
            if tag in allowed_con:
                new_dict[each]["tags"][tag] = 1
                concount += 1
                if concount > 10:
                    break

        newrec[2].update(new_dict)

# Linking papers to tags
for each in newrec[1]:
    for tags in newrec[1][each]["tags"]:
        if each not in newrec[2][tags]["items"]:
            newrec[2][tags]["items"][each] = 1

# Linking authors to tags
for each in newrec[0]:
    for tags in newrec[0][each]["tags"]:
        if each not in newrec[2][tags]["authors"]:
            newrec[2][tags]["authors"][each] = 1

newrec[3] = val[3]

# Dump to reduced file
f2 = open("reducedauthor.json", 'w', encoding='utf-8')
json.dump(newrec, f2)
f2.close()

with open("reducedauthor.json") as red:
    dat = json.load(red)

# Creating the reduced search file
with open('searchdump-1.json') as search:
    searches = json.load(search)

new_search = [[], [], [], 0]

for auth in searches[0]:
    if str(auth["id"]) in search_auth:
        new_dict = dict()
        new_dict = auth.copy()
        new_dict["count"] = dat[0][str(auth["id"])]["count"]
        new_search[0].append(new_dict)

for pap in searches[1]:
    if pap["id"] in allowed_pap:
        new_dict = dict()
        new_dict = pap.copy()
        new_dict["cites"] = dat[1][pap["id"]]["cites"]
        new_dict["refs"] = dat[1][pap["id"]]["refs"]
        new_search[1].append(new_dict)

for tag in searches[2]:
    if str(tag["id"]) in allowed_con:
        new_dict = dict()
        new_dict = tag.copy()
        new_search[2].append(new_dict)

new_search[3] = searches[3]

# Dump to reduced search file
f3 = open("reducedsearch.json", 'w', encoding='utf-8')
json.dump(new_search, f3)
f3.close()

# Replacing all hyphens with empty character
with open("reducedsearch.json") as reader:
    for line in reader.readline():
        line.replace('-', '')

with open("reducedauthor.json") as reader:
    for line in reader.readline():
        line.replace('-', '')