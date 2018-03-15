"""RIP ROUTING ASSIGNMENT - COSC364
Router.py - Main code for virtual routers.
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 03/03/2018 """

import select
import socket
import threading
import time
import ConfigParser
from Packet import Packet

HOST = "127.0.0.1"
INFINITY = 16
INVALID = 16
TIME_BLOCK = 30
PERIODIC_UPDATE = 30 / TIME_BLOCK
TIME_OUT = 180 / TIME_BLOCK
GARBAGE_COLLECTION = 120 / TIME_BLOCK

class Router:
    # Local variables
    router_id = 0       # Router ID of this router
    input_socks = []    # List of input sockets
    output_socks = []   # List of output sockets
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
            socket = self.create_socket(port)
            self.output_socks.append(socket)
        return
    
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
        return socket
    
    # Sends packet
    def send_packet(self, packet):
        encoded_packet = packet.encode()
        try:
            self.input_socks[0].sendto(encoded_packet, (HOST, packet.dst)) # Using first socket as default
        except Exception:
            print("Could not send packet to destination.")
#TODO
    ## Triggers update    
    #def trigger_update():
        #return
    
    ## Sends periodic update 
    #def send_update():
        #return
    
    ## Processes incoming packet
    #def read_packet(data):
        #in_packet = Packet(0, self.router_id, {}) # Initialise class as placeholder
        #rte_table = in_packet.decode(data) # Decode the data
        #print("Processing packet")
        #update_rt_tbl(rte_table) # Update the routing table
    
    ## Updates the routing table
    #def update_rt_tbl(self, rtes):
        #keys = rt_tbl.keys()
        #rt_nxt_hop = rt_tbl[dst][0]
        #rt_metric = rt_tbl[dst][1]
        ##rt_rcf = rt_tbl[dst][2]
        ##rt_time_out = rt_tbl[dst][3]
        ##rt_gbg_coll = rt_tbl[dst][4]
        #for dst in rtes.keys():
            #nxt_hop = rtes[dst][0]
            #metric = rtes[dst][1]
            #new_metric = min(get_neighbour_metric(nxt_hop) + metric, INFINITY)
            #if dst not in keys:
                #if new_metric < 16:
                    #rt_tbl[dst] = nxt_hop, new_metric, 0, init_time_out(), 0
            #else:        
                #if rt_metric < 16:
                    #if rt_time_out > TIME_OUT:
                        #rt_metric = 16
                        #rt_rfc = 1
                        #rt_gbg_coll = time.time()
                        #init_gbg_coll()
                        #trigger_update()
                    #elif nxt_hop == rt_nxt_hop and new_metric < 16:
                        #if new_metric == rt_metric:
                            #rt_time_out = time.time()
                            #init_time_out()
                        #else:
                            #rt_metric = new_metric
                    #elif nxt_hop == rt_nxt_hop and new_metric == 16:
                        #rt_metric = new_metric
                        #rt_rfc = 1
                        #rt_time_out = time.time()
                        #init_time_out()
                        #rt_gbg_coll = time.time()
                        #init_gbg_coll()
                        #trigger_update()
                    #elif nxt_hop != rt_nxt_hop and new_metric < rt_metric:
                        #rt_nxt_hop = nxt_hop
                        #rt_metric = new_metric
                        #rt_time_out = time.time()
                        #init_time_out()
                #else:
                    #if new_metric < 16:
                        #rt_nxt_hop = nxt_hop
                        #rt_metric = new_metric
                        #rt_time_out = time.time()
                        #init_time_out()
                        #rt_gbg_coll = 0
        #print_routing_table()
    
    #def check_time_out(self, dst):
        #if time.time() - rt_tbl[dst][3] > TIME_OUT:
            #rt_tbl[dst][1] = INVALID
            #init_gbg_coll(self,dst)
    
    #def check_gbg_coll(self, dst):
        #if time.time() - rt_tbl[dst][4] > GARBAGE_COLLECTION:
            #del rt_tbl[dst]
    
    #def init_time_out(self,dst):
        #thread = threading.timer(GARBAGE_COLLECTION, check_time_out(dst))
        #thread.start()
    
    #def init_gbg_coll(self,dst):
        #thread = threading.timer(TIME_OUT, check_gbg_coll(dst))
        #thread.start()       
    
    #def print_routing_table():
        #template = "{0:^15d} | {1:^12d} | {2:^10d} | {3:^12.2f} | {4:^20.2f}"
        #print("{0:^15s} | {1:^12s} | {2:^10s} | {3:^12s} | {4:^20s}".format("Destination", "Next Hop", "Metric", "Time Out", "Garbage Collection"))
        #for dst in rt_tbl.keys():
            #print(template.format(dst, rt_tbl[0], rt_tbl[1], rt_tbl[3], rt_tbl[4]))
    
    #def run(self):
        #while True:
        #read_ready, send_ready, except_ready = select.select(self.input_socks, [], [])
        #if read_ready
        
        
################################################################################
    # test
################################################################################
    
y = Router('config_1.ini')
print("Router ID: " + str(y.router_id))
print("Neighbour 2 metric: " + str(y.get_neighbour_metric(2)))
print("Neighbour 2 port: " + str(y.get_neighbour_port(2)))

rting_table = {2: [2, 5, 0, 0, 0], 3: [2, 7, 0, 0, 0], 4: [6, 2, 0, 0, 0]}
x = Packet(1, 2, rting_table)
y.send_packet(x)