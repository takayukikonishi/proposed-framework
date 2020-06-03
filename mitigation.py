import paramiko

class Mitigation():
    def __init__(self, target_ip):
        self.target_ip = target_ip

    def firewall(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.2.0.3', username='user-router', password='0000')

        stdin, stdout, stderr = client.exec_command(f'sudo ufw route deny to {self.target_ip}')
        for line in stdout:
            print(line)

        client.close()
