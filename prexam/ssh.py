import paramiko

def ssh(ip, user='root', passwd='root', port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    on = ssh.connect(hostname=ip, port=port, username='root', password=passwd, timeout=2)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls')


if __name__ == '__main__':
    ssh('140.125.207.218', user='clode', passwd='123')
