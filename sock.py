# -*- coding: utf-8 -*-

# Importo les llibreries
import socket
from variables_globals import *

#Creo el socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Indico l'adreça i el port del servidor
server.bind((host,port))

#Poso el servidor a escoltar
server.listen(backlog)

#Creo la llista entrada amb de moment només el socket
entrada = [server]