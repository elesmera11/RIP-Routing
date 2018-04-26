"""RIP ROUTING ASSIGNMENT - COSC364
ConfigParser.py - Main code for virtual routers.
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 26/04/2018 """

import configparser
import sys

MAX_PORT = 64000
MIN_PORT = 1024
MAX_ID = 64000
MIN_ID = 1


#*******************************************************************************
# Function to parse the user configuration of the router.
# @param filename the filename of the config text file
# @return configurations in format [self ID, [input ports], [output ports]]
# where output ports are of format [port, metric, peer ID] 
#*******************************************************************************
def get_config(filename):
    all_ports = []
    config_list = []
    output_ports = []
    config = configparser.ConfigParser()
    config.read(filename)
    
    # Read the router ID
    router_id = int(config.get('Router', 'router-id'))
   
    # Check validity of router id
    if router_id < MIN_ID or router_id > MAX_ID:
        raise Exception("Error - Router ID must be between 1 and 64000")
    
    # Read the input ports
    input_ports = config.get('Router', 'input-ports').split(" ")
    all_ports = list(input_ports)
    
    #read the output ports
    outputs_split = config.get('Router', 'output-ports').split(" ")
    for output in outputs_split:
        output_data = output.split("-")
        all_ports.append(output_data[0])
        output_ports.append(output_data)
    
    # Check validity of all ports
    check_ports(all_ports)
        
    config_list.append(router_id)
    config_list.append(input_ports)
    config_list.append(output_ports)
    
    return config_list

#*******************************************************************************
# Function to check the validity of all ports
# @param ports_list the list of all ports both in and out
#*******************************************************************************
def check_ports(ports_list):
    # Check the port number
    for port in ports_list:
        port = int(port)
        if port < MIN_PORT or port > MAX_PORT:
            raise Exception("Error - Port number must be between 1024 and 64000")
    # Check for duplicates
    if len(set(ports_list)) != len(ports_list):
        raise Exception("Error - Duplicate port number")  