from difflib import SequenceMatcher
from json import load

from src.search import search, sort

def main():
    with open("website/data/incidents.json", "r") as f:
        incidents = load(f)["Alerts"]

    search_words = "ip:10.123.65.199 and user:john"


    switch = {
        "ip": "RemoteIP",
        "host": "Host",
        "name": "Name",
        "user": "User",
        "process": "Process",
        "cmd": "Cmd"
    }

    if search_words:
        match_all = "and" in search_words

        switch = {
            "ip": "RemoteIP",
            "host": "Host",
            "name": "Name",
            "user": "User",
            "process": "Process",
            "cmd": "Cmd"
        }

        queries = list()
        filters = list()

        for term in search_words.split():
            if term == "and" or term.startswith("search_by"):
                continue
            try:
                x = term.split(":")
                if len(x) > 1:
                    filters.append(x[0])
                    queries.append(x[1])
                else:
                    queries.append(x[1])
            except:
                queries.append(term)
        filters = tuple(map(lambda a: switch[a], filters))
        results = search(incidents, search_words=queries, filters=filters, match_all=match_all) if "and" in search_words else search(incidents, search_words=queries, filters=filters)
        if results:
            incidents = results
        
        if search_words.startswith("search_by"):
            try:
                incidents = sort(incidents, by=switch[search_words[search_words.index(":")+1:search_words.index(" ")]])
            except:
                incidents = sort(incidents, by=switch[search_words[search_words.index(":")+1:]])

    for incident in incidents:
        print(incident)
if __name__ == "__main__":
    main()