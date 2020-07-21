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
        stdin, stdout, stderr = client.exec_command(
            'sudo tc qdisc del dev enp0s3 root')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc qdisc add dev enp0s3 root handle 1: htb default 10')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc class add dev enp0s3 parent 1: classid 1:1 htb rate 1000mbit ceil 1000mbit burst 10mb cburst 10mb')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc class add dev enp0s3 parent 1:1 classid 1:10 htb rate 1kbit ceil 1000mbit burst 10mb cburst 10mb')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc class add dev enp0s3 parent 1:1 classid 1:20 htb rate 1kbit ceil 1mbit burst 10mb cburst 10mb')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc qdisc add dev enp0s3 parent 1:10 handle 100: pfifo limit 1000')
        for line in stdout:
            print(line)
        stdin, stdout, stderr = client.exec_command(
            'sudo tc qdisc add dev enp0s3 parent 1:20 handle 200: pfifo limit 1000')
        for line in stdout:
            print(line)
        for scope in mitigationrequest['ietf-dots-signal-channel:mitigation-scope']['scope']:
            for target_prefix in scope['target-prefix']:
                target_ip = re.sub(r'/\d*', '', target_prefix)
                for target_port_range in scope['target-port-range']:
                    target_lower_port = target_port_range['lower-port']
                    for target_protocol in scope['target-protocol']:
                        command = f'sudo tc filter add dev enp0s3 protocol ip parent 1:0 prio 1 u32 match ip dst {target_ip} match ip dport {target_lower_port} 0xffff match ip protocol {target_protocol} 0xff flowid 1:20'
                        print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        for line in stdout:
                            print(line)
        client.close()
