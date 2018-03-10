class Packet:
    command = 2
    version = 2
    src = 0
    dst = 0
    afi = AF_INET
    tag = 0
    rtes = dict()
    
    def __init__(self, src, dst, routing_table):
        self.src = src
        self.dst = dst
        self.rtes = routing_table
        
    def encode():
        header_format = "!BBH"
        encoded_packet = struct.pack(header_format, command, version, src)
        rte_format = "!HHIII"
        for key in rtes.keys():
            add = key
            nxt_hop = rte[key][0]
            metric = rte[key][1]
            encoded_packet += struct.pack(rte_format, afi, tag, add, nxt_hop, metric)
        return encoded_packet
    
    def decode():
        
        return decoded_packet
    
