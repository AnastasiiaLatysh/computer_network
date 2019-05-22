import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class Client(object):
    PORT = 8888
    BUFSIZ = 1024
    HOST = 'Anastasiias-MacBook-Pro.local'

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))

    def receive_message(self):
        while True:
            try:
                msg = self.socket.recv(self.BUFSIZ).decode("utf8")
                msg_list.insert(tkinter.END, msg)
            except OSError:
                break

    def send(self, event=None):
        msg = my_msg.get()
        my_msg.set("")
        self.socket.send(bytes(msg, "utf8"))
        if msg == "quit":
            self.socket.close()
            top.quit()

    def on_closing(self):
        my_msg.set("quit")
        self.send()

    def smile_button(self):
        my_msg.set(":)")
        self.send()

    def sad_button(self):
        my_msg.set(":(")
        self.send()


client = Client()

top = tkinter.Tk()
top.title("Client Chat")
messages_frame = tkinter.Frame(top)


# For the messages to be sent.
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

# Buttons, label, entry field elements
button_label = tkinter.Label(top, text="Enter message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="Black")
entry_field.bind("<Return>", client.send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=client.send)
send_button.pack()
smiley_button = tkinter.Button(top, text=":)", command=client.smile_button)
smiley_button.pack()
sad_button = tkinter.Button(top, text=":(", command=client.sad_button)
sad_button.pack()
quit_button = tkinter.Button(top, text="Quit", command=client.on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", client.on_closing)

receive_thread = Thread(target=client.receive_message)
receive_thread.start()
tkinter.mainloop()
