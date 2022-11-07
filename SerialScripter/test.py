
# type incident struct {
	# Name     string
	# User     string
	# Process  string
	# RemoteIP string
	# Cmd      string
# }
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

print(search(a["Alerts"], "hunters"))

