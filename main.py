#Hani9 ID: 8303639
# -*- coding: utf-8 -*-

#Importo les llibreries que necessito
import sys
import time
import datetime
import pprint
import select
import os
from conn import *
from sock import *
import telepot

#Passo el token del bot a la llibreria
bot = telepot.Bot(token)
now = datetime.datetime.now()

#Inicio una funció
def handle(msg):
    #Fa un print dels JSON
    pprint.pprint(msg)

    #Analitza el missatge i guarda el seu flavor en una variable
    flavor = telepot.flavor(msg)

    #Si el flavor és un xat, executa la funció glance(), que genera una tupla i emmagatzema en variables.
    if flavor == "chat":
        content_type, chat_type, chat_id = telepot.glance(msg)

        #Comprova que el tipus de contingut sigui text.
        if content_type == "text":
            content_type, chat_type, chat_id = telepot.glance(msg)
            text = msg['text']
            #print text


            # Si el tipus de contingut és text, faig un try per comprovar si és una comanda i que no peti.
            try:
                check_command = msg['entities'][0]['type']
                comanda = text

                # Comprovo si el text que s'envia és una comanda.
                if check_command == "bot_command":


                    # Nota prèvia a les altes.
                    if comanda == "/alta" or comanda == "/alta@SmartlockersBot":
                        bot.sendMessage(chat_id,
                                        "Per tal de realitzar altes el teu nom i cognom de Telegram han de ser els reals. Un cop siguin correctes, envia'm el teu número de taquilla de la forma /num")

                    # Comprovo si la comanda porta el nom del bot o no. El try és perquè no peti.
                    if text[-6:] == CodiAcces:
                        #print text
                        try:
                            if comanda.endswith("@SmartlockersBot"):

                                # Primer provo si el número és de 3 dígits.
                                try:
                                    comanda = comanda[:-15]
                                    print comanda
                                    num = int(comanda[1:3])
                                # Si és de dos dígits o 1 executarà aquest codi.
                                except:
                                    comanda = comanda[:-16]
                            num = int(comanda[1:2])
                            print num # Debug
                            print text

                            # Les altes només estan permeses durant els mesos que s'especifiquen aquí.
                            if now.month == 12:
                                # Si es vol fer una alta fora d'aquests mesos el bot t'avisa que no és possible.
                                bot.sendMessage(chat_id,
                                            "Les altes no estan disponibles en aquests moments. Si creus que es tracta d'un error, contacta amb un administrador.")

                            # Si ens trobem dins d'un dels mesos especificats s'executa el següent codi.
                            else:
                                print num # Debug
                                print text

                                # Comprova que l'usuari tingui nom i cognom.
                                try:
                                    nom = msg['from']['first_name'] + " " + msg['from']['last_name']

                                # Si només té nom avisa que és necessari posar un cognom.
                                except:
                                    bot.sendMessage(chat_id, "És necessari que indiquis el cognom a la configuració de Telegram.")

                                print nom # Debug
                                # Actualització de la base de dades. Allà on l'ID és l'especificat actualitza el chat_id i el nom.
                                cmd = "UPDATE proves SET chat_id = %s, nom=%s WHERE id = %s"
                                cur.execute(cmd,(chat_id, nom, num))

                                # Fa efectives les modificacions de la DB.
                                db.commit()

                                # Envia un missatge dient que l'alta s'ha fet efectiva.
                                bot.sendMessage(chat_id, "El teu usuari s'ha associat amb la taquilla " + str(
                                    num) + ", moltes gràcies.")
                                # cur.close()
                                ##### Funció altes #####

                        except:
                            pass

                    else:
                        bot.sendMessage(chat_id, "El codi especificat no és correcte.")


                # Si el missatge comença amb /obre s'executarà aquest codi.
                if text.startswith("/obre"):

                    # Inicio un bucle infinit (running = 1 segons variables globals).
                    while running:

                        # Aquestes línies són per permetre que el socket gestioni múltiples clients.
                        inputready, outputready, exceptready = select.select(entrada, [], [])

                        for s in inputready:

                            if s == server:
                                # Poso el socket i la IP del client en una tupla.
                                client, address = server.accept()
                                # Transformo el socket a str per poder-lo tractar.
                                clientStr = str(client)
                                # El mateix però amb l'IP
                                addressStr = str(address[0])
                                # Línies de debug
                                print client
                                print address
                                print clientStr
                                print addressStr

                                # S'actualitza la columna socket de la base de dades en funció de la IP.
                                cmd2 = "UPDATE proves SET socket = %s WHERE ip = %s"
                                cur.execute(cmd2,(clientStr, addressStr))

                                # S'efectuen els canvis.
                                db.commit()
                                #cur.close()
                                # Afegeixo el socket a una llista.
                                sockets.append(client)

                        # txt = raw_input("Entrada: ")
                        # if txt == "obre" or txt == "tanca":

                        # Faig una consulta a la base de dades per obtenir tots els chat_id.
                        cur.execute("""SELECT chat_id FROM proves""")
                        consultaXatId = cur.fetchall()

                        # Com que el fetchall retorna una tupla comprova la seva longitud i l'assigno a la variable i.
                        i = len(consultaXatId)
                        print i # Debug

                        # Inicio un bucle que es manté mentre quedin elements per comprovar a la llista.
                        while i > 0:

                            # Cada element de la tupla es converteix en str per poder-se analitzar.
                            chat_db = int(''.join(map(str, consultaXatId[i - 1])))
                            print chat_db # Debug

                            # Va comprovant els ids de la DB amb el del que ha enviat el missatge.
                            if chat_db == chat_id:
                                # Selecciono el socket guardat a la DB.
                                cur.execute("""SELECT socket FROM proves WHERE chat_id = %s""", chat_id)
                                consultaSocket = cur.fetchone()
                                c = ''.join(consultaSocket)
                                # Selecciono el número del GPIO i el passo a str ja que el socket només permet passar strings.
                                cur.execute("""SELECT gpio FROM proves WHERE chat_id = %s""", chat_id)
                                consultaGpio = cur.fetchone()
                                gpio = int(''.join(map(str, consultaGpio)))
                                # print gpio

                                ''' Com que el que li passes a la comanda send ha de ser un socket, necessito comprovar
                                el que tinc amb str amb els que hi ha a la llista prèviament creada'''
                                for s in sockets:

                                    # En el moment que coincideixen s'envia el gpio en forma de cadena i es tanca la connexió.
                                    if c == str(s):
                                        # print c
                                        # print s


                                        s.send(str(gpio)) # Al codi del client es passa a int.
                                        print gpio # Debug
                                        s.close()

                            # Aquest codi és el que permet als establiments obrir qualsevol taquilla.
                            elif chat_id == chat_id_admin:
                                # Com que l'estructura de la comanda és /obre num agafo els dígits a partir del 6.
                                num = int(text[6:])
                                # Com en el codi anterior, selecciono el socket i el gpio per enviar-ho a la pi zero.
                                cur.execute("""SELECT socket FROM proves WHERE id = %s""", num)
                                consultaSocket = cur.fetchone()
                                c = ''.join(consultaSocket)
                                cur.execute("""SELECT gpio FROM proves WHERE id = %s""", num)
                                consultaGpio = cur.fetchone()
                                gpio = int(''.join(map(str, consultaGpio)))
                                # print gpio

                                # Igual que abans, es comprova el socket a la llista.
                                for s in sockets:
                                    if c == str(s):
                                        # print c
                                        # print s


                                        s.send(str(gpio))
                                        print gpio
                                        s.close()
                                break # Tanco el bucle

                            i -= 1 # Si el que fa la petició no és l'admin es va restant i per no tenir un ifinite loop.

                        break # Tanco el bucle infinit.

                            ###################################################################################################



            except:
                pass



# Línies per tenir el bot en funcionament.
bot.message_loop(handle)
while 1:
    time.sleep(10)
