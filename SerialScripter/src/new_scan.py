import os
import nmap
import logging
from time import time
from pprint import pprint

def osdetect(ip):
    # sys.stdout.write(Bcolors.RED + "\nOS：\n" + Bcolors.ENDC)
    nm = nmap.PortScanner()
    try:
        result = nm.scan(hosts=ip, arguments="-sS -n -T4 -F --min-hostgroup 256 --min-parallelism 10")
        # print(result)
        for ip in result["scan"]:
            if result["scan"][ip]["status"]["state"] == 'up':
                print(ip)

        
        # for k, v in result.get("scan").items():
        #     if v.get("osmatch"):
        #         for i in v.get("osmatch"):
        #             print("OSdetect", ip, i.get("name") + "\n")
        #             return i.get("name")
        #     else:
        #         break
    except Exception as e:
        print("OSdetect", ip, "None\n")
        logging.exception(e) 
start = time()
osdetect("192.168.1.0/24")




# print(os.popen(f'nmap -sS -O -vv -n -T4 -F --min-hostgroup 256 --min-parallelism 10 --reason 192.168.1.0/24').readlines())
end = time()
print(end-start)


# print(f"No para: {sum([111.43866181373596,63.44760584831238,29.7033269405365,45.112815380096436,27.13277244567871,29.004868030548096])/6}")

# print(f"POPEN: {sum([25.272660493850708,24.382062196731567,47,67.32178807258606,32.549999952316284,52.034154653549194])/6}")

# print(f"Para: {sum([70.37018251419067,24.383501052856445,37.29046154022217,28.757407188415527,32.46862530708313,32.19897770881653])/6}")