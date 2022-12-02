from difflib import SequenceMatcher
from re import match

def is_ip(ip: str):
    return bool(match("^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$", ip))

def check_sequence(incident, sequencer, key, query):
    sequencer.set_seq1(incident['Incident'][key])

    if is_ip(query) and sequencer.ratio() == 1:
        print(f'{query} == {incident["Incident"][key]}')
        return True
    elif not is_ip(query) and sequencer.ratio() > 0.6:
        print(f'{query} == {incident["Incident"][key]}')
        return True
    return False

def matches_query(incident, queries, match_all=False) -> bool:
    match_counter = 0
    
    for query in queries:
        sequencer = SequenceMatcher(None, "", query[0])
        if query[1]:
            x = check_sequence(incident, sequencer, query[1], query[0])
            if x and match_all:
                match_counter += 1
                break
            elif x:
                return True
        else:
            for value in incident['Incident']:
                x = check_sequence(incident, sequencer, value, query[0])
                if x and match_all:
                    match_counter += 1
                    break
                elif x:
                    return True

    if match_all and match_counter == len(queries):
        return True

    return False

def search(incidents, search_words=["host"], filters=[], match_all=False):
    queries = list()
    for i, word in enumerate(search_words):
        try:
            queries.append((word, filters[i]))
        except:
            queries.append((word,))
    
    return tuple(incident for incident in incidents if matches_query(incident, queries, match_all=match_all))

def sort(incidents: list[dict], by="Host"):

    return sorted(incidents, key=lambda ip: ip["Incident"][by])