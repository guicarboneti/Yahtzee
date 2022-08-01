from asyncio import FastChildWatcher
import socket

IP = "127.0.0.1"
PORT = 5003

receiveFrom = 5002
sendTo = 5000

relayBaton = False