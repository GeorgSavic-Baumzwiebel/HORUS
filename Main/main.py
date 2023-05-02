"""
30.03.2023
"""
import json
import os
from multiprocessing import Pool, freeze_support
import subprocess
import winrm
import pdoc
import time
from wakeonlan import send_magic_packet


def change_boot_priority(ip_address, system, username, password):
    """
    This function is used to change the boot priority of a given host
    It works by opening up a winrm session with the remote host and then sending ps commands to it to change the boot priority.
    following that it restarts the system with the "shutdown /r /t 0" command.
    :param ip_address: The IP address of the remote host
    :param system: the subsystem description to change to
    :return: the GUID of the remote host
    """
    session = winrm.Session(ip_address, auth=(username, password))
    run = session.run_ps(
        f"bcdedit | Select-String '{system}' -Context 3,0 | ForEach-Object {{ $_.Context.PreContext[0] -replace '^identifier +\' }}")
    id = str(run.std_out)[2:-5]
    session.run_ps(f"bcedit /default \"{id}\"")
    session.run_ps("shutdown /r /t 0")
    return id

def check_OperatingSystem(ip_address, possible_accounts: list[dict]):
    """
    This function is used to get the operating system of the remote host
    :param ip_address: The IP of the Host to check
    :param possible_accounts: list of possible account names with their password and respective
    Operating System params: username, password, OS
    :return: The Operating System running on the specified host
    """
    for account in possible_accounts:
        session = winrm.Session(ip_address,auth=(account.get("username"), account.get("password")))
        try:
            session.run_cmd("ipconfig")
        except winrm.exceptions.InvalidCredentialsError:
            continue
        return account.get("OS")

def trustedhosts(ip_address):
    """
    This function is used to add a speficied ip address to the list of trusted hosts
    :param ip_address: The IP address to add to the trusted host file on this machine
    :return: nothing
    """
    subprocess.run(
        f"powershell Set-Item WSMan:\localhost\Client\TrustedHosts -Value '{ip_address}' -Concatenate -Force")


def multiple_hosts(filename):
    """
    This function is used to iterate through a file containing multiple hosts and change the boot priority on each remote host
    :param filename: The file name containing the remote hosts seperated by line breaks containing one ip per line
    :return: nothing
    """
    args = {x.strip() for x in open(filename, "r").readlines()}
    pool = Pool()
    pool.map(trustedhosts, args, chunksize=10)
    time.sleep(1)


def wake_up_hosts(filename):
    """
    This functions wakes up all hosts specifies in the filename provided. This function only works if the specified
    hosts has been configured to wake up on magic packets
    :param filename: The json file containing the MAC-Addresses of the hosts to wake up
    :return: nothing
    """
    with open(filename) as file:
        file = json.load(file)
        file = [a['mac'] for a in file['pcs'] if not a['status']]
    for line in file:
        send_magic_packet(line)


def check_status(ip):
    """
    This function checks if the specified host (by IP) is currently running
    :param ip: The IP address to check
    :return: True if the host is currently running, False otherwise
    """
    return True if os.system("ping -c 1 " + ip) == 0 else False


if __name__ == '__main__':
    dictionary = {
        "username": "junioradmin",
        "password": "junioradmin",
        "OS": "tes123"
    }
    print(check_OperatingSystem("10.0.76.24", [dictionary]))
