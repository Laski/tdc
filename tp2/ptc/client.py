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


import threading
import random

from common import PacketBuilder, ProtocolControlBlock
from soquete import Soquete
from packet import ACKFlag, FINFlag, SYNFlag
from worker import ClientProtocolWorker
from buffers import DataBuffer, RetransmissionQueue, NotEnoughDataException
from constants import MIN_PACKET_SIZE, MAX_PACKET_SIZE, CLOSED,\
                      ESTABLISHED, FIN_SENT, SYN_SENT, MAX_SEQ,\
                      SEND_WINDOW, MAX_RETRANSMISSION_ATTEMPTS


class ClientControlBlock(ProtocolControlBlock):
    
    def __init__(self, address, port):
        ProtocolControlBlock.__init__(self, address, port)
        # Próximo SEQ a enviar
        self.send_seq = random.randint(1, MAX_SEQ)
        # Tamaño de la ventana de emisión
        self.send_window = SEND_WINDOW
        # Límite inferior de la ventana (i.e., unacknowledged)
        self.window_lo = self.send_seq
        # Límite superior de la ventana
        self.window_hi = self.modular_sum(self.window_lo, self.send_window)
        
    def get_send_seq(self):
        return self.send_seq
    
    def get_send_window(self):
        return self.send_window
    
    def accept_control_ack(self, packet):
        return ACKFlag in packet and packet.get_ack_number() == self.get_send_seq()
        
    def accept_ack(self, packet):
        if ACKFlag in packet: # asumimos que el numero de ack corresponde a un paquete enviado
            self.window_lo = packet.get_ack_number() + 1
            self.window_hi = self.modular_sum(self.window_lo, self.send_window)
            return True
        else:
            return False

    def increment_send_seq(self):
        self.send_seq += 1
        if self.send_seq >= MAX_SEQ:
            send_seq = 1
            
    def modular_sum(self, window_lo, send_window):
        res = window_lo + send_window
        while res >= MAX_SEQ:
            res -= MAX_SEQ
            res += 1 # evitamos el 0
        return res
    
    # Responde True sii la ventana de emisión no está saturada.
    def send_allowed(self):
        return self.send_seq < self.window_hi        

class PTCClientProtocol(object):
    
    def __init__(self, address, port):
        self.retransmission_queue = RetransmissionQueue(self)
        self.retransmission_attempts = dict()
        self.outgoing_buffer = DataBuffer()
        self.state = CLOSED
        self.control_block = ClientControlBlock(address, port)
        self.socket = Soquete(address, port)
        self.packet_builder = PacketBuilder(self)
    
    def is_connected(self):
        return self.state == ESTABLISHED
        
    def build_packet(self, payload=None, flags=None):
        seq = self.control_block.get_send_seq()
        if payload is not None:
            self.control_block.increment_send_seq()
        packet = self.packet_builder.build(payload=payload, flags=flags, seq=seq)
        return packet
        
    def send_packet(self, packet):
        self.socket.send(packet)
        
    def send_and_queue_packet(self, packet):
        self.send_packet(packet)
        self.retransmission_queue.put(packet)
        
    def send(self, data):
        if not self.is_connected():
            raise Exception('cannot send data: connection not established')
        self.worker.send(data)

    def connect_to(self, address, port):
        self.worker = ClientProtocolWorker.spawn_for(self)
        self.worker.start()
        self.connected_event = threading.Event()
        self.control_block.set_destination_address(address)
        self.control_block.set_destination_port(port)
        
        syn_packet = self.build_packet(flags=[SYNFlag])
        self.send_and_queue_packet(syn_packet)
        self.state = SYN_SENT
        
        self.connected_event.wait()
    
    def handle_timeout(self):
        for packet in self.retransmission_queue:
            if packet not in self.retransmission_attempts:
                self.retransmission_attempts[packet] = 0
            self.retransmission_attempts[packet] += 1
            if self.retransmission_attempts[packet] >= MAX_RETRANSMISSION_ATTEMPTS:
                self.shutdown()
                self.error =  "Intentos de retransmisión superó el máximo"
                break
            else:
                self.send_packet(packet)
        
        ###################
        ##   Completar!  ##
        ###################
        
        # Tener en cuenta que se debe:
        # (1) Obtener los paquetes en self.retranmission_queue
        # (2) Volver a enviarlos
        # (3) Reencolarlos para otra eventual retransmisión
        # ...y verificar que no se exceda la cantidad máxima de reenvíos!
        # (hacer self.shutdown() si esto ocurre y dejar un mensaje en self.error)
        
    
    def handle_pending_data(self):
        more_data_pending = False
        
        if self.control_block.send_allowed():
            try:
                data = self.outgoing_buffer.get(MIN_PACKET_SIZE, MAX_PACKET_SIZE)
            except NotEnoughDataException:
                pass
            else:
                packet = self.build_packet(payload=data)
                self.send_and_queue_packet(packet)
                
            if not self.outgoing_buffer.empty():
                more_data_pending = True
        else:
            more_data_pending = True
        
        if more_data_pending:
            self.worker.signal_pending_data()
    
    def handle_incoming(self, packet):
        if self.state == ESTABLISHED and self.control_block.accept_ack(packet):
            self.retransmission_queue.acknowledge(packet)
            self.clear_retransmission_attempts(packet.get_ack_number())
        elif self.state == SYN_SENT and self.control_block.accept_control_ack(packet):
            self.state = ESTABLISHED
            self.connected_event.set()
        elif self.state == FIN_SENT and self.control_block.accept_control_ack(packet):
                self.state = CLOSED
                        
        # Tener en cuenta que se debe:
        # * Corroborar que el flag de ACK esté seteado
            # Se encarga el control_block
        # * Distinguir el caso donde el estado es SYN_SENT
            # Dale
        #   * No olvidar de hacer self.connected_event.set() al confirmar el ACK y establecer la conexión!!!
            # A full
        # * Analizar si #ACK es aceptado (hablar con el bloque de control para hacer este checkeo)
            # Sí
        # * Sacar de la cola de retransmisión los paquetes reconocidos por #ACK
            # Lo hace la cola
        # * Ajustar la ventana deslizante con #ACK
            # Lo hace el control_block
        # * Tener en cuenta también el caso donde el estado es FIN_SENT
            # Ok
            
    def clear_retransmission_attempts(self, ack):
        for packet in self.retransmission_attempts.keys():
            if packet.get_seq_number() <= ack:
                del self.retransmission_attempts[packet]
            
    def handle_close_connection(self):
        if not self.outgoing_buffer.empty():
            self.worker.signal_pending_data()
            self.worker.signal_close_connection()
        elif not self.retransmission_queue.empty():
            self.worker.signal_close_connection()
        else:
            fin_packet = self.build_packet(flags=[FINFlag])
            self.send_and_queue_packet(fin_packet)
            self.state = FIN_SENT
        
    def close(self):
        if self.is_connected():
            self.worker.signal_close_connection()
        
    def shutdown(self):
        self.outgoing_buffer.clear()
        self.retransmission_queue.clear()
        self.retransmission_attempts.clear()
        self.worker.stop()
        # Esto es por si falló el establecimiento de conexión (para destrabar al thread principal)
        self.connected_event.set()
        self.state = CLOSED