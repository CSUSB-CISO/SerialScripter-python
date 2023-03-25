import ctypes
lib = ctypes.cdll.LoadLibrary('./libsearch.so')  # replace with the path to the compiled C code

class Incident(ctypes.Structure):
    _fields_ = [
        ('host', ctypes.c_char_p),
        ('type', ctypes.c_char_p),
        ('name', ctypes.c_char_p),
        ('time', ctypes.c_char_p),
        ('user', ctypes.c_char_p),
        ('severity', ctypes.c_char_p),
        ('payload', ctypes.c_char_p),
    ]

class IncidentList(ctypes.Structure):
    _fields_ = [
        ('incidents', ctypes.POINTER(Incident)),
        ('size', ctypes.c_int),
    ]


search_incidents = lib.search_incidents
search_incidents.argtypes = [ctypes.POINTER(IncidentList), ctypes.c_char_p, ctypes.c_int]
search_incidents.restype = IncidentList


# incidents_arr = []

# # Declare and initialize an array of Incident structures
# incidents_arr = [
#     Incident(b"192.168.1.1", b"Alert", b"bruh test", b"12:00:00", b"root", b"3", b"/x00/0x4f"),
#     Incident(b"192.168.1.2", b"BLAH", b"Bad sudo", b"12:00:00", b"hunte", b"3", b"root"),
#     Incident(b"192.168.1.5", b"BOO", b"Changing File", b"12:00:00", b"james", b"3", b"root"),
# ]

# incidents = IncidentList((Incident * len(incidents_arr))(*incidents_arr), len(incidents_arr))


# # print all users in the result array
# for i in range(results.size):
#     print(results.incidents[i].type.decode())


class Search:
    def __init__(self, incident_data: dict[dict[str]], search_terms) -> None:
        self.incidents = self.to_IncidentList(incident_data)
        self.search_terms = search_terms.encode()
        
        self.result = self.search()

    def to_IncidentList(self, incidents):
        # IncidentList((Incident * len(incidents_arr))(*incidents_arr), len(incidents_arr))
        incidents_arr = [Incident(host=incidents['Host'].encode(),type=type_.encode(),name=incidents['Incident']['Name'].encode(),time=incidents['Incident']['CurrentTime'].encode(),user=incidents['Incident']['User'].encode(),severity=incidents['Incident']['Severity'].encode(),payload=incidents['Incident']['Payload'].encode(),) for incident_dict in incidents for type_, incidents in incident_dict.items()]
        return IncidentList((Incident * len(incidents_arr))(*incidents_arr), len(incidents_arr))

    def to_dict(self, incidents: IncidentList):
        # {'Alert': {'Host': '192.168.1.1', 'Incident': {'Name': 'Changed file', 'CurrentTime': 'bruh time', 'User': 'root', 'Severity': 'High', 'Payload': 'random metadata bullshit'}}}
        
        return [{ incidents.incidents[i].type.decode(): { 'Host': incidents.incidents[i].host.decode(),'Incident': {'Name': incidents.incidents[i].name.decode(),'CurrentTime': incidents.incidents[i].time.decode(),'User': incidents.incidents[i].user.decode(),'Severity': incidents.incidents[i].severity.decode(),'Payload': incidents.incidents[i].payload.decode(),} }} for i in range(incidents.size)]

    def search(self):
        results_ptr = search_incidents(ctypes.byref(self.incidents), self.search_terms, self.incidents.size)
        
        results = self.to_dict(results_ptr)
        lib.free(results_ptr)

        return results
    

if __name__ == "__main__":
    incidents = [
        {'Alert': {'Host': '192.168.1.1', 'Incident': {'Name': 'Changed file', 'CurrentTime': 'bruh time', 'User': 'root', 'Severity': 'High', 'Payload': 'random metadata bullshit'}}},
        {'Warning': {'Host': '192.168.1.2', 'Incident': {'Name': 'Bad sudo', 'CurrentTime': '12:00:00', 'User': 'hunte', 'Severity': 'Medium', 'Payload': 'root'}}},
        {'Critical': {'Host': '192.168.1.5', 'Incident': {'Name': 'Changing File', 'CurrentTime': '12:00:00', 'User': 'james', 'Severity': 'Low', 'Payload': 'root'}}},
    ]

    print(Search(incidents, "hunte").result)

# incident_objects = [Incident(host=incident_data['Host'].encode(),type_=type_.encode(),name=incident_data['Incident']['Name'].encode(),time=incident_data['Incident']['CurrentTime'].encode(),user=incident_data['Incident']['User'].encode(),severity=incident_data['Incident']['Severity'].encode(),payload=incident_data['Incident']['Payload'].encode(),) for incident_dict in self.incidents for type_, incident_data in incident_dict.items()]
# incident_objects = Search.to_IncidentList(incidents)
# results = search_incidents(ctypes.byref(incident_objects), b"hunte", incident_objects.size)
# print(Search.to_dict(results))
# lib.free(results.incidents)
