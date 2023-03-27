"""
21.03.2023
"""

import subprocess
from os import popen
from pywinos import WinOSClient
import winrm


def change_boot_priority(ip_address):
    session = winrm.Session('10.0.0.9', auth=("junioradmin", "junioradmin"))
    run = session.run_cmd() # to be finished



def trustedhosts(ip_address):
    subprocess.call(
        f"powershell Set-Item WSMan:\localhost\Client\TrustedHosts -Value '{ip_address}' -Concatenate -Force")

def multiple_hosts(filename):
    for line in filename:
        trustedhosts(line)
        change_boot_priority(line)
