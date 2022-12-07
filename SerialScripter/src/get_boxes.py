from nmap import PortScanner
from os import popen 
from json import dump
import time
class Recon:
    def __init__(self, range: str) -> None:
        self.range = range
        nm = PortScanner()
        self.results = nm.scan(hosts=self.range, arguments="-sS -n -T4 -F")
        
        
        # self.results = nm.scan(hosts=range, arguments="-sn --min-hostgroup 256 --min-parallelism 10")
        # ips = ', '.join(tuple(ip for ip in self.results['scan']))
        # self.results = nm.scan(hosts=self.range, arguments="-sS -n -T4 -F --min-hostgroup 256 --min-parallelism 10")

        # print(self.results)
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
 
