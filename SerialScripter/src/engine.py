#!/usr/bin/python3
import os
import re
from core.razdavat import Razdavat
from pathlib import Path
class Engine:
    """
    This class is a collection of classes and methods which build up
    the scripting engines core backend functionallity
    """

    
    def dos_2_unix():
        """Make all scripts unix files"""
        mydir = Path("scripts/linux")
        for file in mydir.glob('*'):
            text = open(file, 'rb').read().replace(b'\r\n', b'\n')
            open(file, 'wb').write(text)

    @staticmethod
    def load_scripts(os_name: str) -> list:
        """
        Loads all CCDC scripts for a specified operating system

        :param str os_name: name of the desired operating scripts
        :rtype: list[tuple[int, function]]
        """

        rList = list()

        mydir = Path(f"scripts/{os_name}")
        for file in mydir.glob('*'):
            rList.append((file.name, None))
        return rList

    @staticmethod
    def load_host_options(menu) -> list:
        """
        Loads all hosts specified in the hosts-list_1.log and adds 
        them as options on the specified menu

        :param :class:'Menu<gui.ui.Menu>' menu: The menu to add our host options to
        :rtype: list[tuple[int, function]]
        """

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        rList = list()

        with open(f'hosts.log') as file:
            file_contents = file.read()

        for i, j in enumerate(re.findall("\[(.*?)\]", file_contents)):
            rList.append((f'[{alphabet[i]}] [{j}]', menu.start))

        rList.append(("[<] Go back", print))

        return rList

    @staticmethod
    def get_ips() -> tuple:
        """
        Parses and returns a list of all IPs from the hosts-list_1.log file

        :rtype: tuple[tuple]
        """
        host_ips = list()

        with open(f'hosts.log') as file:
            hosts = file.read()

        hosts = hosts.split('\n\n')
        for i in range(len(hosts)):
            hosts[i] = hosts[i][hosts[i].find("]")+1:]

        for j in range(len(hosts)):
            host_ips.append(tuple(hosts[i].split()))

        return tuple(host_ips)

    @staticmethod
    def command_handler(entries, BackupMenu, HardenMenu):
        a = Razdavat('52.188.170.74',
                             input("Input host password:\n"))
        if "backup.sh" in entries:
            BackupMenu().start()
            entries.pop(
                entries.index("backup.sh")
            )
        if "hardening_v1.0.0.sh" in entries:
            HardenMenu().start()
            entries.pop(
                entries.index("hardening_v1.0.0.sh")
            )
        for entry in entries:
            a.deploy(entry)
