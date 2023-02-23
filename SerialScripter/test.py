import sys
sys.path.append('lib/search')
import search

incidents = [
    {
            "Host": "host-69420",
            "Name": "Net cat back door",
            "User": "hunte",
            "Process": "nc.exe",
            "RemoteIP": "10.123.65.30",
            "Cmd": "nc.exe --someoption"
    },
    {
    
            "Host": "host-69421",
            "Name": "Net cat back door",
            "User": "John",
            "Process": "nc.exe",
            "RemoteIP": "10.123.65.116",
            "Cmd": "nc.exe --someoption"

    }
]

search_string = "hunte"
match_ratio = 0.6

matches = search.find_matches(incidents, search_string, match_ratio)
print(matches)
