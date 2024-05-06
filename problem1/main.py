
#based on Simulation Modeling and Analysis, Averil Law

import numpy.random as random

#Make time pass
def timing():
    global next_event_type 
    global time_next_event
    global sim_time

    min_time_next_event = 1e9

    next_event_type = ''
    min_event = time_next_event[0]
    
    for event in time_next_event: #We get the minimum time until the next event to advance to it
        if event[1] < min_time_next_event:
            min_time_next_event = event[1]
            next_event_type = event[0]
            min_event = event
    
    time_next_event.remove(min_event)
    if next_event_type == '':
        print('Event list is emplty at time', sim_time)
        sys.exit()
    #We advance the time to the next event
    sim_time = min_time_next_event

#Event: the order arrives
def arrive_order():
    global inventory_levels
    global backlogged_demand
    global outstanding_order

    #Update the inventory levels, taking first the ones that were backlogged
    print("received:", outstanding_order, " and have:", inventory_levels)
    if outstanding_order > backlogged_demand:
        inventory_levels = inventory_levels + outstanding_order - backlogged_demand;
        backlogged_demand = 0;
        outstanding_order = 0;
    else:
        #If we hav more backlogged items than the ones we received
        backlogged_demand -= outstanding_order
        outstanding_order = 0;
    print("now have:", inventory_levels)

#Event: a customer places a order
def demand_costumer():
    global inventory_levels 
    global backlogged_demand
    global time_next_event
    global sim_time
    global all_customer_demands

    #Calculate the quantity to order
    order_rand = random.uniform(0,6)
    order = 4;
    if order_rand <= 1:
        order = 1;
    elif order_rand <= 3:
        order = 2;
    elif order_rand <= 5:
        order = 3;
    all_customer_demands += order;

    #If we can satisfy the order with our inventory_levels, we do so
    #if inventory_levels >= order:
    #    inventory_levels -= order;
    #else:
        #If not, we take all that remains in the inventory and put the rest in backlog
        #backlogged_demand = backlogged_demand + order - inventory_levels;
    #    inventory_levels = 0;
    inventory_levels -= order;

    #Place the event for the next order
    time_next_order = sim_time + random.exponential(scale=0.1)
    time_next_event.append(('customer_demand', time_next_order))
    print("sold:", order)

#Evento: begining of the month, reavaluate inventory
def inventory_evaluation_and_ordering():
    global inventory_levels
    global time_next_event
    global backlogged_demand
    global small_s
    global big_s
    global sim_time
    global shortage_cost
    global handling_cost
    global all_orders

    #SE O INVENTARIO FOR MENOR QUE ZERO COLOCO EXPRESSO

    #Check the inventory levels
    to_order = 0;
    inc = inc_normal;
    base = base_normal;
    #if inventory_levels == 0 and backlogged_demand > 0:
    if inventory_levels < 0:
        to_order = big_s - inventory_levels;
        inc = inc_express;
        base = base_express;
        next_delivery_time = sim_time + random.uniform(0.25, 0.5)
    elif inventory_levels < small_s:
        #to_order = big_s - inventory_levels + backlogged_demand;
        to_order = big_s - inventory_levels;
        next_delivery_time = sim_time + random.uniform(0.5, 1)

    #Add the next event to evaluate inventory
    next_avaliation_time = sim_time + 1;
    time_next_event.append(('avaliation', next_avaliation_time))

    #Check that the quantity to demmand is bigger than zero
    if to_order > 0:
        global outstanding_order
        global ordereing_cost
        global inc
        print("now have", inventory_levels, " so will order", to_order)

        ordereing_cost += base + inc * to_order;
        outstanding_order = to_order;
        all_orders += 1;

        #Adds the event to receive the new stock
        time_next_event.append(('delivery', next_delivery_time))

    #Adds cust 1 for every item in the inventory
    handling_cost += inventory_levels
    
    #Adds cost 5 per item in the backlog
    if inventory_levels < 0:
        #shortage_cost += 5 * backlogged_demand
        shortage_cost += - 5 * inventory_levels; #Negative because the inventory level is negative also

#Event: End of the simulation
def end_simulation():
    global continue_simulation
    continue_simulation = False


# main

# initialize

# simulation clock
sim_time = 0.0

# state variables
outstanding_order = 0;
time_last_event = 0.0;
#backlogged_demand = 0;

all_s = [[20,40], [20,60], [20,80], [20,100], [40,60], [40,80], [60,80], [60,100]];

s = all_s[0];
small_s = s[0];
big_s = s[1];
inc_normal = 3
inc_express = 4
base_normal = 32;
base_express = 48;

inventory_levels = big_s + 20;
continue_simulation = True;

# statistics
total_cost = 0;
handling_cost = 0;
ordereing_cost = 0;
shortage_cost = 0;
all_customer_demands = 0;
all_orders = 0;
    
# event list
time_next_event = []
time_next_event.append(("End_simulation", 120))

time_next_order = random.exponential(scale=0.1)
time_next_event.append(('customer_demand', time_next_order))
time_next_event.append(('avaliation', 1))

next_event_type = ''

#Até ao fim da simulação
while continue_simulation:
    
    #Faz o tempo passar
    timing()
    
    #Caso o próximo evento seja um cliente chegar ou sair, executa a função respetiva
    if next_event_type == 'End_simulation':
        end_simulation()
    elif next_event_type == 'avaliation':
        inventory_evaluation_and_ordering()
    elif next_event_type == 'customer_demand':
        demand_costumer()
    elif next_event_type == 'delivery':
        arrive_order()
       
print("total_cost:", handling_cost+ordereing_cost+shortage_cost)
print("handling_cost:", handling_cost)
print("ordereing_cost:", ordereing_cost)
print("shortage_cost:", shortage_cost)
print("total_demands:", all_customer_demands)
print("total_orders:", all_orders)
##
