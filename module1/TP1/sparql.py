# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 18:01:18 2021

@author: XPS
"""
from datetime import datetime as dt
from SPARQLWrapper import SPARQLWrapper, JSON
# Retrieve results from SPARQL
endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
sparql = SPARQLWrapper(endpoint)

# P39 = position held 
# Q33126365 = mayor of Brussels
# P69 = educated at
# P569 = date of birth
# P570 = date of death


# statement = """
# SELECT DISTINCT ?person ?personLabel ?dateBirth ?dateDeath ?University 
# WHERE {
#     ?person  wdt:P39  wd:Q33126365 .
#     ?person  wdt:P69  ?University .
#     FILTER (?University = wd:Q20754971 || ?University = wd:Q574606) .
#     ?person  wdt:P569 ?dateBirth .
#     OPTIONAL {?person wdt:P570 ?dateDeath .}
#     SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
# }

# ORDER BY ?personLabel
# """

statement = """
SELECT DISTINCT ?person ?personLabel ?startDate ?party ?partyLabel
WHERE {
    ?person     wdt:P39     wd:Q33126365 ;
                wdt:P102    ?party .
    
    ?person     p:P39       ?statement .
    ?statement  pq:P580     ?startDate .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
}

ORDER BY ?personLabel
"""


sparql.setQuery(statement)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
rows = results['results']['bindings']

MayorList = [result['personLabel']['value'] for result in rows]

date_format = "%Y-%m-%dT%H:%M:%SZ"

for row in rows:
    try:
        start_date = dt.strptime(row['startDate']['value'], date_format)
    except ValueError:
        start_date = "????"
    try:
        political_party = row['partyLabel']['value']
    except ValueError: # unknown death date
        political_party = "????"

    print(f"{row['personLabel']['value']}- {start_date} - {political_party})")
    