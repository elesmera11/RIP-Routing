class Router:
    INFINITY = 16
    MIN_HOP = 0
    router_id = 0
    routing_table = Routing_Table()
    
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
                
        
    