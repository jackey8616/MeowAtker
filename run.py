from __future__ import unicode_literals, print_function 
import os, sys, traceback
import click

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.patch_stdout import patch_stdout

from utils.User import User
from utils.RedisManager import RedisManager
from utils.ftpd.handler import FTPHandler
from utils.Dashboard import Dashboard
from analysis.analysis import Analysis
from exploit.exploit import Exploit

click.disable_unicode_literals_warning = True

user = None
redis = None
ftp = None

dashboard = None

def init(debug):
    try:
        redis.start()
        dashboard.start()
        if user.getRole() == 'None':
            ftp.start()
        print('Inited')
        return True
    except Exception as e:
        if debug:
            traceback.print_exc()
        return False


def stop(debug):
    try:
        redis.stop()
        dashboard.stop()
        if user.getRole() == 'None':
            ftp.stop()
        return True
    except Exception as e:
        if debug:
            traceback.print_exc()
        return False

@click.command()
@click.option('--debug', default=False, type=bool)
@click.option('--data-path', default=os.getcwd() + '/data/', type=str)
@click.option('--username', default=None, type=str)
@click.option('--role', default='None', type=str)
@click.option('--host-ip', default='127.0.0.1', type=str)
@click.option('--redis-port', default=6379, type=int)
@click.option('--ftp-port', default=21, type=int)
def run(debug, data_path, username, role, host_ip, redis_port, ftp_port):
    global user, redis, ftp
    user = User(username, role)
    redis = RedisManager(ip=host_ip, port=redis_port, debug=debug)
    ftp = FTPHandler(ip=host_ip, port=ftp_port, path=data_path + 'ftp/', user=user)

    history = InMemoryHistory()
    history.append_string('init')
    history.append_string('stop')
    history.append_string('exit')
    history.append_string('analysis')
    history.append_string('exploit')
    history.append_string('defense')
    session = PromptSession(history=history,
            auto_suggest=AutoSuggestFromHistory(), 
            completer=PathCompleter(),
            complete_in_thread=True,
            complete_while_typing=True,
            enable_history_search=True)

    global dashboard
    dashboard = Dashboard(redis)
    analysis = Analysis(session, ftp)
    exploit = Exploit(session, ftp)

    stopSignal = False

    while True:
        with patch_stdout():
            text = '''MeowAtker
init        -   Service init command
stop        -   Service stop command
exit        -   Service exit command


analysis    -   Analysis
exploit     -   Exploit
defense     -   Defense 
> '''
            user_input = session.prompt(text)
        if user_input == 'init':
            stopSignal = not init(debug)
        elif user_input == 'stop':
            stopSignal = stop(debug)
        elif user_input == 'exit':
            if not stopSignal:
                stop(debug)
            sys.exit(0)
        elif user_input.startswith('analysis'):
            analysis.process(user_input.replace('analysis ', ''))
        elif user_input.startswith('exploit'):
            exploit.process(user_input.replace('exploit ', ''))
        else:
            print('Maybe this is not a valid command.')


if __name__ == "__main__":
    run()
    
