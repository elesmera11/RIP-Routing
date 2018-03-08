import configparser

def get_config(filename):
    config =configparser.ConfigParser()
    config.read(filename)
    router_id = int(config.get('Router', 'router-id'))
   
    if router_id < 1 or router_id > 64000:
        print("Router ID must be between 1 and 64000")
        return
    input_ports = config.get('Router', 'input-ports').split(" ")
    
    for port in input_ports:
        if int(port) < 1024 or int(port) > 64000:
            print("Port number must be between 1024 and 64000")
            return
        
    if len(set(input_ports)) != len(input_ports):
        print("Duplicate port number")
        return
   
    outputs = config.get('Router', 'outputs').split(" ")
    print(outputs)
    return

filename = "config_1.ini"
get_config(filename)