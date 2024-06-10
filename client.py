# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:03:47 2024

@author: weiji
"""

import socket
from threading import Thread
import tkinter as tkt

def receive():
    #Gestisce la ricezione dei messaggi.
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode(ENCODE)
            msg_list.insert(tkt.END, msg)
        except OSError:
            break

def send(event=None):
    #Gestisce l'invio dei messaggi.
    msg = my_msg.get()
    my_msg.set("")
    try:
        client_socket.send(bytes(msg, ENCODE))
        if msg == "{quit}":
            client_socket.close()
            finestra.quit()
    except OSError:
        pass

def on_closing(event=None):
    #Gestisce la chiusura della finestra.
    my_msg.set("{quit}")
    send()

# Configurazione della finestra principale di Tkinter
finestra = tkt.Tk()
finestra.title("Chat")

messages_frame = tkt.Frame(finestra)
my_msg = tkt.StringVar()
my_msg.set("Scrivi qui i tuoi messaggi")
scrollbar = tkt.Scrollbar(messages_frame)

msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkt.Entry(finestra, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkt.Button(finestra, text="Invia", command=send)
send_button.pack()

finestra.protocol("WM_DELETE_WINDOW", on_closing)

# Connessione al server
HOST = input('Inserire il server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZE = 1024
ADDR = (HOST, PORT)
ENCODE = "utf8"

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(ADDR)
except Exception as e:
    print(f"Errore nella connessione al server: {e}")
    finestra.quit()

# Avvio del thread per la ricezione dei messaggi
receive_thread = Thread(target=receive)
receive_thread.start()

# Avvio del loop principale di Tkinter
tkt.mainloop()

