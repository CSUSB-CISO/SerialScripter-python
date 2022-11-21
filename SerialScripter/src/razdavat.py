from paramiko import SSHClient, AutoAddPolicy
from time import sleep


class Razdavat(SSHClient):
    def __init__(self, server: str, password: str = None, key_path: str = None ,port: int = 22, user: str = 'root', os="linux") -> None:
        super().__init__()
        self.set_missing_host_key_policy(AutoAddPolicy())
        self.server = server
        self.os = os

        if key_path:
            self.connect(
                server,
                username=user,
                key_filename=key_path,
                port=port
            )
        elif password:
            self.connect(
                server,
                username=user,
                password=password,
                port=port
            )
        else:
            print("INVALID LOGIN TYPE")

    def add_ssh_key(self, key_to_add: str) -> None:
        self.exec_command(f'yes "y" | ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/host-{self.server.split(".")[-1]} -N ""')
        self.exec_command(f'echo {key_to_add} >> ~/.ssh/authorized_keys')

    def remove_ssh_key(self, key_to_delete: str) -> None:
        _, stdout, _ = self.exec_command("cat ~/.ssh/authorized_keys")
        keys = stdout.readlines()
        self.exec_command(f'echo -n "" > ~/.ssh/authorized_keys')
        for key in keys:
            if key not in (key_to_delete+"\n", "\n"):
                self.exec_command("echo "+key.replace('\n', "")+">> ~/.ssh/authorized_keys")

    def put(self, script_name, script_path='/tmp/'):
        sftp = self.open_sftp()
        sftp.put(f'scripts/{self.os}/'+script_name, script_path+script_name)
        sftp.chmod(script_path+script_name, 777)
        sftp.close()

    def get(self, file, file_path='/tmp/'):
        sftp = self.open_sftp()
        sftp.get(file_path+file, file)
        sftp.close()

    def deploy(self, script_name, script_path='/tmp/'):
        if script_path[-1] != "/":
            script_path += "/"
        self.put(script_name, script_path=script_path)
        self.exec_command(f'{script_path}{script_name}')
