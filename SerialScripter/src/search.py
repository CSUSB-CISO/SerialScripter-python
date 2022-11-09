from difflib import SequenceMatcher

def matches_query(incident, queries, filters=[]) -> bool:
  if filters:
    for query in queries:
      for filter in filters:
        query.set_seq1(incident['Incident'][filter])
        if query.ratio() > 0.6:
          return True
  else:
    for query in queries:
      for value in incident['Incident']:
        query.set_seq1(incident['Incident'][value])
        if query.ratio() > 0.6:
          return True
  return False



def search(incidents, search_words=["host"], filters=[]):
  queries = {SequenceMatcher(None, "", word) for word in search_words}
  return tuple(incident for incident in incidents if matches_query(incident, queries))
