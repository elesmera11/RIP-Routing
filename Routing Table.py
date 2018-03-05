"""RIP ROUTING ASSIGNMENT - COSC364
Authors: Shan Koo and Kate Chamberlin
Due date: 27/04/2018, 11:59pm
Date of last edit: 05/03/2018 """

class Routing_Table:
    routing_table = []
    entries = 0;
    
# Adds new route to the routing table
def add_route(route):
    routing_table.append(route)
    entries += 1

# Deletes route from the routing table
def delete_route(route):
    i = 0
    while i < entries:
        if routing_table[i].dst_add == route:
            routing_table.pop(i)
        else:
            i += 1
    entries -= 1
    
# Checks if route already in routing table
def check_route(route, routing_table):
    if route in routing_table:
        return True
    else:
        return False


