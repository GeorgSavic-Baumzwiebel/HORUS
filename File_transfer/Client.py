import socket
import tkinter
from tkinter import filedialog
import ctypes
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "10.0.0.179"
# the port, let's use 5001
port = 5001
# with ctypes with can increase the DPI of the window and therefore increase resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = tkinter.Tk()
root.withdraw()
# the name of file we want to send, make sure it exists
filename = tkinter.filedialog.askopenfilename()
# get the file size
filesize = os.path.getsize(filename)
print(f"File: {filename} selected")

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission is sent
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
