import paramiko

from time import sleep


class Razdavat(paramiko.SSHClient):
    def __init__(self, server, password, port=22, user='root') -> None:
        super().__init__()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(
            server,
            username=user,
            password=password,
            port=port
        )

    def put(self, script, script_path='/tmp/'):
        sftp = self.open_sftp()
        sftp.put('scripts/linux/'+script, script_path+script)
        sftp.chmod(script_path+script, 777)
        sftp.close()

    def get(self, file, file_path='/tmp/'):
        sftp = self.open_sftp()
        sftp.get(file_path+file, file)
        sftp.close()

    def deploy(self, script, script_path='/tmp/'):
        out = script.split(".")[0]
        self.put(script, script_path)
        self.exec_command(f'{script_path}{script} > {script_path}{out}')
        sleep(4)
        self.get(out, script_path)
