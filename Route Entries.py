class Route_Entries:
    dst_add = ""
    nxt_hop_add = ""
    metric = 0
    route_change_flag = False
    time_out = 0
    garbage_collection = 0
    
    def __init__(self, dst, nxt_hop, distance):
        self.dst_add = dst
        self.nxt_hop_add = nxt_hop
        self.metric = distance
        
    def create_route(dst, nxt_hop, distance):
        route = Route(dst, nxt_hop, distance)
        return route
    
    def set_route_change_flag():
        route.route_change_flag = True
        
    def clear_route_change_flag():
        route.route_change_flag = False
        
    def set_time_out():
        route.time_out = 30
        
    def clear_time_out():
        route.time_out = 0
        
    def set_garbage_collection():
        route.garbage_collection = 120
        
    def clear_garbage_collection():
        route.garbage_collection = 0
        
    def update_metrics(new_metric):
        route.metric = new_metric
    
    def update_next_hop(new_hop):
        route.nxt_hop_add = new_hop
        
    