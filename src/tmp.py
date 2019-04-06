import subprocess
import getpass
import sys
import re
import pwd

command = 'python -m webbrowser -n http://129.108.7.29:8085'
if re.match('linux', sys.platform):
    for p in pwd.getpwall():
        if p[3] >= 999 and re.match('/home', p[5]):
            user = p[0]
            break
    subprocess.call("su - " + user + " -c '" + command + "'", shell=True)
elif re.match('win32', sys.platform):
    user = getpass.getuser()
    print(user)
    # subprocess.call("runas /noprofile /user:" + user + command, shell=True)
