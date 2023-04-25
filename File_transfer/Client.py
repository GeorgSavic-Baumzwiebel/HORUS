import socket
import re
import os


def get_ethernet_ip():
    # Create Regext to find all room 76 addresses
    regex = re.compile(r'10.0.76.\d')
    # Get a list of all network interfaces
    interfaces = socket.getaddrinfo(socket.gethostname(), None)
    # Find only addresses that match regex (should be exactly 1)
    interfaces = [interface[4][0] for interface in interfaces if bool(regex.match(interface[4][0]))]
    # Return IP
    return interfaces[0]

CLIENT_HOST = get_ethernet_ip()
# Port to run the socket on
SERVER_PORT = 5001
# Junk Seperator
SEPARATOR = "<SEPARATOR>"
# How many Bytes we are sending each time
BUFFER_SIZE = 4096

s = socket.socket()
s.bind((CLIENT_HOST, SERVER_PORT))
# Listen to max 1 connection
s.listen(1)
print(f"[*] Listening as {CLIENT_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] Getting file from{address}")

# receive the file infos
# receive using the client socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# Delete the file if it exists (fixes error with overwriting)
if os.path.exists(filename):
    os.remove(filename)
# Absolete: remove absolute path if there is
# filename = os.path.basename(filename)
# convert Filesize to integer
filesize = int(filesize)

# start receiving the file from the socket and write it down
with open(filename, "wb") as f:
    while True:
        # read 4096 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # write the bytes we just received
        f.write(bytes_read)

# close the client socket
client_socket.close()
# close the entire socket
s.close()
