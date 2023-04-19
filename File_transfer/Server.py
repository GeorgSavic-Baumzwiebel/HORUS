import socket
import tkinter
from tkinter import filedialog
import ctypes
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
host = ["192.168.0.1", "192.168.0.1"]
port = 5001
# with ctypes we can increase the DPI of the window and therefore increase resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = tkinter.Tk()
root.withdraw()
# Opens a GUI for Users to select the files to be sent
filename = tkinter.filedialog.askopenfilename()
filesize = os.path.getsize(filename)

# creating the socket
print("[+] Waiting . . .")
# send to all devices in our list
for a in host:
    s = socket.socket()
    s.connect((a, port))
    print(f"[*] Sending to {a}:{port}")

    # Sending the filename and filesize, seperated by a junk message
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # Progress bar of transfer
    progress = tqdm.tqdm(range(filesize), f"Sending {filename} to {a}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file into a buffer
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            #send the buffer
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    s.close()