from nmap import PortScanner
from os import popen 
from json import dump
import time
class Recon:
    def __init__(self, range: str) -> None:
        self.range = range
        nm = PortScanner()
        # self.results = nm.scan(hosts=range, arguments="-sS -n -T4 -F --min-hostgroup 256 --min-parallelism 10")
        
        
        self.results = nm.scan(hosts=range, arguments="-sn --min-hostgroup 256 --min-parallelism 10")
        ips = ', '.join(tuple(ip for ip in self.results['scan']))
        self.results = nm.scan(hosts=ips, arguments="-sS -n -T4 -F --min-hostgroup 256 --min-parallelism 10")

        self.results = nm.scan(hosts=ips)
        print(self.results)
        self.hosts = self.set_box_ips()

        self.box_data = self.init_box_data(self.hosts, self.get_TTLs(self.hosts))

    def set_box_ips(self) -> tuple:
        return tuple(ip for ip in self.results["scan"] if "tcp" in self.results["scan"][ip])
    
    def get_TTLs(self, hosts: tuple) -> tuple:
        TTLs = list()

        for ip in hosts:
            try:
                response = popen(f"ping {ip}").readlines()[2]
                TTLs.append(int(response[response.index("TTL=")+4:]))
            except:
                print(f"PING blocked by ip {ip}")
                TTLs.append(None)

        return tuple(TTLs)

    def init_box_data(self, hosts: tuple, TTLs: tuple) -> tuple:
        box_data = list()
        for i, ip in enumerate(hosts):
            if TTLs[i] != None:
                if TTLs[i] > 128:
                    box_data.append(
                        {
                            "name": f'host-{ip.split(".")[-1]}',
                            "ip": ip,
                            "OS": "Unknown",
                            "services": [
                                {
                                    "port": port,
                                    "service": self.results["scan"][ip]["tcp"][port]["name"]
                                } for port in self.results["scan"][ip]["tcp"]
                            ],
                            "isOn": True,
                            "docker": [],
                            "tasks": [{}],
                            "firewall": [],
                            "shares": [
                                {
                                    "name": {},
                                    "fullpath": {},
                                    "permissions": [
                                        {
                                        "users": [
                                            {
                                            "username": {}
                                            }
                                        ]
                                        }
                                    ],
                                    "SMBversion": {}
                                }
                            ]  
                        }
                    )
                elif TTLs[i] >= 120:
                    box_data.append(
                        {
                            "name": f'host-{ip.split(".")[-1]}',
                            "ip": ip,
                            "OS": "Windows",
                            "services": [
                                {
                                    "port": port,
                                    "service": self.results["scan"][ip]["tcp"][port]["name"]
                                } for port in self.results["scan"][ip]["tcp"]
                            ],
                            "isOn": True,
                            "docker": [],
                            "tasks": [{}],
                            "firewall": [],
                            "shares": [
                                {
                                    "name": {},
                                    "fullpath": {},
                                    "permissions": [
                                        {
                                        "users": [
                                            {
                                            "username": {}
                                            }
                                        ]
                                        }
                                    ],
                                    "SMBversion": {}
                                }
                            ]   
                        }
                    )
                else:
                    box_data.append(
                        {
                            "name": f'host-{ip.split(".")[-1]}',
                            "ip": ip,
                            "OS": "Linux",
                            "services": [
                                {
                                    "port": port,
                                    "service": self.results["scan"][ip]["tcp"][port]["name"]
                                } for port in self.results["scan"][ip]["tcp"]],
                            "isOn": True,
                            "docker": [],
                            "tasks": [{}],
                            "firewall": [],
                            "shares": [
                                {
                                    "name": {},
                                    "fullpath": {},
                                    "permissions": [
                                        {
                                        "users": [
                                            {
                                            "username": {}
                                            }
                                        ]
                                        }
                                    ],
                                    "SMBversion": {}
                                }
                            ]   
                        }
                    )
        return tuple(box_data)

    def get_box_data(self):
        return self.box_data

    def save_box_data(self):
        with open("website/data/hosts.json",
        "w") as f:
            f.write('{\n\t"hosts": [\n')

            for box_name in range(len(self.box_data)):
                if box_name < len(self.box_data)-1:
                    f.write("\t\t")
                    dump(self.box_data[box_name], f)
                    f.write(",\n")
                else:
                    f.write("\t\t")
                    dump(self.box_data[box_name], f)
                    f.write("\n\t]\n}")
 
# start = time.time()
# a = Recon("192.168.1.0/24")

# print(end-start)
# print(a.get_box_data())
# a.save_box_data()

# a = {'nmap': {'command_line': 'nmap -oX - -sn --min-hostgroup 256 --min-parallelism 10 192.168.1.0/24', 'scaninfo': {'warning': ['Warning: You specified a highly aggressive --min-hostgroup.\n']}, 'scanstats': {'timestr': 'Sat Dec  3 08:38:39 2022', 'elapsed': '31.91', 'uphosts': '9', 'downhosts': '247', 'totalhosts': '256'}}, 'scan': {'192.168.1.1': {'hostnames': [{'name': 'www.routerlogin.com', 'type': 'PTR'}], 'addresses': {'ipv4': '192.168.1.1', 'mac': '94:A6:7E:F6:38:CF'}, 'vendor': {'94:A6:7E:F6:38:CF': 'Netgear'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.3': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.3', 'mac': 'E0:D5:5E:35:5A:46'}, 'vendor': {'E0:D5:5E:35:5A:46': 'Giga-byte Technology'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.5': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.5', 'mac': '94:B5:55:77:9B:48'}, 'vendor': {'94:B5:55:77:9B:48': 'Espressif'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.6': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.6', 'mac': 'F4:A4:75:EA:9D:9F'}, 'vendor': {'F4:A4:75:EA:9D:9F': 'Intel Corporate'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.7': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.7', 'mac': '82:A2:5E:BB:0E:3F'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.9': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.9', 'mac': '38:FC:98:E5:01:5F'}, 'vendor': {'38:FC:98:E5:01:5F': 'Intel Corporate'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.10': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.10', 'mac': '10:3D:1C:A7:9E:91'}, 'vendor': {'10:3D:1C:A7:9E:91': 'Intel Corporate'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.12': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.12', 'mac': 'F4:B3:01:69:C9:31'}, 'vendor': {'F4:B3:01:69:C9:31': 'Intel Corporate'}, 'status': {'state': 'up', 'reason': 'arp-response'}}, '192.168.1.11': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.11'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'localhost-response'}}}}



# ips = ', '.join(tuple(ip for ip in a['scan']))
# nm = PortScanner()

# results = nm.scan(hosts=ips, arguments="-sS -n -T4 -F --min-hostgroup 256 --min-parallelism 10")
# print(ips)

# print(results)
# end = time.time()
# print(end-start)
