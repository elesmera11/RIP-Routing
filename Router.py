class Router:
    HOST = "127.0.0.1"
    router_id = 0
    inputs = []
    outputs = []
    routing_table = dict()
    neighbours = dict()
    
    def __init__(self, config_list):
        self.router_id = config_list[0]
        for port in config_list[1]:
            socket = create_socket(port)
            self.inputs.append(socket)
        for port, cost, router in config_list[2]:
            self.neighbours[router] = int(port), int(cost)
            socket = create_socket(port)
            self.outputs.append(socket)
        return
    
    # Get neighbour's metric
    def get_neighbour_metric(self, router_id):
        return self.neighbours[router_id][1]
    
    # Get neighbour's port
    def get_neighbour_port(self, router_id):
        return self.neighbours[router_id][0]
    
    # Creates sockets
    def create_socket(self, port):
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.setblocking(False)
        socket.bind((HOST, port))
        print("Socket " + str(port) + " created")
        return socket
    
    # Sends packet
    def send_packet(packet):
        
    
    # Triggers update    
    def trigger_update():
        
    # Sends periodic update 
    def send_update():
        
    # Add route to routing table
    def read_packet(rcvd_packet):
        packet = rcvd_packet.decode()
        if packet.check_packet == True:
            new_metric = MIN(metric + cost, INFINITY)
            if routing_table.check_route(packet.get_route) == False:
                routing_table.add_route(route)
            else:
                
        
    