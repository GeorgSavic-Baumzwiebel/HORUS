import socket
import tqdm
import re

# device's IP address
# Loop through the interfaces and find the first Ethernet interface
def get_ethernet_ip():
    # Get a list of all network interfaces
    regex = re.compile(r'10.0.76.\d')
    interfaces = socket.getaddrinfo(socket.gethostname(), None)
    # Filter to all that match regex(should be 1)
    interfaces = [interface[4][0] for interface in interfaces if bool(regex.match(interface[4][0]))]
    # Loop through the interfaces and find the first Ethernet interface
    return interfaces[0]

CLIENT_HOST = get_ethernet_ip()
SERVER_PORT = 5001
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

s = socket.socket()
s.bind((CLIENT_HOST, SERVER_PORT))
s.listen(3)
print(f"[*] Listening as {CLIENT_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] Getting message from{address}")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
# filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket and write it down
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()