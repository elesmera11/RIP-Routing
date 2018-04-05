"""RIP ROUTING ASSIGNMENT - COSC364
Packet.py - Class code for the packet objects. Implements 
split horizon with poisoned reverse.
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 15/03/2018 """

import socket
import struct

TAG = 0                 # Since there is no IGP/BGP routing, always 0
COMMAND = 2             # No request packets so always 2
VERSION = 2             # RIPv2 
AFI = socket.AF_INET    # Address Family for IPv4
INFINITY = 16           # Infinity metric

# set format and calculate sizes, see
# https://docs.python.org/2/library/struct.html#format-characters
HEADER_FORMAT = "!BBH"  
RTE_FORMAT = "!HHIII" 
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
RTE_SIZE = struct.calcsize(RTE_FORMAT)

class Packet:
    src = 0
    dst = 0
    rtes = {}
    
    def __init__(self, src, dst, routing_table):
        self.src = src
        self.dst = dst
        self.rtes = routing_table
    
    
    #***************************************************************************
    # Function to encode the packet into a binary string
    # @return the encoded packet
    #***************************************************************************       
    def encode(self):
        metric = 0
        
        # Pack the header into a binary format given by RFC 
        encoded_packet = struct.pack(HEADER_FORMAT, COMMAND, VERSION, self.src)
        
        for key in self.rtes.keys():
            if (key != self.dst): # Doesn't send its own route
                nxt_hop = self.rtes[key][0]
                
                # Implement split horizon with poisoned reverse
                if (self.dst == nxt_hop): 
                    metric = INFINITY     
                else:
                    metric = self.rtes[key][1]
                
                # Pack each RTE and add it to the binary packet
                encoded_packet += struct.pack(RTE_FORMAT, AFI, TAG, 
                                              key, nxt_hop, metric)
        return(encoded_packet)
    
    #***************************************************************************
    # Function to decode the packet from binary string. 
    # @param filename the filename of the config text file
    # @return the decoded RTEs in format: {dest: [next hop, metric]}
    #***************************************************************************    
    def decode(self, data):
        num_rtes = int((len(data) - HEADER_SIZE) / RTE_SIZE)
        decoded_rte_table = {}
        
        # Unpack the header
        header = struct.unpack_from(HEADER_FORMAT, data)
        self.COMMAND = header[0]
        self.VERSION = header[1]
        self.src = header[2]
        
        # Unpack each RTE, beginning from the first one.
        i = HEADER_SIZE
        while i < len(data):
            rte = struct.unpack_from(RTE_FORMAT, data[i:])
            
            # Check validity of RTE
            if rte[0] == AFI and rte[1] == TAG and rte[4] >= 1 and rte[4] <=16:
                addr = rte[2]
                nxt_hop = rte[3]
                metric = rte[4]
                decoded_rte_table[addr] = [nxt_hop, metric]
                i += RTE_SIZE #increment by size of one RTE 
            else:
                i += RTE_SIZE
        return decoded_rte_table


################################################################################
    # test
################################################################################
rting_table = {2: [2, 5, 0, 0, 0], 3: [2, 7, 0, 0, 0], 4: [6, 2, 0, 0, 0]}
y = Packet(1, 2, rting_table)
x = y.encode()
y.decode(x)