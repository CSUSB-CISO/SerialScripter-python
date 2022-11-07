# # importing the required module
import timeit 


 
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


# cProfile.run(mycode)
# cProfile.run(mycode2)

print (timeit.timeit(stmt = mycode,
                     number = 100000))
print (timeit.timeit(stmt = mycode2,
                     number = 100000))
