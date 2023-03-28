"""
21.03.2023
"""

import subprocess
from os import popen
from pywinos import WinOSClient
import winrm


def change_boot_priority(ip_address):
    session = winrm.Session(ip_address, auth=("security", "security"))
    run = session.run_cmd('hostname')
    return run.std_out



def trustedhosts(ip_address):
    subprocess.call(
        f"powershell Set-Item WSMan:\localhost\Client\TrustedHosts -Value '{ip_address}' -Concatenate -Force")

def multiple_hosts(filename):
    for line in filename:
        trustedhosts(line)
        change_boot_priority(line)

print(change_boot_priority('10.0.76.6'))