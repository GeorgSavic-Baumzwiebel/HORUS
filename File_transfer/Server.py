import socket
import tkinter
from tkinter import filedialog
import ctypes
import tqdm
import os
import json


# Get Ips from webserver Json file
def read_ips(file):
    with open(file) as file:
        file = json.load(file)
        file = [a['ip'] for a in file['pcs']]
    return file


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = read_ips('../HorusWebInterface/PCs.json')
port = 5001
# with ctypes we can increase the DPI of the window and therefore increase resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = tkinter.Tk()
root.withdraw()
# Opens a GUI for Users to select the files to be sent
filename = tkinter.filedialog.askopenfilename()
filesize = os.path.getsize(filename)

print("[+] Waiting for connection . . .")
# send to all ips in our list
for a in host:
    s = socket.socket()
    # Try to connect and send some data to check the connection
    try:
        s.connect((a, port))
        print(f"[*] Sending to {a}:{port}")

        # Sending the filename and filesize, separated by a junk message separator
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # Catch Socket Error
    except socket.error as err:
        print(f'Socket error on {a}:\n', err)
        # Continue sending to other hosts, we don't need to crash because of one error
        continue

    # Progress bar of transfer, tqdm == <3
    progress = tqdm.tqdm(range(filesize), f"Sending {filename} to {a}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read bytes from the file into a buffer
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # send the buffer
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
# Close the socket after all ips have had the file transferred
s.close()
