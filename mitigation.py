import paramiko

class Mitigation():
    def __init__(self, router):
        self.router = router

    def firewall(self, target_ip, target_lower_port, target_protocol):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.router, username='tkonishi', password='0000')
        print(f'sudo ufw route deny to {target_ip} port {target_lower_port} proto {target_protocol}')

        stdin, stdout, stderr = client.exec_command(f'sudo ufw route deny to {target_ip} port {target_lower_port} proto {target_protocol}')
        for line in stdout:
            print(line)

        client.close()
