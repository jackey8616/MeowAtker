from __future__ import unicode_literals, print_function 
import traceback, os, click
click.disable_unicode_literals_warning = True

from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.completion import PathCompleter

from utils.User import User
from utils.RedisManager import RedisManager
from utils.ftpd.handler import FTPHandler
from utils.Dashboard import Dashboard
from analysis.analysis import Analysis
from exploit.exploit import Exploit

user = None
redis = None
ftp = None

dashboard = None

stopSignal = False
select = ''

def init(debug):
    try:
        redis.start()
        dashboard.start()
        if user.getRole() == 'None':
            ftp.start()
        return True
    except Exception as e:
        if debug:
            traceback.print_exc()
        return False


def stop(debug):
    try:
        if user.getRole() == 'None':
            ftp.stop()
        dashboard.stop()
        redis.stop()
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
def main(debug, data_path, username, role, host_ip, redis_port, ftp_port):

    ftpText       = '===============================\n              ftp              \n===============================\n'
    dashboardText = '===============================\n           Dashboard           \n===============================\n'
    exploitText   = '===============================\n            Exploit            \n===============================\n'
    defenseText   = '===============================\n            Defense            \n===============================\n'
    analysisText  = '===============================\n           Analysis            \n===============================\n'

    ftp_field = TextArea(text=ftpText, height=10)
    dashboard_field = TextArea(text=dashboardText)
    exploit_field = TextArea(text=exploitText)
    defense_field = TextArea(text=defenseText)
    analysis_field = TextArea(text=analysisText)

    input_field = TextArea(
            height=1, 
            prompt=' > ', 
            style='class:input-field',
            completer=PathCompleter()
            )


    global user, redis, ftp, dashboard
    user = User(username, role, dashboard_field)
    redis = RedisManager(ip=host_ip, port=redis_port, printField=dashboard_field, user=user, debug=debug)
    ftp = FTPHandler(ip=host_ip, port=ftp_port, path=data_path + 'ftp/', user=user, printField=ftp_field)

    analysis = Analysis(redis, None, ftp, [dashboard_field, analysis_field])
    exploit = Exploit(redis, None, ftp, [dashboard_field, exploit_field])
    dashboard = Dashboard(redis, exploit, None, analysis, dashboard_field, debug=debug)

    if user.getRole() == 'None':
        leftSplit = HSplit([
            ftp_field,
            Window(height=1, char='-', style='class:line'),
            dashboard_field
        ])
    else:
        leftSplit = dashboard_field

    container = HSplit([
        VSplit([
            leftSplit,
            Window(width=1, char='|', style='class:line'),
            HSplit([
                exploit_field,
                Window(height=1, char='-', style='class:line'),
                defense_field,
                Window(height=1, char='-', style='class:line'),
                analysis_field
            ])
        ]),
        Window(height=1, char='-', style='class:line'),
        input_field
    ])

    kb = KeyBindings()

    @kb.add('c-q')
    def _(event):
        event.app.exit()

    @kb.add('c-c')
    def _(event):
        input_field.text = ''

    @kb.add('c-o')
    def _(event):
        global select
        if 'Exploit' in select:
            exploit.process(select, 'help')
        elif 'Defense' in select:
            pass
        elif 'Analysis' in select:
            analysis.process(select, 'help')
        else:
            dashboard.process(select, 'help')


    @kb.add('enter')
    def _(event):
        global stopSignal, select
        userInput = input_field.text
        if userInput == 'init':
            stopSignal = not init(debug)
        elif userInput == 'stop':
            stopSignal = stop(debug)
        elif userInput == 'exit':
            if not stopSignal:
                stop(debug)
            application.exit()
        elif 'Exploit' in select or userInput.startswith('exploit'):
            select = exploit.process(select, userInput.replace('exploit ', ''))
        elif 'Defense' in select or userInput.startswith('defense'):
            pass
        elif 'Analysis' in select or userInput.startswith('analysis'):
            select = analysis.process(select, userInput.replace('analysis ', ''))
        elif userInput.startswith('help'):
            dashboard.process(select, userInput)
        else:
            dashboard.process(select, userInput)
       
        input_field.text = ''

    style = Style([
        ('output-field', 'bg:#000044 #ffffff'),
        ('input-field', 'bg:#000000 #ffffff'),
        ('line', '#004400')
    ])

    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        full_screen=True
    )

    application.run()


if __name__ == '__main__':
    main()
