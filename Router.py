import select

HOST = "127.0.0.1"
INFINITY = 16
TIME_BLOCK = 30
PERIODIC_UPDATE = 30 / TIME_BLOCK
TIME_OUT = 180 / TIME_BLOCK
GARBAGE_COLLECTION = 120 / TIME_BLOCK

class Router:
    router_id = 0
    inputs = []
    outputs = []
    rt_tbl = dict()
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
        return
    
    # Triggers update    
    def trigger_update():
        return
    
    # Sends periodic update 
    def send_update():
        return
    
    # Processes incoming packet
    def read_packet(data):
        packet = data.decode()
        if check_packet(packet) == True:
            print("Processing packet")
            update_rt_tbl(packet.get_rtes())
        return
        
    # Checks the packet's validity
    def check_packet(self, packet):
        if packet.get_dst == self.router_id:
            if packet.get_src() in self.neighbours.keys():
                return True
            else:
                print("Packet dropped - not a valid neighbour")
                return False
        else:
            print("Packet dropped - Not for this address")
            return False
    
    # Updates the routing table
    def update_rt_tbl(self, rtes):
        keys = rt_tbl.keys()
        rt_nxt_hop = rt_tbl[dst][0]
        rt_metric = rt_tbl[dst][1]
        rt_rfc = rt_tbl[dst][2]
        rt_time_out = rt_tbl[dst][3]
        rt_gbg_coll = rt_tbl[dst][4]
        for dst in rtes.keys():
            nxt_hop = rtes[dst][0]
            metric = rtes[dst][1]
            new_metric = MIN(get_neighbour_metric(nxt_hop) + metric, INFINITY)
            if dst not in keys:
                if new_metric < 16:
                    rt_tbl[dst] = nxt_hop, new_metric, 0, init_time_out(), 0
            else:        
                if rt_metric < 16:
                    if rt_time_out > TIME_OUT:
                        rt_metric = 16
                        rt_rfc = 1
                        rt_gbg_coll = init_gbg_coll
                        trigger_update()
                    elif nxt_hop == rt_nxt_hop and new_metric < 16:
                        if new_metric == rt_metric:
                            reset_time_out()
                        else:
                            rt_metric = new_metric
                    elif nxt_hop == rt_nxt_hop and new_metric == 16:
                        rt_metric = new_metric
                        rt_rfc = 1
                        rt_time_out = init_time_out()
                        rt_gbg_coll = init_gbg_coll()
                        trigger_update()
                    elif nxt_hop != rt_nxt_hop and new_metric < rt_metric:
                        rt_nxt_hop = nxt_hop
                        rt_metric = new_metric
                        rt_time_out = init_time_out()
                else:
                    if rt_time_out > GARBAGE_COLLECTION:
                        del rt_tbl[dst]
                    elif new_metric < 16:
                        rt_nxt_hop = nxt_hop
                        rt_metric = new_metric
                        rt_time_out = init_time_out()
                        rt_gbg_coll = clear_gbg_coll()
        print_routing_table()
        return
                
    def init_time_out():
        
    def reset_time_out():
    
    def init_gbg_coll():
        
    def clear_gbg_coll():
    
    def print_routing_table():
        
    def run(self):
        while True:
        read_ready, send_ready, except_ready = select.select(self.inputs, [], [])
        if read_ready