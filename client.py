#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importo les llibreries
import socket
import RPi.GPIO as GPIO
import time

# Faig la configuració bàsica del GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) # Només utilitzo el 18. Es podria fer un bucle per activar-ne diversos alhora.


# Indico la IP del servidor i el port de comunicació
host = "PLACE_YOUR_SERVER_IP_HERE"
port = 12345

# Inicio un bucle infinit
while 1:
    s = socket.socket() # Creo el socket
    s.connect((host, port)) # Connecto al servidor
    data = s.recv(1024) # Rebo dades

    GPIO.output(int(data), GPIO.HIGH) # La dada rebuda indica el pin del gpio que es farà UP
    time.sleep(1) # S'espera 1 segon
    GPIO.output(int(data), GPIO.LOW) # Fa un DOWN del pin

    s.close() # Tanca la connexió
