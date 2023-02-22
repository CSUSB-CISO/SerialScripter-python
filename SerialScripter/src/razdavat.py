import paramiko

class Razdavat(paramiko.SSHClient):
    def __init__(self, server: str, password: str = None, key_path: str = None ,port: int = 22, user: str ="", os="linux") -> None:
        super().__init__()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.server = server
        
        self.user = "root" if "windows" not in os.lower() else "Administrator" if not user else user
        self.os = os


        if key_path:
            self.connect(
                server,
                username=self.user,
                key_filename=key_path,
                port=port
            )
        elif password:
            self.connect(
                server,
                username=self.user,
                password=password,
                port=port
            )
        else:
            print("INVALID LOGIN TYPE")

    def add_ssh_key(self, key_to_add: str) -> None:
        if "windows" in self.os.lower():
            self.exec_command(f"echo {key_to_add} >> C:\\ProgramData\\ssh\\administrators_authorized_keys")
        else:
            # make .ssh dir and create authorized_keys file if they dont already exist
            self.exec_command(f'yes "y" | mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys')
            # change perms
            self.exec_command(f'chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys')
            # edit ssh config
            self.exec_command(f'echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config')
            self.exec_command(f'ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/host-{self.server.split(".")[-1]} -N ""')
            self.exec_command(f'echo {key_to_add} >> ~/.ssh/authorized_keys')

    def remove_ssh_key(self, key_to_delete: str) -> None:
        if "windows" in self.os.lower():
            _, stdout, _ = self.exec_command(f"cat C:\\ProgramData\\ssh\\administrators_authorized_keys")
            keys = stdout.readlines()
            self.exec_command(f'echo -n "" > C:\\ProgramData\\ssh\\administrators_authorized_keys')
            for key in keys:
                if key not in (key_to_delete+"\n", "\n"):
                    self.exec_command("echo "+key.replace('\n', "")+">> C:\\ProgramData\\ssh\\administrators_authorized_keys")
        else:
            _, stdout, _ = self.exec_command("cat ~/.ssh/authorized_keys")
            keys = stdout.readlines()
            self.exec_command(f'echo -n "" > ~/.ssh/authorized_keys')

            for key in keys:
                if key not in (key_to_delete+"\n", "\n"):
                    self.exec_command("echo "+key.replace('\n', "")+">> ~/.ssh/authorized_keys")

    # put script onto machine
    def put(self, script_name, script_path='/opt/memento/'):

    
        if "windows" not in self.os.lower():
            
            # os variable is necessary because of the directory structure on local machine 
            # where scripts are located in linux and windows respectively
            os = "linux"
            try:
                self.exec_command("mkdir /opt/memento/")
            except:
                print("Directory already exists")
        else:
            os = "windows"
            script_path = "C:/Windows/temp/"

        sftp = self.open_sftp()
        sftp.put(f'scripts/{os}/'+script_name, script_path+script_name)
        sftp.chmod(script_path+script_name, 777)
        sftp.close()

    def get(self, file, file_path='/'):
        sftp = self.open_sftp()
        sftp.get(file_path+file, file)
        sftp.close()

    def deploy(self, script_name, params, script_path="/opt/memento"):
        self.put(script_name, script_path=script_path)
        if params:
            self.exec_command(f'{script_path}{script_name} {params}')
            print(f'{script_path}{script_name} {params}')
        else:
            self.exec_command(f'{script_path}{script_name}')
            

