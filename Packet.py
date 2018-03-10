class Packet:
    header_format = "!BBH"
    rte_format = "!HHIII"
    header_size = struct.calcsize(header_format)
    rte_size = struct.calcsize(rte_format)
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
        
    def encode(self):
        encoded_packet = struct.pack(header_format, self.command, self.version, self.src)
        for key in rtes.keys():
            if key != self.dst:
                add = key
                nxt_hop = rte[key][0]
                metric = rte[key][1]
                encoded_packet += struct.pack(rte_format, self.afi, self.tag, add, nxt_hop, metric)
        return encoded_packet
    
    def decode(self, data):
        num_rtes = int((len(data) - header_size) / rte_size)
        header = struct.unpack_from(header_format, data)
        self.command = header[0]
        self.version = header[1]
        self.src = header[2]
        i = header_size
        while i < len(data):
            rte = struct.unpack_from(rte_format, data[i:])
            if rte[0] == self.sfi and rte[1] == self.tag and rte[4] >= 1 and rte[4] <=16:
                add = rte[2]
                nxt_hop = rte[3]
                metric = rte[4]
                rtes[add] = nxt_hop, metric
                i += rte_size
            else:
                i += rte_size
        return 
    
