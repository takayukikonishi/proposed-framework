import re

import paramiko


class Mitigation():
    def __init__(self, router):
        self.router = router

    def drop(self, mitigationrequest):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.router, username='tkonishi', password='0000')
        for scope in mitigationrequest['ietf-dots-signal-channel:mitigation-scope']['scope']:
            for target_prefix in scope['target-prefix']:
                target_ip = re.sub(r'/\d*', '', target_prefix)
                for target_port_range in scope['target-port-range']:
                    target_lower_port = target_port_range['lower-port']
                    for target_protocol in scope['target-protocol']:
                        if target_protocol == 6:
                            target_protocol = 'tcp'
                        elif target_protocol == 17:
                            target_protocol = 'udp'
                        command = f'sudo ufw route deny to {target_ip} port {target_lower_port} proto {target_protocol}'
                        print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        for line in stdout:
                            print(line)
        client.close()

    def shaping(self, mitigationrequest):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.router, username='tkonishi', password='0000')
        for scope in mitigationrequest['ietf-dots-signal-channel:mitigation-scope']['scope']:
            for target_prefix in scope['target-prefix']:
                target_ip = re.sub(r'/\d*', '', target_prefix)
                for target_port_range in scope['target-port-range']:
                    target_lower_port = target_port_range['lower-port']
                    for target_protocol in scope['target-protocol']:
                        if target_protocol == 6:
                            target_protocol = 'tcp'
                        elif target_protocol == 17:
                            target_protocol = 'udp'
                        command = f'sudo ufw route limit to {target_ip} port {target_lower_port} proto {target_protocol}'
                        print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        for line in stdout:
                            print(line)
        client.close()
