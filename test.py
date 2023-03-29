"""
21.03.2023
"""

import subprocess
from os import popen
from pywinos import WinOSClient
import winrm


def change_boot_priority(ip_address,system):
    session = winrm.Session(ip_address, auth=("junioradmin", "junioradmin"))
    test = f"bcdedit  | Select-String '{system}' -Context 3,0 | ForEach-Object {{ $_.Context.PreContext[0] -replace '^Bezeichner +\' }}"
    print(test)
    run = session.run_ps(f"bcdedit | Select-String '{system}' -Context 3,0 | ForEach-Object {{ $_.Context.PreContext[0] -replace '^identifier +\' }}")
    id = str(run.std_out)[2:-5]
    session.run_ps(f"bcedit /default \"{id}\"")
    session.run_ps("shutdown /r /t 0")
    return id


def trustedhosts(ip_address):
    subprocess.call(
        f"powershell Set-Item WSMan:\localhost\Client\TrustedHosts -Value '{ip_address}' -Concatenate -Force")

def multiple_hosts(filename):
    for line in filename:
        trustedhosts(line)
        change_boot_priority(line)

print(change_boot_priority('10.0.0.18','GNS3-Security'))