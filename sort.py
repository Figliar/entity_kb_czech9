import time

from sub_orgs import sub_of_organisation
from sub_occs import sub_of_occurence
from help_functions import *
import re
import sys

from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

#   Q[0-9]+\torganizace\t[^\t]+\t[^A-Z]
#   Q[0-9]+\torganizace\t[^\t]+\t[^A-ZÚČŠŽŘÁÉ0-9\„Ó\"\'ÜΟР﻿ŻÅÎÖŚÄØ]

array = {}


# Získa IDčka a ich početnosti a uloží ich do array
def get_ids(input_f):
    try:
        with open(input_f, "r") as f:
            for i, ii in enumerate(f):
                print(i)
                line = ii.split("\t")
                sparql_query = 'SELECT ?instanceLabel WHERE { wd:%s p:P31/ps:P31 ?instanceLabel . }' % line[0]
                # sparql_query = 'SELECT ?instanceLabel WHERE { wd:%s p:P31/ps:P31 ?instanceLabel . SERVICE wikibase:label { ' \
                #                'bd:serviceParam wikibase:language "[AUTO_LANGUAGE],cs" }}' % line[0]

                try:
                    try:
                        res = return_sparql_query_results(sparql_query)
                        time.sleep(2)
                    except ConnectionError as c:
                        print(c, "c")
                except ValueError as e2:
                    print(e2, "e2")
                    continue

                for value in res["results"]["bindings"]:
                    id = value["instanceLabel"]["value"].split("/")
                    if id[-1] not in sub_of_occurence.keys() and id[-1] not in sub_of_organisation.keys():
                        if id[-1] not in array.keys():
                            array[id[-1]] = {}
                            array[id[-1]]["instances"] = 1
                        else:
                            array[id[-1]]["instances"] += 1
        f.close()
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(1)


# Získa počty entít s českými názvami konkrétných tried
def get_entities():
    length = len(array)
    for i in array.keys():
        print(i, " / ", length)
        array[i]["entities"] = 1
        sparql_query = 'SELECT ?item ?itemLabel \
                        WHERE \
                        {\
                        ?item wdt:P31 wd:%s.\
                        ?item rdfs:label ?label .\
                        FILTER (lang(?label) = "cs")\
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],cs". }\
                        }\
                        ' % i
        try:
            try:
                res = return_sparql_query_results(sparql_query)
                # time.sleep(10)
                n = 1
                for number, y in enumerate(res["results"]["bindings"]):
                    n += 1
                if number:
                    array[i]["entities"] = number
                else:
                    array[i]["entities"] = 1
            except ConnectionError as c2:
                print(c2, "c2")
        except ValueError as e:
            print(e, "e")
            continue


# Zapíše získané hodnoty do výstupového súboru vo formáte TSV
def write_(output_f):
    var = {k: v for k, v in sorted(array.items(), key=lambda item: item[1]["entities"], reverse=True)}

    print("sorting hotovo")
    try:
        with open(output_f, "w") as f_2:
            for value in var.keys():
                name = get_name_from_id(value)
                if name == "":
                    sparql_query = 'SELECT  *\
                                    WHERE {\
                                    wd:%s rdfs:label ?label .\
                                    FILTER (lang(?label) = "en")\
                                    }\
                                    LIMIT 1\
                                    ' % value
                    try:
                        res = return_sparql_query_results(sparql_query)
                        name = str(res["results"]["bindings"][0]["label"]["value"])
                        time.sleep(2)
                    except IndexError or UnboundLocalError:
                        continue
                    f_2.write(value + "\t" + name + " (EN)\t" + str(array[value]["instances"]) + "\t" + str(
                        array[value]["entities"]) +
                              "\n")
                else:
                    f_2.write(value + "\t" + name + "\t" + str(array[value]["instances"]) + "\t" +
                              str(array[value]["entities"]) + "\n")
        f_2.close()
    except FileNotFoundError:
        print(FileNotFoundError)
        sys.exit(2)


if __name__ == '__main__':

    if sys.argv[1]:
        READ_FILE = sys.argv[1]
        WRITE_FILE = "instances_" + READ_FILE

        print("Z:   " + READ_FILE)
        print("DO:   " + WRITE_FILE)

        get_ids(READ_FILE)

        print("Getting ids finnished")

        get_entities()

        print("entities hotovo")

        write_(WRITE_FILE)

        print("Hotovo")
    else:
        print("Missing INPUT_FILE argument!\n")
