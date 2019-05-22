from socket import AF_INET, socket, SOCK_STREAM, gethostname
from threading import Thread

from log import log


class Server(object):
    PORT = 8888
    BUFSIZ = 1024

    def __init__(self):
        self.clients = {}
        self.addresses = {}
        self.opened_socket = socket(AF_INET, SOCK_STREAM)
        self.opened_socket.bind((gethostname(), self.PORT))

    def accept_connections(self):
        while True:
            client, client_address = self.opened_socket.accept()
            log.info("%s:%s has connected." % client_address)
            client.send(b"Hi :) Welcome to chat.\n Please write your name and press enter!")
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client, client_address)).start()

    def handle_client(self, client_conn, addr):
        name = client_conn.recv(self.BUFSIZ).decode("utf8")
        welcome = 'Welcome, %s! If you ever want to quit, type "quit" to exit.' % name
        client_conn.send(bytes(welcome, "utf8"))
        msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
        self.send_messages_to_all(bytes(msg, "utf8"))
        self.clients[client_conn] = name
        while True:
            try:
                msg = client_conn.recv(self.BUFSIZ)
                if msg != bytes("quit", "utf8"):
                    self.send_messages_to_all(msg, name + ": ")
                else:
                    client_conn.send(bytes("quit", "utf8"))
                    client_conn.close()
                    self.clients.pop(client_conn)
                    self.send_messages_to_all(bytes("%s has left the chat." % name, "utf8"))
                    break
            except ConnectionError:
                log.info(f"Client {addr} was disconnected by himself")
                break

    def send_messages_to_all(self, msg, user_name=""):
        try:
            for client_socket in self.clients:
                client_socket.send(bytes(user_name, "utf8") + msg)
        except BrokenPipeError:
            log.info("No possibility to send message to clients {}".format(self.clients))


if __name__ == "__main__":
    server = Server()
    server.opened_socket.listen(5)
    log.info("Server started !!")
    log.info("IP address is: {}".format(gethostname()))
    log.info("Wait for client connections...")
    accepted_thread = Thread(target=server.accept_connections)
    accepted_thread.start()
    accepted_thread.join()
    server.opened_socket.close()
