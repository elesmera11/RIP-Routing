"""RIP ROUTING ASSIGNMENT - COSC364
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 03/03/2018 """


import random
import time
import socket
import select
import sys

MIN_PORT = 1024
MAX_PORT = 64000
input_ports = []
output_ports = {}
router_id = -1
routing_table = {} #format is [dest_router_id][metric, flag, timers, next_hop_port]


#------------------------------------------------------------------------------#
# Input processing
#------------------------------------------------------------------------------#


def process_cmd(filename):
    print("Reading the supplied config file...")
    #open and read the file
    config_file = open(filename, 'r')
    router_id_line = config_file.readline()
    input_ports_line = config_file.readline()
    output_ports_line = config_file.readline()
    process_router_id(router_id_line)
    process_input_ports(input_ports_line)
    process_output_ports(output_ports_line)
    
def process_router_id(first_line):
    global router_id
    words = first_line.strip().split(',')
    #checking first line format
    if ((len(words) == 2) and (words[0] == 'router_id')):
        router_id = int(words[1])
    #else throw error and quit
    else:            
        print("Incorrect configuration file format")
        sys.exit() 
    print("The router ID is " + str(router_id))
    
def process_input_ports(second_line):
    global input_ports
    words = second_line.strip().split(',')
    #checking second line format
    if ((len(words) >= 2) and (words[0] == 'input_ports')):
        for ii in range(1, len(words)):
            #check that it is a port number
            port_no = int(words[ii])
            if ((port_no >= MIN_PORT) and (port_no <= MAX_PORT)):
                input_ports.append(port_no)
            else:
                print("Port number not valid")
                sys.exit()       
    #else throw error and quit
    else:            
        print("Incorrect configuration file format")
        sys.exit() 
    print("The input ports are " + ', '.join(str(num) for num in input_ports))
    
def process_output_ports(third_line):
    global output_ports
    global routing_table
    words = third_line.strip().split(',')
    #checking third line format
    if ((len(words) >= 2) and (words[0] == 'output_ports')):
        for ii in range(1, len(words)):
            #check that the format of each entry is correct
            port_data = words[ii].split('-')
            port_data = [int(i) for i in port_data]
            if ((len(port_data) == 3) and (port_data[0] >= MIN_PORT) 
                and (port_data[0] <= MAX_PORT) and (port_data[1] >=0)
                and (port_data[1] <= 16)):
                port_no, metric, peer_router_id = port_data
                timers = [0, 0]
                flags = False
                #add to routing table and output ports list
                routing_table[peer_router_id] = [metric, flags, timers, peer_router_id]
                output_ports[peer_router_id] = port_no
            else: 
                print("Incorrect configuration file format")
                sys.exit() 
    else: 
        print("Incorrect configuration file format")
        sys.exit()     
    print("The output ports are:")
    print(output_ports)


#------------------------------------------------------------------------------#
# String manipulation and printing
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
# Daemon creation and sockets
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
# Time functions
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
# Datagram transfer
#------------------------------------------------------------------------------#
my_file = "config_1" 
process_cmd(my_file)