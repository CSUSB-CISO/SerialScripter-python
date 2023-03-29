from nmap import PortScanner
from os import popen 
from json import dump
from website.models import create_host_from_dict
from re import compile
from sqlalchemy.exc import IntegrityError
class Recon:
    def __init__(self, range: str) -> None:
        self.range = range
        nm = PortScanner()
        self.results = nm.scan(hosts=self.range, arguments="-T4 -F")
        
        self.hosts = self.set_box_ips()
        self.box_data = self.init_box_data(self.hosts, self.get_TTLs(self.hosts))

    def set_box_ips(self) -> tuple:
        return tuple(ip for ip in self.results["scan"] if "tcp" in self.results["scan"][ip])
    
    def get_TTLs(self, hosts: tuple) -> tuple:
        TTLs = list()

        for ip in hosts:
            try:
                response = popen(f"ping {ip} -c 1").readlines()[1]
                pattern = compile('ttl=\d*')
                TTLs.append(int(pattern.search(str(response)).group().split("=")[1]))
            except AttributeError:
                print(f"PING blocked by ip {ip}")
                TTLs.append(None)

        return tuple(TTLs)

    def init_box_data(self, hosts: tuple, TTLs: tuple) -> tuple:
        box_data = list()
        for i, ip in enumerate(hosts):
            if TTLs[i] != None:
                if TTLs[i] > 128:
                    os = "Unkown"
                elif TTLs[i] >= 120:
                    os = "Windows"
                else:
                    os = "Linux"
                box_data.append(
                        {
                            "hostname": self.results["scan"][ip]["hostnames"][0]["name"],
                            "name": f'host-{ip.split(".")[-1]}',
                            "ip": ip,
                            "OS": os,
                            "services": [
                                {
                                    "port": port,
                                    "service": self.results["scan"][ip]["tcp"][port]["name"]
                                } for port in self.results["scan"][ip]["tcp"]
                            ],
                            "isOn": False,
                            "isChanged": False,
                            "isConnected": False,
                            "timeConnected": "",
                            "docker": [],
                            "tasks": [{}],
                            "firewall": [],
                            "shares": [
                                {
                                    "NetName": "",  
                                    "Remark": "",  
                                    "Path": "", 
                                    "Type": "", 
                                    "Permissions": "",  
                                    "MaxUses": "", 
                                    "CurrentUses": "", 
                                }
                            ],
                        }
                    )


        return tuple(box_data)

    def get_box_data(self):
        return self.box_data

    def save_box_data(self, db):
        for box in self.box_data:
            print(box)
            host = create_host_from_dict(box)
            try:
                db.session.add(host)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print("Inventory has been ran already")