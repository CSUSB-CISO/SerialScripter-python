from os import popen 
import re 
response = popen("ping 192.168.1.189 -c 1").readlines()[1]
pattern = re.compile('ttl=\d*')
print(pattern.search(str(response)).group().split("=")[1])