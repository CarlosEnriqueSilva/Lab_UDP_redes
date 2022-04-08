# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:37:08 2022

@author: Seccion 2 Grupo 1
"""
import socket
import os

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input('Ingresar direccion ip --> ')
        self.target_port = input('Ingresar puerto --> ')
        self.buffer_size=int(input('Ingrese el tamaño del buffer (max 64KB) --> '))

        #self.s.connect((self.target_ip,int(self.target_port)))

        self.main()

    def reconnect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.s.connect((self.target_ip,int(self.target_port)))
        print('Reconecto con el servidor')

    def main(self):
        while 1:
            #file_name = input('Enter file name on server --> ')
            #self.s.send(file_name.encode())
            address=(self.target_ip,int(self.target_port))
            self.s.sendto('Conectando'.encode(), address)
            #confirmation = self.s.recv(self.buffer_size)
            confirmation = self.s.recvfrom(self.buffer_size)[0].decode()
            if confirmation == "El Archivo no existe":
                print("Error de envío de archivo desde el servidor.")

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

            else:
                #file_name = self.s.recv(self.buffer_size).decode()
                file_name = self.s.recvfrom(self.buffer_size)[0].decode()
                
                if not file_name.endswith('.txt'):
                    #self.s.send('Error Al recibir el nombre'.encode())
                    self.s.sendto('Error Al recibir el nombre'.encode(), address)
                    
                else:
                    #self.s.send('Nombre recibido correctamente'.encode())
                    self.s.sendto('Nombre recibido correctamente'.encode(), address)
                    write_name = 'ArchivosRecibidos/' + file_name
                    if os.path.exists(write_name): os.remove(write_name)
    
                    with open(write_name,'wb') as file:
                        while 1:
                            #data = self.s.recv(self.buffer_size)
                            data = self.s.recvfrom(self.buffer_size)[0]
                            #if not data:
                             #   break
                            
                            if data.decode() == 'EOF' or not data:
                                print(file_name,'Descargado exitosamente. \n')
                                #self.s.send('OK'.encode())
                                self.s.sendto('OK'.encode(), address)
                                break
                            
                            if data.decode().endswith('EOF') or 'EOF' in data.decode():
                                w = data.decode()
                                w = w.replace('EOF','')
                                w = w.encode()
                                file.write(w)
                                print(file_name,'Descargado exitosamente. \n')
                                self.s.sendto('OK'.encode(), address)
                                break
    
                            file.write(data)
                    #hashVal = self.s.recv(self.buffer_size).decode()
                    hashVal = self.s.recvfrom(self.buffer_size).decode()
                    print('Valor hash del archivo:', hashVal)
                    print(file_name,'successfully downloaded.')

                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()
                
client = Client()