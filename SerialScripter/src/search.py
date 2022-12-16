from difflib import SequenceMatcher
from re import match


# Check if a given string is an ip
def is_ip(ip: str):
    return bool(match("^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$", ip))

# Check to the sequence to see if we have a match
def check_sequence(incident, sequencer: SequenceMatcher, key: str, query: str):
    sequencer.set_seq1(incident['Incident'][key])

    # ip matches must be exact
    if is_ip(query) and sequencer.ratio() == 1: 
        return True
    # Make sure youre not checking an ip
    # regular matches only need a 0.6 match
    elif not is_ip(query) and sequencer.ratio() > 0.6:
        return True
    return False

# 
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

def search(incidents, search_words = ["host"], filters = [], match_all: bool = False):
    queries = list()
    for i, word in enumerate(search_words):
        try:
            queries.append((word, filters[i]))
        except:
            queries.append((word,))
    
    return [incident for incident in incidents if matches_query(incident, queries, match_all=match_all)]

def sort(incidents, by: str = "Host"):
    return sorted(incidents, key=lambda ip: ip["Incident"][by])
