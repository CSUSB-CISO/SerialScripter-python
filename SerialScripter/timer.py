# # importing the required module
import timeit 

import cProfile

 
# # timeit statement

# 10000 Searches 0.028911684000377136
# 50000 Searches 0.136522376999892
# 100000 Searches 0.26013425700011794
mycode = """
a = {
  "Alerts": [
    {
      "Incident": {
        "Host": "host-69420",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69421",
        "Name": "Net cat back door",
        "User": "John",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69422",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    }
  ]
}

def partial(item, query):
        return item if query in item or (len(query)//2 > 0 and query[0:len(query)//2] in item) or (len(query)//2 > 0 and query[len(query)//2::] in item) else None

def search(items: list, query, filters=None) -> tuple:
        if filters:
                try:
                        return tuple(item for item in items for filter in filters if partial(item["Incident"][filter], query))
                except KeyError:
                        return tuple(item for item in items for key in item["Incident"] if partial(item["Incident"][key], query))
        else:
                return tuple(item["Incident"] for item in items for key in item["Incident"] if partial(item["Incident"][key], query))

search(a["Alerts"], "hunter", filters=["User"])
"""

# 10000 Searches 0.10469168200006607
# 50000 Searches 0.5029173799998716
# 100000 Searches 1.0016284640000777
mycode2 = """
a = {
  "Alerts": [
    {
      "Incident": {
        "Host": "host-69420",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69421",
        "Name": "Net cat back door",
        "User": "John",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69422",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    }
  ]
}
def partial(item, query):
        return item if query in item or (len(query)//2 > 0 and query[0:len(query)//2] in item) or (len(query)//2 > 0 and query[len(query)//2::] in item) else None

def search(items: list, query, filters=None) -> tuple:
        if filters:
                try:
                        return tuple(item for item in items for filter in filters if partial(item["Incident"][filter], query))
                except KeyError:
                        return tuple(item for item in items for key in item["Incident"] if partial(item["Incident"][key], query))
        else:
                return tuple(item["Incident"] for item in items for key in item["Incident"] if partial(item["Incident"][key], query))

search(a["Alerts"], "hunter")
"""

mycode3 = """
from difflib import SequenceMatcher

a = {
  "Alerts": [
    {
      "Incident": {
        "Host": "host-69420",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69421",
        "Name": "Net cat back door",
        "User": "John",
        "Process": "nc.exe",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    },
    {
      "Incident": {
        "Host": "host-69422",
        "Name": "Net cat back door",
        "User": "hunte",
        "Process": "hunte",
        "RemoteIP": "10.123.65.30",
        "Cmd": "nc.exe --someoption"
      }
    }
  ]
}

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

search(incidents=a["Alerts"], search_words=["hunter"], filters=["User"])

"""
# cProfile.run(mycode)
# cProfile.run(mycode2)
cProfile.run(mycode3)


# print (timeit.timeit(stmt = mycode,
#                      number = 50000))
# print (timeit.timeit(stmt = mycode2,
#                      number = 50000))
# print (timeit.timeit(stmt = mycode3,
#                      number = 50000))
