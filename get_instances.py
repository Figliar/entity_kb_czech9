import time
from re import split
import sys
from qwikidata.sparql import (get_subclasses_of_item, return_sparql_query_results)
import os

# Takes output of ent_parser.py and writes down subclasses of all found classes
if __name__ == '__main__':

    if sys.argv[1]:
        os.mkdir("_" + sys.argv[1])
        with open(sys.argv[1], "r") as f:
            for i, ii in enumerate(f):
                entity = ii.split("\t")
                sparql_query = 'SELECT ?item ?itemLabel \
                                    WHERE \
                                    {\
                                    ?item wdt:P31 wd:%s.\
                                    ?item rdfs:label ?label .\
                                    FILTER (lang(?label) = "cs")\
                                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],cs". }\
                                    }\
                                    ' % entity[0]
                try:
                    res = return_sparql_query_results(sparql_query)
                    # time.sleep(10)
                    file_name = "_" + sys.argv[1] + "/" + entity[1]
                    file = open(file_name, "w")
                    for number, y in enumerate(res["results"]["bindings"]):
                        file.write(y["item"]["value"].split("/")[-1] + "\t" + y["itemLabel"]["value"] + "\n")
                except ValueError as e:
                    print(e, "e")
                    continue
                print(i)
    else:
        print("Missing INPUT_FILE argument!\n")
