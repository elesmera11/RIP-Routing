"""RIP ROUTING ASSIGNMENT - COSC364
Router.py - Main code for virtual routers.
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 03/03/2018 """

import select
import socket
import threading
import time
import sys
import ConfigParser
from Packet import Packet

HOST = "127.0.0.1"
INFINITY = 16
INVALID = 16
TIME_BLOCK = 15
PERIODIC_UPDATE = 30 / TIME_BLOCK
TIME_OUT = 180 / TIME_BLOCK
GARBAGE_COLLECTION = 120 / TIME_BLOCK

class Router:
    # Local variables
    current_time = 0
    router_id = 0       # Router ID of this router
    input_socks = []    # List of input sockets
    rt_tbl = {}         # Dict of format {dest: [next hop, metric, RCF, timeout, garbage collection]}
    neighbours = {}     # Dict of format {router ID: [port, metric]
    
    # Initialisation
    def __init__(self, config_file):
        # Parse configurations
        config_list = ConfigParser.get_config(config_file)
        self.router_id = config_list[0] # Parse router ID
        
        # Parse and set input ports
        for port in config_list[1]:
            port = int(port)
            socket = self.create_socket(port)
            self.input_socks.append(socket)
        
        # Parse and set output ports
        for port, metric, router in config_list[2]:
            router = int(router)
            port = int(port)
            metric = int(metric)
            self.neighbours[router] = [port, metric]
    
    # Get neighbour's metric
    def get_neighbour_metric(self, router_id):
        return self.neighbours[router_id][1]
    
    # Get neighbour's port
    def get_neighbour_port(self, router_id):
        return self.neighbours[router_id][0]
    
    # Creates sockets
    def create_socket(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind((HOST, port))
        print("Socket " + str(port) + " created")
        return sock
    
    # Sends packet
    def send_packet(self, packet):
        encoded_packet = packet.encode()
        try:
            self.input_socks[0].sendto(encoded_packet, (HOST, self.neighbours[packet.dst][0])) # Using first socket as default
        except Exception:
            print("Could not send packet to destination.")
#TODO
    # Triggers update    
    def trigger_update(self):
        changed = {}
        for dst in self.rt_tbl.keys():
            if self.rt_tbl[dst][2] == 1:
                changed[dst] = self.rt_tbl[dst]
                self.rt_tbl[dst][2] = 0
        if len(changed) > 0:
            for neighbour in self.neighbours:
                packet = Packet(self.router_id, neighbour, self.rt_tbl)
                self.send_packet(packet)
    
    # Sends periodic update 
    def send_update(self):
        thread = threading.Timer(PERIODIC_UPDATE, self.send_update)
        thread.daemon = True
        thread.start()
        
        for neighbour in self.neighbours:
            print("Sending update to router " + str(neighbour))
            packet = Packet(self.router_id, neighbour, self.rt_tbl)
            self.send_packet(packet)
    
    # Processes incoming packet
    def read_packet(self, data):
        in_packet = Packet(0, self.router_id, {}) # Initialise class as placeholder
        rte_table = in_packet.decode(data) # Decode the data
        packet_src = in_packet.src
        print("Processing packet from router " + str(packet_src))
        print("RTE table from " + str(packet_src) + " :")
        print(rte_table)
        self.update_rt_tbl(packet_src, rte_table) # Update the routing table
        
    #def check_neighbours(self, decoded_packet):
        #if decoded_packet.src in self.neighbours.keys():
            #self.rt_tbl[decoded_packet.src] = [decoded_packet.src, 
                                               #self.get_neighbour_metric(decoded_packet.src),
                                               #0, 
                                               #time.time(), 
                                               #0]
            #print(self.rt_tbl)
            #self.init_time_out()
            #return decoded_packet.src
    
    def start_time_out(self, packet_src):
        for dst in self.rt_tbl.keys():
            if self.rt_tbl[dst][0] == packet_src or dst == packet_src:
                self.rt_tbl[dst][3] = time.time()  
    
    # Updates the routing table
    def update_rt_tbl(self, packet_src, rtes):
        keys = self.rt_tbl.keys()
        neighbours = self.neighbours.keys()
        nxt_hop = packet_src
        nxt_hop_metric = self.get_neighbour_metric(nxt_hop)
        if packet_src != keys:
            self.update_route(nxt_hop, nxt_hop, nxt_hop_metric, 0)
        for dst in rtes.keys():
            metric = rtes[dst][1]
            new_metric = min(nxt_hop_metric + metric, INFINITY)
            # Route does not exist
            if dst not in keys:
                if new_metric < INFINITY:
                    self.rt_tbl[dst] = [nxt_hop, new_metric, 0, 0, 0]
                    print("Entry added for route " + str(dst))
            # Route exist
            else:
                rt_nxt_hop = self.rt_tbl[dst][0]
                rt_metric = self.rt_tbl[dst][1]   
                rt_garbage = self.rt_tbl[dst][4] 
                if rt_metric < INFINITY:
                    if nxt_hop == rt_nxt_hop:
                        if new_metric != rt_metric:
                            if rt_metric < INFINITY and new_metric >= INFINITY:
                                self.update_route(dst, nxt_hop, new_metric, 1)
                                if self.rt_tbl[dst][4] == 0:
                                    self.rt_tbl[dst][4] = time.time()
                                    self.init_gbg_coll(dst)
                            else:
                                self.update_route(dst, nxt_hop, new_metric, 0)
                    else:
                        if new_metric < rt_metric:
                            self.update_route(dst, nxt_hop, new_metric, 0)
                else: 
                    if new_metric < INFINITY:
                        self.update_route(dst, nxt_hop, new_metric, 0)
                        
        self.trigger_update()
        self.start_time_out(packet_src)
        self.init_time_out()
        self.print_routing_table()
    
    def update_route(self, dst, nxt_hop, new_metric, rcf):
        self.rt_tbl[dst] = [nxt_hop, new_metric, rcf, 0, 0]
    
        
    def check_time_out(self):
        for dst in self.rt_tbl.keys():
            if time.time() - self.rt_tbl[dst][3] > TIME_OUT:
                self.rt_tbl[dst][1] = INFINITY
                self.rt_tbl[dst][2] = 1
                self.trigger_update()
                if self.rt_tbl[dst][4] == 0:
                    self.rt_tbl[dst][4] = time.time()
                    self.init_gbg_coll(dst)
        return
    
    def check_gbg_coll(self, dst):
        if time.time() - self.rt_tbl[dst][4] > GARBAGE_COLLECTION:
            del self.rt_tbl[dst]
        return
    
    def init_time_out(self):
        thread = threading.Timer(GARBAGE_COLLECTION, self.check_time_out)
        thread.daemon = True
        thread.start()
    
    def init_gbg_coll(self, dst):
        thread = threading.Timer(TIME_OUT, self.check_gbg_coll, args = [dst])
        thread.daemon = True
        thread.start()       
    
    def print_routing_table(self):
        print("Thread count is :")
        print(threading.activeCount())
        template = "{0:^15d} | {1:^12d} | {2:^10d} | {3:^12.2f} | {4:^20.2f}"
        print("{0:^15s} | {1:^12s} | {2:^10s} | {3:^12s} | {4:^20s}".format("Destination", "Next Hop", "Metric", "Time Out", "Garbage Collection"))
        for dst in self.rt_tbl.keys():
            if self.rt_tbl[dst][4] == 0:
                print(template.format(dst, self.rt_tbl[dst][0], self.rt_tbl[dst][1], time.time() - self.rt_tbl[dst][3], 0))
            else:
                print(template.format(dst, self.rt_tbl[dst][0], self.rt_tbl[dst][1], time.time() - self.rt_tbl[dst][3], time.time() - self.rt_tbl[dst][4]))
    
    def run(self):
        print("Router is running")
        self.send_update()
        while True:
            read_ready, write_ready, except_ready = select.select(self.input_socks, [], [])
            for sock in read_ready:
                data, src = sock.recvfrom(512)
                self.read_packet(data)
                
def main():
                
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            sys.exit("No file given")
     
        router = Router(str(sys.argv[-1]))
        router.run()
        
        if sys.exit():
            for sock in self.input_socks:
                sock.close()
                print("Socket " + str(sock.getsockname() + " is now closed"))

main()
		
  
    
################################################################################
    # test
################################################################################
    