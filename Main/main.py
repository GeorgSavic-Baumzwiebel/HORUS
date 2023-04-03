"""
30.03.2023
"""
from multiprocessing import Pool, freeze_support
import subprocess
import winrm
import pdoc
import time
from wakeonlan import send_magic_packet


def change_boot_priority(ip_address, system):
    """
    This function is used to change the boot priority of a given host
    It works by opening up a winrm session with the remote host and then sending ps commands to it to change the boot priority.
    following that it restarts the system with the "shutdown /r /t 0" command.
    :param ip_address: The IP address of the remote host
    :param system: the subsystem description to change to
    :return: the GUID of the remote host
    """
    session = winrm.Session(ip_address, auth=("junioradmin", "junioradmin"))
    run = session.run_ps(
        f"bcdedit | Select-String '{system}' -Context 3,0 | ForEach-Object {{ $_.Context.PreContext[0] -replace '^identifier +\' }}")
    id = str(run.std_out)[2:-5]
    session.run_ps(f"bcedit /default \"{id}\"")
    session.run_ps("shutdown /r /t 0")
    return id


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
    args = {x.strip() for x in open(filename,"r").readlines()}
    pool = Pool()
    pool.map(trustedhosts, args, chunksize=10)
    time.sleep(1)


def wake_up_hosts(filename):
    file = {x.strip() for x in open(filename,"r").readlines()}
    for line in file:
        send_magic_packet(line)

if __name__ == '__main__':
    wake_up_hosts("ip_addresses.txt")
