from difflib import SequenceMatcher
from re import match

def is_ip(ip: str):
    return bool(match("^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$", ip))

def check_sequence(incident, sequencer, key, query, match_all):
    sequencer.set_seq1(incident['Incident'][key])
    if match_all:
        if is_ip(query[0]) and sequencer.ratio() == 1:
            match_counter += 1
        elif sequencer.ratio() > 0.6:
            match_counter += 1
    else:
        if is_ip(query[0]):
            if sequencer.ratio() == 1:
                return True
        elif sequencer.ratio() > 0.6:
            return True

def matches_query(incident, queries, match_all=False) -> bool:
    match_counter = 0
    
    for query in queries:
        sequencer = SequenceMatcher(None, "", query[0])
        print(query)
        if query[1]:
            sequencer.set_seq1(incident['Incident'][query[1]])
            print("ratio"+str(sequencer.ratio()), is_ip(query[0]))

            if match_all:
                if is_ip(query[0]) and sequencer.ratio() == 1:
                    match_counter += 1
                    break
                elif not is_ip(query[0]) and sequencer.ratio() > 0.6:
                    match_counter += 1
                    break
            else:

                if is_ip(query[0]):
                    return query[0] == incident['Incident'][query[1]]
                elif sequencer.ratio() > 0.6:
                    return True
        else:
            for value in incident['Incident']:
                sequencer.set_seq1(incident['Incident'][value])
                # print(incident['Incident'][value], "ratio"+str(sequencer.ratio()), is_ip(query[0]))

                if match_all:
                    
                    if is_ip(query[0]) and sequencer.ratio() == 1:
                        print(query[0], incident['Incident'][value])
                        match_counter +=1
                        break
                    elif not is_ip(query[0]) and sequencer.ratio() > 0.6:
                        match_counter +=1
                        print(query[0], incident['Incident'][value])
                        break
                else:
                    if is_ip(query[0]):
                        if sequencer.ratio() == 1:
                            return True
                    elif sequencer.ratio() > 0.6:
                        return True

    if match_all and match_counter == len(queries):
        print(match_counter)
        return True

    return False

def search(incidents, search_words=["host"], filters=[], match_all=False):
    queries = list()
    for i, word in enumerate(search_words):
        try:
            queries.append((word, filters[i]))
        except:
            queries.append((word,))
    print(queries)
    
    return tuple(incident for incident in incidents if matches_query(incident, queries, match_all=match_all))

def sort(incidents: list[dict], by="Host"):

    return sorted(incidents, key=lambda ip: ip["Incident"][by])