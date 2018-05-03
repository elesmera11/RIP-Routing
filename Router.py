"""RIP ROUTING ASSIGNMENT - COSC364
Router.py - Main code for virtual routers.
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 27/04/2018 """

import select
import random
import socket
import os.path
import threading
import time
import sys
import ConfigParser
from Packet import Packet

#enumeration for the dictionary format (no spaces to ensure difference)
NEXTHOP = 0
METRIC = 1
RCF = 2
TIMEOUT = 3
GARBAGECOLL = 4
PORT = 0

#constants
HOST = "127.0.0.1"
INFINITY = 16
INVALID = 16
TIME_BLOCK = 15
PERIODIC_UPDATE = 30 / TIME_BLOCK
TIME_OUT = 180 / TIME_BLOCK
GARBAGE_COLLECTION = 120 / TIME_BLOCK

class Router:
    # Local variables
    lock = threading.RLock()
    router_id = 0       # Router ID of this router
    input_socks = []    # List of input sockets
    rt_tbl = {}         # Dict of format {dest: [next hop, metric, RCF, timeout, garbage collection]}
    neighbours = {}     # Dict of format {router ID: [port, metric]
    
    #***************************************************************************
    # Initialise the router
    # @param config_file the router configuration file
    #***************************************************************************
    def __init__(self, config_file):
        # Parse configurations
        config_list = ConfigParser.get_config(config_file)
        self.router_id = config_list[0] # Parse router ID
        
        # Parse and set input ports
        for port in config_list[1]: #line 2, input ports
            port = int(port)
            socket = self.create_socket(port)
            self.input_socks.append(socket)
        
        # Parse and set output ports
        for port, metric, router in config_list[2]: #line 3, output ports
            router = int(router)
            port = int(port)
            metric = int(metric)
            self.neighbours[router] = [port, metric]
    
    #***************************************************************************
    # Gets the metric of a neighbour
    # @param router_id the router id
    #***************************************************************************
    def get_neighbour_metric(self, router_id):
        return self.neighbours[router_id][METRIC]
    
    #***************************************************************************
    # Gets the port of a neighbour
    # @param router_id the router id
    #***************************************************************************
    def get_neighbour_port(self, router_id):
        return self.neighbours[router_id][PORT]
    
    #***************************************************************************
    # Creates socket for the port number
    # @param port the port number
    #***************************************************************************
    def create_socket(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind((HOST, port))
        print("Socket " + str(port) + " created")
        return sock
    
    #***************************************************************************
    # Sends the packet
    # @param packet the packet
    #***************************************************************************
    def send_packet(self, packet):
        encoded_packet = packet.encode()
        try:
            # Using first socket as default
            self.input_socks[0].sendto(encoded_packet, (HOST, self.neighbours[packet.dst][PORT])) 
        except Exception:
            print("Could not send packet to destination.")
            return
            
    #***************************************************************************
    # Triggers update
    # @param src the source router id that triggered the update
    #***************************************************************************        
    def trigger_update(self, src):
        changed = {}
        for dest in self.rt_tbl.keys():
            if self.rt_tbl[dest][RCF] == 1:
                changed[dest] = self.rt_tbl[dest]
                self.rt_tbl[dest][RCF] = 0
        if len(changed) > 0:
            delay = random.randint(1, 5)
            thread = threading.Timer(delay, self.init_trigger_update, 
                                     args = [changed, src])
            thread.daemon = True
            thread.start()
    
    #***************************************************************************
    # Function to send trigger update to the neighbours
    # @param changed a list of changed route(s)
    # @param src the source destination that calls the trigger update
    #***************************************************************************    
    def init_trigger_update(self, changed, src):
        for neighbour in self.neighbours:
            if neighbour != src:
                packet = Packet(self.router_id, neighbour, changed)
                self.send_packet(packet)
        return
        
    #***************************************************************************
    # Sends periodic update to neighbours
    #*************************************************************************** 
    def send_update(self):
        period = float(random.randint(8, 12) / 10)
        thread = threading.Timer(period * PERIODIC_UPDATE, self.send_update)
        self.print_routing_table()        
        thread.daemon = True
        thread.start()
        
        for neighbour in self.neighbours:
            packet = Packet(self.router_id, neighbour, self.rt_tbl)
            self.send_packet(packet)
    
    #***************************************************************************
    # Process incoming packet
    # @param data the packet
    #***************************************************************************
    def read_packet(self, data):
        in_packet = Packet(0, self.router_id, {}) # Initialise class as placeholder
        rte_table = in_packet.decode(data) # Decode the data
        packet_src = in_packet.src
        self.update_rt_tbl(packet_src, rte_table) # Update the routing table
        
    #***************************************************************************
    # Starts time out
    # @param packet_src the source router id
    #***************************************************************************
    def start_time_out(self, packet_src):
        for dest in self.rt_tbl.keys():
            if self.rt_tbl[dest][NEXTHOP] == packet_src or dest == packet_src:
                if (self.rt_tbl[dest][METRIC] < INFINITY):
                    self.rt_tbl[dest][TIMEOUT] = time.time()  
        self.init_time_out(packet_src)
    
    #***************************************************************************
    # Updates routing table according to RIP protocol
    # @param packet_src the source router id
    # @param rtes the routing entries received in a packet
    #***************************************************************************
    def update_rt_tbl(self, packet_src, rtes):
        self.lock.acquire() #locking mechanism for threads
        keys = self.rt_tbl.keys()
        neighbours = self.neighbours.keys()
        nxt_hop = packet_src
        nxt_hop_metric = self.get_neighbour_metric(nxt_hop)
        # add a new route
        if packet_src not in keys: 
            self.update_route(nxt_hop, nxt_hop, nxt_hop_metric, 0)
        for dest in rtes.keys():
            metric = rtes[dest][1]
            new_metric = min(nxt_hop_metric + metric, INFINITY)
            # Route does not exist
            if dest not in keys:
                if new_metric < INFINITY:
                    self.rt_tbl[dest] = [nxt_hop, new_metric, 0, 0, 0]
            # Route exist
            else:
                rt_nxt_hop = self.rt_tbl[dest][NEXTHOP]
                rt_metric = self.rt_tbl[dest][METRIC]   
                rt_garbage = self.rt_tbl[dest][GARBAGECOLL]
                # Valid route
                if rt_metric < INFINITY:
                    # Same next hop
                    if nxt_hop == rt_nxt_hop:
                        # Metric changed
                        if new_metric != rt_metric:
                            # Route becomes invalid
                            if rt_metric < INFINITY and new_metric >= INFINITY:
                                if self.rt_tbl[dest][GARBAGECOLL] == 0:
                                    self.rt_tbl[dest][METRIC] = new_metric
                                    self.rt_tbl[dest][RCF] = 1
                                    self.rt_tbl[dest][GARBAGECOLL] = time.time()
                                    self.init_gbg_coll(dest)
                            # Route metric changed
                            else:
                                self.update_route(dest, nxt_hop, new_metric, 0)
                    # Different next hop
                    else:
                        # New optimal path found
                        if new_metric < rt_metric:
                            self.update_route(dest, nxt_hop, new_metric, 0)
                # Invalid route
                else: 
                    # Another route found
                    if new_metric < INFINITY:
                        self.update_route(dest, nxt_hop, new_metric, 0)
                        
        self.start_time_out(packet_src)
        self.trigger_update(packet_src)
        self.lock.release()
    
    #***************************************************************************
    # Updates routing table entry
    # @param dest the destination id
    # @param nxt_hop the next hop id
    # @param new_metric the metric
    # @param rcf the route change flag
    #***************************************************************************    
    def update_route(self, dest, nxt_hop, new_metric, rcf):
        self.rt_tbl[dest] = [nxt_hop, new_metric, rcf, 0, 0]
    
    #***************************************************************************
    # Function to check time out of an entry
    # @param src the source router id
    #***************************************************************************        
    def check_time_out(self, src):
        self.lock.acquire()
        for dest in self.rt_tbl.keys():
            if dest == src or self.rt_tbl[dest][NEXTHOP] == src:
                # Route is invalid
                if time.time() - self.rt_tbl[dest][TIMEOUT] > TIME_OUT:
                    self.rt_tbl[dest][METRIC] = INFINITY
                    self.rt_tbl[dest][RCF] = 1
                    if self.rt_tbl[dest][GARBAGECOLL] == 0:
                        self.rt_tbl[dest][GARBAGECOLL] = time.time()
                        self.init_gbg_coll(dest)
        self.trigger_update(src)
        self.lock.release()
        return
    
    #***************************************************************************
    # Function to check garbage collection of an entry
    # @param dest the destination id
    #***************************************************************************
    def check_gbg_coll(self, dest):
        self.lock.acquire()
        if self.rt_tbl[dest][4] != 0:
            # Route removed
            if (time.time() - self.rt_tbl[dest][GARBAGECOLL]) > GARBAGE_COLLECTION:
                del self.rt_tbl[dest]
        self.lock.release()
        return
    
    #***************************************************************************
    # Function to start thread to check time out
    # @param src the source id
    #***************************************************************************    
    def init_time_out(self, src):
        thread = threading.Timer(TIME_OUT, self.check_time_out, args = [src])
        thread.daemon = True
        thread.start()
    
    #***************************************************************************
    # Function to start thread to check garbage collection
    # @param dest the destination id
    #***************************************************************************    
    def init_gbg_coll(self, dest):
        thread = threading.Timer(GARBAGE_COLLECTION, 
                                 self.check_gbg_coll, 
                                 args = [dest])
        thread.daemon = True
        thread.start()       
    
    #***************************************************************************
    # Prints routing table in format:
    # Destination, Next Hop, Metric, Time-out, Garbage Collection
    #***************************************************************************    
    def print_routing_table(self):
        template = "{0:^15d} | {1:^12d} | {2:^10d} | {3:^12.2f} | {4:^20.2f}"
        print("Router {0}".format(self.router_id))
        print("{0:^15s} | {1:^12s} | {2:^10s} | {3:^12s} | {4:^20s}".format(
            "Destination", "Next Hop", "Metric", "Time Out", 
            "Garbage Collection").rstrip())
        for dest in self.rt_tbl.keys():
            if self.rt_tbl[dest][GARBAGECOLL] == 0:
                print(template.format(dest, self.rt_tbl[dest][NEXTHOP], 
                                      self.rt_tbl[dest][METRIC], 
                                      time.time() - self.rt_tbl[dest][TIMEOUT],
                                      0).rstrip())
            else:
                print(template.format(dest, self.rt_tbl[dest][NEXTHOP], 
                                      self.rt_tbl[dest][METRIC], 
                                      time.time() - self.rt_tbl[dest][TIMEOUT], 
                                      time.time() - self.rt_tbl[dest][GARBAGECOLL])
                      .rstrip())
    
    #***************************************************************************
    # Runs the router
    #***************************************************************************    
    def run(self):
        self.send_update()
        while True:
            read_ready, write_ready, except_ready = select.select(self.input_socks, [], [])
            for sock in read_ready:
                data, src = sock.recvfrom(512)
                self.read_packet(data)

#***************************************************************************
# Main function to start the router
#***************************************************************************           
def main():
                
    if __name__ == "__main__":
        try:
            if len(sys.argv) < 2:
                print("No file given")
                sys.exit(0)
            
            filename = str(sys.argv[-1])
            if os.path.exists(filename):
                router = Router(filename)
                router.run()
            else:
                print("File does not exist")
                sys.exit(0)
            
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)         

main()
    
