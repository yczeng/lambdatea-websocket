#!/usr/bin/env python3

import sys
import math
import time
import tkinter
import os
from io import BytesIO
from websocket_server import WebsocketServer
import string
from multiprocessing import Process, Queue

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	#server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	print("Client(%d) said: %s" % (client['id'], message))
	old_balance = float(os.popen('venmo balance').read().strip('\n'))

	venmo_waiting = True
	while venmo_waiting:
		new_balance = float(os.popen('venmo balance').read().strip('\n'))
		
		if new_balance - old_balance >= 0.01:
			server.send_message(client, "uramazing. emailusat hello@lambdatea.com")
			venmo_waiting = False

PORT=9001
HOST="172.31.27.32"
server = WebsocketServer(PORT, HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

def runserver():
	server.run_forever()

def venmo():
	while True:
		time.sleep(1)
		os.system('venmo balance')

first = Process(target=runserver, args=())
second = Process(target=venmo, args=())

first.start()
second.start()
