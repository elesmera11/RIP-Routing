import configparser

def get_config(filename):
    config_list = []
    config =configparser.ConfigParser()
    config.read(filename)
    router_id = int(config.get('Router', 'router-id'))
   
    if router_id < 1 or router_id > 64000:
        print("Router ID must be between 1 and 64000")
        return
    config_list.append(router_id)
    print(config_list)
    input_ports = config.get('Router', 'input-ports').split(" ")
    
    input_port_list = []
    for port in input_ports:
        if int(port) < 1024 or int(port) > 64000:
            print("Port number must be between 1024 and 64000")
            return
        else:
            input_port_list.append(port)
        
    if len(set(input_ports)) != len(input_ports):
        print("Duplicate port number")
        return
    config_list.append(input_port_list)
    print(config_list)
    print(config_list[1][1])
   
    output_list = []
    outputs = config.get('Router', 'outputs').split(" ")
    for output in outputs:
        output_data = output.split("-")
        output_list.append(output_data)
    config_list.append(output_list)
    print(config_list)
    print(config_list[0])
    print(config_list[1])
    print(config_list[2])
    return

filename = "config_1.ini"
get_config(filename)