
import ctypes

# Define the struct
class Incidents(ctypes.Structure):
    _fields_ = [
        ("host", ctypes.c_char * 50),
        ("name", ctypes.c_char * 50),
        ("user", ctypes.c_char * 50),
        ("process", ctypes.c_char * 50),
        ("remoteIP", ctypes.c_char * 50),
        ("cmd", ctypes.c_char * 100)
    ]

# Define the function signature

find_matching_incidents = ctypes.cdll.LoadLibrary("lib/search_incidents/libsearch.so").find_matching_incidents
find_matching_incidents.argtypes = [ctypes.POINTER(Incidents), ctypes.c_int, ctypes.c_char_p, ctypes.c_double, ctypes.POINTER(ctypes.c_int)]
find_matching_incidents.restype = ctypes.POINTER(Incidents)

# Sample data
incidents = (Incidents * 3)(
    Incidents(b"localhost", b"chrome", b"user1", b"chrome.exe", b"192.168.0.1", b"chrome browser"),
    Incidents(b"example.com", b"firefox", b"hunte", b"firefox.exe", b"192.168.0.2", b"firefox browser"),
    Incidents(b"example.com", b"edge", b"user3", b"msedge.exe", b"192.168.0.3", b"edge browser")
)

# Call the find_matching_incidents function
num_matches = ctypes.c_int(0)
matches = find_matching_incidents(incidents, len(incidents), b"hunte", 0.5, ctypes.byref(num_matches))

# Print the matching incidents
for i in range(num_matches.value):
    print(matches[i].host.decode(), matches[i].name.decode(), matches[i].user.decode(), matches[i].process.decode(), matches[i].remoteIP.decode(), matches[i].cmd.decode())
