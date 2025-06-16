###[PyZerotrust]###
## Zerofish0      #
## version :0.1   #
###################
# Importations
import socket
import threading
import random
from ui import PyZeroTrustUI

# Main class
class PyZeroTrust:
    def __init__(self) -> None :
        self.instance_name = str()
        self.mode = str()
        self.ui = PyZeroTrustUI()
        self.running = True
        self.initiated = False

        # server var
        self.server_port = int()
        self.server_ip = str()

        # client var
        self.host_ip = str()
        self.host_port = int()

    def initiate(self) :
        self.ui.error("###[ZeroTrust Chat App]###")
        self.ui.running(" - Never trust anyone")
        self.ui.success("===[Initialization]===")

        self.initiated = True

        self.instance_name = self.ui.ui_input("Enter your name (leave blank for random): ", default=f"Anon{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}")

        mode = self.ui.ui_input("Enter mode (client/server): ")
        if not mode in ["client", "server"]:
            raise ValueError("Invalid mode")
        self.mode = mode

        if self.mode == "server" :
            self.server_ip = self.ui.ui_input("Enter server IP (leave blank for local): ", default=self._getLocalIp())
            self.server_port = int(self.ui.ui_input("Enter server port (default : 12002): ", default="12002"))

        elif self.mode == "client" :
            self.host_ip = self.ui.ui_input("Enter host IP (leave blank for local): ", default=self._getLocalIp())
            self.host_port = int(self.ui.ui_input("Enter host port (default : 12002): ", default="12002"))

        self.ui.success("Initialization complete")

    def run(self) :
        self.ui.success("===[Starting]===")
        if self.initiated :
            if self.mode == "server" :
                self.startServer()
            elif self.mode == "client" :
                self.startClient()
        else :
            self.ui.error("Please initalize first")

    def _getLocalIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # On essaie de se "connecter" à une IP quelconque (pas besoin que ça marche)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def _listenForMessages(self, connection, peer_name):
        while self.running:
            try:
                # receive the message
                raw_data = connection.recv(1024)
                # if there is no data received, close the connection
                if not raw_data:
                    break
                # else, receive and decode the message
                message = raw_data.decode()
                # if the message is "exit00", close the chat
                if message == "exit00":
                    self.ui.peerMessage(f"{peer_name} killed the conversation.", peer_name, self.instance_name)
                    connection.close()
                    break

                # else, print the message
                self.ui.peerMessage(message, peer_name, self.instance_name)
            except Exception as e:
                self.ui.error(f"\nError during reception : {e}")
                break
        raise OSError("Conversation terminated.")

    def _sendMessages(self, connection, peer_name : str) :
        """Send messages to the peer, and if it contains "exit", kill the conversation"""
        while self.running :
            try :
                message = self.ui.ui_input(f"{self.instance_name} (you) : ")

                if message == "exit00":
                    connection.sendall(message.encode())
                    self.ui.ownMessage("You killed the conversation.")
                    connection.close()
                    break
                connection.sendall(message.encode())
            except Exception as e:
                self.ui.error(f"Error while sending messages : {e}")
                break
        raise OSError("Conversation terminated.")

    def startServer(self):
        """Starts the server instance and listen for incoming connections, then, for every connection, it follows this protocol :
        - the client connects to the server (socket.connect)
        - then, the server accept the connection and wait for data
        - then, the client send his name to the server
        - the server respond with his own name
        - then, the client and the server can send message to each other (using threading to have a bidiractional chat)"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.server_ip, self.server_port))
        sock.listen(1)
        self.ui.running(f"[*] The server : {self.instance_name} is listening on {self.server_ip}:{self.server_port}")

        connection, address = sock.accept()
        self.ui.success(f"[+] Connection from {address} accepted")

        # the client sends his name to the server before sending any message
        peer_name = connection.recv(1024).decode()
        self.ui.success(f"[+] Client identified as {peer_name}")

        # the server sends his name to the client
        self.ui.running("[*] Authenticating ourselves...")
        connection.sendall(self.instance_name.encode())

        self.ui.success("[+] Authentication successful, conversation can start")
        self.ui.success("="*30)

        threading.Thread(target=self._listenForMessages, args=(connection,peer_name)).start()
        threading.Thread(target=self._sendMessages, args=(connection,peer_name)).start()

    def startClient(self):
        """Starts the client instance and connect to the server, then, for every connection, it follows this protocol :
        - the client connects to the server (socket.connect)
        - then, the server accept the connection and wait for data
        - then, the client send his name to the server
        - the server respond with his own name
        - then, the client and the server can send message to each other (using threading to have a bidiractional chat)"""
        self.ui.running(f"[*] Starting client : {self.instance_name}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host_ip, self.host_port))
        self.ui.success(f"[+] Client : {self.instance_name} connected to {self.host_ip}:{self.host_port}")

        # the client sends his name to the server before sending any message
        self.ui.running("[*] Authenticating ourselves...")
        sock.send(self.instance_name.encode())

        # the server respond with his own name
        server_name = sock.recv(1024).decode()
        self.ui.success(f"[+] Server identified as {server_name}")
        self.ui.success("[+] Authentication successful, conversation can start")
        self.ui.success("="*30)

        threading.Thread(target=self._listenForMessages, args=(sock, server_name)).start()
        threading.Thread(target=self._sendMessages, args=(sock, server_name)).start()

# Main program
if __name__ == "__main__":
    instance = PyZeroTrust()
    instance.initiate()
    instance.run()
