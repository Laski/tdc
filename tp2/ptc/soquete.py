# -*- coding: utf-8 -*- 
# # # # # # # # # # # # # # # # # # # # #
#                                       #                                       
#    Trabajo Práctico 3 - Conexiones    # 
#                                       #
#     Teoría de las Comunicaciones      #
#      Departamento de Computación      #
#              FCEN - UBA               #
#           octubre de 2013             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #


import socket

from packet_parser import PacketParser
from constants import PROTOCOL_NUMBER


class Soquete(object):
    
    MAX_SIZE = 65535
    
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, PROTOCOL_NUMBER)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.port = port
        self.address = address
        self.bind()
        
    def close(self):
        self.socket.close()  
        
    def bind(self):
        self.socket.bind((self.address, self.port))
        
    def send(self, packet):
        data = packet.get_bytes()
        dst_address = packet.get_destination_ip()
        dst_port = packet.get_destination_port()
        self.socket.sendto(data, (dst_address, dst_port))
        
    def receive(self, timeout = None):
        should_stop = False
        if timeout is not None and timeout > 0:
            self.socket.settimeout(timeout)
        else:
            self.socket.settimeout(None)
        while not should_stop:
            packet_bytes, _ = self.socket.recvfrom(self.MAX_SIZE)
            packet = PacketParser().parse_from(packet_bytes)
            if self.is_for_me(packet):
                should_stop = True
        return packet
                
    def is_for_me(self, packet):
        address = packet.get_destination_ip()
        port = packet.get_destination_port()
        return address == self.address and port == self.port