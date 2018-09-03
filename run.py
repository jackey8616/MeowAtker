from __future__ import unicode_literals, print_function 
import os, sys
import click

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

from utils.User import User
from utils.RedisManager import RedisManager
from utils.ftpd.handler import FTPHandler
from analysis.analysis import Analysis
from exploit.exploit import exploit

click.disable_unicode_literals_warning = True

@click.command()
@click.option('--debug', default=False, type=bool)
@click.option('--data-path', default=os.getcwd() + '/data/', type=str)
@click.option('--username', default=None, type=str)
@click.option('--role', default='None', type=str)
@click.option('--host-ip', default='127.0.0.1', type=str)
@click.option('--redis-port', default=6379, type=int)
@click.option('--ftp-port', default=21, type=int)
def run(debug, data_path, username, role, host_ip, redis_port, ftp_port):
    user = User(username, role)
    redis = RedisManager(ip=host_ip, port=redis_port, debug=debug)
    ftp = FTPHandler(ip=host_ip, port=ftp_port, path=data_path + 'ftp/', user=user)

    analysis = Analysis(ftp)

    while True:
        with patch_stdout():
            text = '''MeowAtker
run         -   Service init command
stop        -   Service stop command
exit        -   Service exit command


analysis    -   Analysis
exploit     -   Exploit
defense     -   Defense 
> '''
            user_input = prompt(text)
        if user_input == 'run':
            redis.start()
            if user.getRole() == 'None':
                ftp.start()
        elif user_input == 'stop':
            redis.stop()
            if user.getRole() == 'None':
                ftp.stop()
        elif user_input == 'exit':
            sys.exit(0)
        elif user_input == 'analysis':
            analysis.process()
        elif user_input == 'exploit':
            exploit()




if __name__ == "__main__":
    run()
    
