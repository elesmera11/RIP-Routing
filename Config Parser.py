import configparser

def get_config(filename):
    config_list = []
    config =configparser.ConfigParser()
    config.read(filename)
    router_id = int(config.get('Router', 'router-id'))
   
   # Check validity of router id
    if router_id < 1 or router_id > 64000:
        print("Error - Router ID must be between 1 and 64000")
        return
    
    input_ports = config.get('Router', 'input-ports').split(" ")
    all_ports = input_ports
    output_list = []
    outputs = config.get('Router', 'outputs').split(" ")
    for output in outputs:
        output_data = output.split("-")
        all_ports.append(output_data[0])
        output_list.append(output_data)
    
    # Check validity of all ports
    
    for port in all_ports:
        port = int(port)
        if port < 1024 or port > 64000:
            print("Error - Port number must be between 1024 and 64000")
            return
    
    # Check for unique port numbers
    if len(set(all_ports)) != len(all_ports):
        print("Error - Duplicate port number")
    
    config_list.append(router_id)
    config_list.append(input_ports)
    config_list.append(output_list)
    
    return config_list

