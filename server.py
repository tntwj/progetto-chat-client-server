# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:46:43 2024

@author: weijie
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZE = 1024
ADDR = (HOST, PORT)
ENCODE = "utf8"

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accetta_connessioni_in_entrata():
    while True:
        try:
            client, client_address = SERVER.accept ()
            print("%s:%s sÌ è collegato." % client_address)
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", ENCODE))
            indirizzi [client] = client_address
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=gestisce_client, args=(client,)).start()  
        except Exception as e:
            print(f"Errore nell'accettare le connessioni: {e}")

        
def gestisce_client(client):
    try:
        nome = client.recv(BUFSIZE).decode("utf8")
        benvenuto = 'benvenuto %s, se vuoi lasciare la chat, scrivi {quit} per uscire' % nome
        client.send(bytes(benvenuto, ENCODE))
        msg = "%s si è unito all chat!" % nome
        broadcast(bytes(msg, ENCODE))
        clients[client] = nome
        while True:
            msg = client.recv(BUFSIZE)
            if msg != bytes("{quit}", ENCODE):
                broadcast(msg, nome + ": ")
            else:
                client.send(bytes("{quit}", ENCODE))
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la chat" % nome, ENCODE))
                break
    except (OSError, ConnectionResetError):
        client.close()
        if client in clients:
            nome = clients[client]
            del clients[client]
            broadcast(bytes("%s ha abbandonato la chat" % nome, ENCODE))

def broadcast(msg, prefisso=""):
    for utente in clients:
        try:
            utente.send(bytes(prefisso, ENCODE) + msg)
        except Exception as e:
            print(f"Errore nell'invio del messaggio a {clients[utente]}: {e}")
            utente.close()
            del clients[utente]
    
SERVER.listen(5)
print("In attesa di connessioni...")
ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()    