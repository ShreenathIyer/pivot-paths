'''

Create a dump of objects in a fixed manner from the original dataset.

'''


import jsonlines
import json

search_list = [[], [], [], 0]
users = []
resources = []
concepts = []
concepts_list = []
authordump = [{}, {}, {}, []]
citations = {}
citedby = {}
person_key = 0
authors = {}
count = 0

f2 = open("searchdump.json", 'w', encoding='utf-8')
f3 = open("authdetails.txt", 'w', encoding='utf-8')
f4 = open("singleauthordump.json", 'w', encoding='utf-8')


# Read the original data set
with jsonlines.open('mag_papers_80.txt') as reader:
    for obj in reader:
        print(count)
        lfull = []

        # We only pick the objects which are written in english and have all the required keys
        if "fos" in obj and "lang" in obj and "authors" in obj:
            if obj["lang"] == "en":
                dname = obj["authors"]
                fullname = ''
                org = ''
                fname = ''
                lname = ''
                mname = ''

                for each in dname:
                    if "org" in each:
                        org = each["org"]
                        break

                interests = ""

                # We make a list of the current concepts and insert very new concept in the search file
                currcon = []
                for i in range(0, len(obj["fos"])):
                    currcon.append(str(obj["fos"][i]))
                    interests += (str(obj["fos"][i]))
                    if i < len(obj["fos"]) - 1:
                        interests += ", "
                    if str(obj["fos"][i]) not in concepts_list:
                        concepts_list.append(str(obj["fos"][i]))

                        new_concept = {"id": concepts_list.index(str(obj["fos"][i])), "name": str(obj["fos"][i]),
                                       "type": str(obj["fos"][i]), "count": 1, "type": 2,
                                       "fullid": "2_" + str(concepts_list.index(str(obj["fos"][i])))}
                        concepts.append(new_concept)

                        # We insert the new concept in the authors file
                        conid = concepts_list.index(str(obj["fos"][i]))
                        authordump[2][conid] = {"id": conid, "name": new_concept["name"], "count": 1, "items": {},
                                                "authors": {}, "tags": {}, "type": 2, "fullid": new_concept["fullid"]}

                    else:
                        concepts[concepts_list.index(str(obj["fos"][i]))]["count"] += 1
                        authordump[2][concepts_list.index(str(obj["fos"][i]))]["count"] += 1

                # Since the current concepts are all related, they need to be present in each other's tags fields
                for ic in currcon:
                    conid = concepts_list.index(ic)
                    for jc in currcon:
                        if jc != ic:
                            if concepts_list.index(jc) not in authordump[2][conid]["tags"]:
                                authordump[2][conid]["tags"][concepts_list.index(jc)] = 1
                            else:
                                authordump[2][conid]["tags"][concepts_list.index(jc)] += 1

                url = ""
                if "url" in obj:
                    url = obj["url"][0]

                # Inserting a new author to the authors data set
                for each in dname:
                    if "name" in each:
                        fullname = each["name"]
                        lfull = fullname.split(' ')
                        if len(lfull) == 3:
                            fname = lfull[0]
                            mname = lfull[1]
                            lname = lfull[2]
                        elif len(lfull) == 2:
                            fname = lfull[0]
                            lname = lfull[1]
                            mmane = ''
                        else:
                            lname = lfull[0]
                            fname = ''
                            mname = ''
                        if fullname not in authors:
                            authors[fullname] = person_key
                            person_key += 1

                # Inserting a new author to the search file
                for each in dname:
                    if "name" in each:
                        fullname = each["name"]
                        lfull = fullname.split(' ')
                        if len(lfull) == 3:
                            fname = lfull[0]
                            mname = lfull[1]
                            lname = lfull[2]
                        elif len(lfull) == 2:
                            fname = lfull[0]
                            lname = lfull[1]
                            mmane = ''
                        else:
                            lname = lfull[0]
                            fname = ''
                            mname = ''
                        new_user = {}
                        new_user = {"id": authors[fullname], "name": fullname, "fname": fname, "lname": lname, "mname": mname,
                                "count": 0, "org": org, "link": url, "fullname": fullname, "interests": interests,
                                "fullid": "0_" + str(authors[fullname]), "type": 0}
                        users.append(new_user)

                        # Adding concepts to the author's tags field
                        for ic in currcon:
                            conid = concepts_list.index(ic)
                            for jc in currcon:
                                if jc != ic:
                                    if new_user["id"] not in authordump[2][conid]["authors"]:
                                        authordump[2][conid]["authors"][new_user["id"]] = 1
                                    else:
                                        authordump[2][conid]["authors"][new_user["id"]] += 1

                        # Inserting the new author to the authors file
                        dumpid = authors[fullname]
                        if dumpid not in authordump[0]:
                            authordump[0][dumpid] = {"id": dumpid, "fullname": new_user["name"], "name": new_user["name"],
                                                     "count": 1, "org": new_user["org"], "link": new_user["link"],
                                                     "interests": interests, "type": new_user["type"], "fullid": new_user["fullid"],
                                                     "cnt": 1, "items": {obj["id"]: 1}, "authors": {}, "tags": {}, "cites": 0}

                            for con in range(0, len(obj["fos"])):
                                authordump[0][dumpid]["tags"][concepts_list.index(obj["fos"][con])] = 1

                            for per in obj["authors"]:
                                if "name" in per and per["name"] != fullname:
                                    tempauth = per["name"]
                                    tempid = authors[tempauth]
                                    authordump[0][dumpid]["authors"][tempid] = 1

                        else:
                            authordump[0][dumpid]["cnt"] += 1
                            authordump[0][dumpid]["count"] += 1
                            authordump[0][dumpid]["items"][obj["id"]] = 1

                            for con in range(0, len(obj["fos"])):
                                if obj["fos"][i] not in authordump[0][dumpid]["tags"]:
                                    authordump[0][dumpid]["tags"][concepts_list.index(obj["fos"][con])] = 1
                                else:
                                    authordump[0][dumpid]["tags"][concepts_list.index(obj["fos"][con])] += 1

                            # Inserting all related authors as keys in each other's author's dictionary
                            for per in obj["authors"]:
                                if "name" in per:
                                    tempauth = per["name"]
                                    tempid = authors[tempauth]
                                    if tempauth not in authordump[0][dumpid]["authors"]:
                                        authordump[0][dumpid]["authors"][tempid] = 1
                                    else:
                                        authordump[0][dumpid]["authors"][tempid] += 1

                # Inserting new paper to the search file
                new_resource = {}
                doi = ''
                references = 0
                abstract = "None provided"
                if "doi" in obj:
                    doi = obj['doi'].replace('/', '')
                if "references" in obj:
                    references = len(obj["references"])
                if "abstract" in obj:
                    abstract = obj["abstract"]
                new_resource = {'id': obj['id'], 'year': obj['year'], 'name': obj['title'],
                                'link': url, 'text': '', 'type': 1, 'fullid': '1_' + obj['id'],
                                'refs': references, 'cites': 0}
                resources.append(new_resource)

                # Inserting the current concepts to the item's tags field
                for ic in currcon:
                    conid = concepts_list.index(ic)
                    for jc in currcon:
                        if jc != ic:
                            if new_resource["id"] not in authordump[2][conid]["items"]:
                                authordump[2][conid]["items"][new_resource["id"]] = 1
                            else:
                                authordump[2][conid]["items"][new_resource["id"]] += 1

                # Inserting paper to the authors file
                paperid = new_resource["id"]
                if new_resource["id"] not in authordump[1]:
                    authordump[1][paperid] = {"id": paperid, "year": new_resource["year"], "name": new_resource["name"],
                                              "text": '', "type": 1, "fullid": new_resource["fullid"], "refs": new_resource["refs"],
                                              "deg": 1, "cites_": {}, "refs_": {}, "cites": 0, "authors": {}, "tags": {}}
                    for obja in dname:
                        if "name" in obja:
                            authorname = obja["name"]
                            authorid = authors[authorname]
                            authordump[1][paperid]["authors"][authorid] = 1

                    currconcepts = obj["fos"]
                    for objc in currconcepts:
                        conceptid = concepts_list.index(objc)
                        authordump[1][paperid]["tags"][conceptid] = 1

                # Adding references as citations in respective papers
                if references != 0:
                    for reference in obj["references"]:
                        if reference in citations:
                            citations[reference] += 1
                        else:
                            citations[reference] = 1

                        if reference not in citedby:
                            citedby[reference] = {}
                            citedby[reference][paperid] = 1
                        else:
                            citedby[reference][paperid] = 1

                        authordump[1][paperid]["refs_"][reference] = 1

        count += 1

        # if len(users) > 3000 and len(resources) > 3000 and len(concepts) > 3000:
        #     break
    print("done with reading")

    # Traverse yet again to fill in the citations
    for resource in resources:
        if resource["id"] in citations:
            rid = resource["id"]
            resource["cites"] = citations[rid]

    # Adding cites to papers
    for yetanotherid in authordump[1]:
        if authordump[1][yetanotherid]["id"] in citations:
            rid = authordump[1][yetanotherid]["id"]
            authordump[1][yetanotherid]["cites"] = citations[rid]
        if authordump[1][yetanotherid]["id"] in citedby:
            authordump[1][yetanotherid]["cites_"] = citedby[authordump[1][yetanotherid]["id"]].copy()

    # Increase the citations per author
    for runningouttaids in authordump[0]:
        for pap in authordump[0][runningouttaids]["items"]:
            if pap in citations:
                rid = pap
                authordump[0][runningouttaids]["cites"] += citations[rid]

search_list[0] = users
search_list[1] = resources
search_list[2] = concepts

authordump[3].append(15)

# Dump to files
json.dump(search_list, f2)
f2.close()
json.dump(authors, f3)
f3.close()
json.dump(authordump, f4)
f4.close()

print(search_list)


