
#based on Simulation Modeling and Analysis, Averil Law

import numpy.random as random

#Adds new items to inventory and clears backlogged items
def add_items(num_items, items_inventory, inventory_levels, sim_time):
    to_add = num_items;
    if (inventory_levels < 0):
        to_add = num_items + inventory_levels;
    for i in range(to_add):
        new_time = sim_time + random.uniform(1.5, 2.5)
        items_inventory.append(new_time)
    inventory_levels += num_items;
    return inventory_levels

#Takes the items from the inventory
def take_items(num_items, items_inventory, inventory_levels, roten_items, sim_time):
    to_take = num_items;
    for i in range(inventory_levels):
        item = items_inventory.pop(0);
        if (item >= sim_time): #In case the item is ok
            num_items -= 1;
            if num_items == 0:
                break;
        else: #In case the item is expired
            roten_items += 1;
            to_take += 1;
    inventory_levels = inventory_levels - to_take;
    return inventory_levels, roten_items

#Make time pass
def timing(next_event_type, time_next_event, sim_time):
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
        #print('Event list is emplty at time', sim_time)
        sys.exit()
    #We advance the time to the next event
    sim_time = min_time_next_event
    return next_event_type, sim_time

#Event: the order arrives
def arrive_order(inventory_levels, outstanding_order, items_inventory, sim_time):
    #print("received:", outstanding_order, " and have:", inventory_levels)
    inventory_levels = add_items(outstanding_order, items_inventory, inventory_levels, sim_time);
    #print("now have:", inventory_levels)
    return inventory_levels

#Event: a customer places a order
def demand_costumer(inventory_levels, items_inventory, all_customer_demands, all_roten_items, time_next_event, sim_time):
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
    inventory_levels, all_roten_items = take_items(order, items_inventory, inventory_levels, all_roten_items, sim_time);

    #Place the event for the next order
    time_next_order = sim_time + random.exponential(scale=0.1)
    time_next_event.append(('customer_demand', time_next_order))
    #print("sold:", order)
    return inventory_levels, all_customer_demands, all_roten_items

#Evento: begining of the month, reavaluate inventory
def inventory_evaluation_and_ordering(inventory_levels, time_next_event, inventory_data, prices, sim_time, outstanding_order, statistics):
    #SE O INVENTARIO FOR MENOR QUE ZERO COLOCO EXPRESSO
    (inc_normal, inc_express, base_normal, base_express) = prices
    (small_s, big_s) =  inventory_data

    [handling_cost, ordering_cost, shortage_cost, all_orders] = statistics;

    #Check the inventory levels
    to_order = 0;
    inc = inc_normal;
    base = base_normal;
    #print("EVALUATION-> HAS:", inventory_levels)
    if inventory_levels < 0:
        #print("WILL ASK EXPRESSO BECAUSE:", inventory_levels)
        #input()
        to_order = big_s - inventory_levels;
        inc = inc_express;
        base = base_express;
        next_delivery_time = sim_time + random.uniform(0.25, 0.5)
        #print("WILL ORDER EXPRESSO")
    elif inventory_levels < small_s:
        to_order = big_s - inventory_levels;
        next_delivery_time = sim_time + random.uniform(0.5, 1)
        #print("WILL ORDER NORMAL")

    #Add the next event to evaluate inventory
    next_avaliation_time = sim_time + 1;
    time_next_event.append(('avaliation', next_avaliation_time))

    #Check that the quantity to demmand is bigger than zero
    if to_order > 0:
        #print("now have", inventory_levels, " so will order", to_order)

        ordering_cost += base + inc * to_order;
        outstanding_order = to_order;
        all_orders += to_order;

        #Adds the event to receive the new stock
        time_next_event.append(('delivery', next_delivery_time))
    
    #Adds cost 5 per item in the backlog
    if inventory_levels < 0:
        print("SHORTAGE COST:", shortage_cost)
        shortage_cost += - 5 * inventory_levels; #Negative because the inventory level is negative also
        print("SHORTAGE COST:", shortage_cost)
    else:
        #Adds cust 1 for every item in the inventory
        handling_cost += inventory_levels

    statistics = [handling_cost, ordering_cost, shortage_cost, all_orders];
    return outstanding_order, statistics 

#Event: End of the simulation
def end_simulation(continue_simulation):
    continue_simulation = False


# main
# initialize
# state variables

def iteration(inventory_data):
    sim_time = 0
    outstanding_order = 0;
    time_last_event = 0.0;

    outstanding_order = 0;
    time_last_event = 0.0;


    inc_normal = 3
    inc_express = 4
    base_normal = 32;
    base_express = 48;
    prices = (inc_normal, inc_express, base_normal, base_express)

    #all_s = [(20,40), (20,60), (20,80), (20,100), (40,60), (40,80), (60,80), (60,100)];

    #inventory_data = all_s[N];

    simulation_end_months = 120

    inventory_levels = 0;
    continue_simulation = True;

    # statistics
    total_cost = 0;
    handling_cost = 0;
    ordering_cost = 0;
    shortage_cost = 0;
    all_customer_demands = 0;
    all_roten_items = 0;
    all_orders = 0;

    statistics = [handling_cost, ordering_cost, shortage_cost, all_orders]

    items_inventory = [];
    inventory_levels = add_items(inventory_data[1] + 20, items_inventory, inventory_levels, sim_time);

    time_next_event = []
    time_next_event.append(("End_simulation", simulation_end_months))

    time_next_order = random.exponential(scale=0.1)
    time_next_event.append(('customer_demand', time_next_order))
    time_next_event.append(('avaliation', 1))

    next_event_type = ''

    #Até ao fim da simulação
    while continue_simulation:
        
        #Faz o tempo passar
        next_event_type, sim_time = timing(next_event_type, time_next_event, sim_time)

        #Caso o próximo evento seja um cliente chegar ou sair, executa a função respetiva
        if next_event_type == 'End_simulation':
            continue_simulation = end_simulation(continue_simulation)
        elif next_event_type == 'avaliation':
            outstanding_order,statistics = inventory_evaluation_and_ordering(inventory_levels, time_next_event, inventory_data, prices, sim_time, outstanding_order, statistics);
        elif next_event_type == 'customer_demand':
            inventory_levels, all_customer_demands, all_roten_items = demand_costumer(inventory_levels, items_inventory, all_customer_demands, all_roten_items, time_next_event, sim_time)
        elif next_event_type == 'delivery':
            inventory_levels = arrive_order(inventory_levels, outstanding_order, items_inventory, sim_time)
        #input("COPNTINUE")
    
    [handling_cost, ordering_cost, shortage_cost, all_orders] = statistics;
    total_cost = handling_cost+ordering_cost+shortage_cost
    #print("total_cost:", handling_cost+ordering_cost+shortage_cost)
    #print("handling_cost:", handling_cost)
    #print("ordereing_cost:", ordering_cost)
    #print("shortage_cost:", shortage_cost)
    #print("total_demands:", all_customer_demands)
    #print("total_orders:", all_orders)
    return total_cost, all_customer_demands, all_roten_items, statistics


def main():
    sum_cost = 0;
    sum_demands = 0;
    sum_roten = 0;

    handling_sum = 0
    ordering_sum = 0
    shortage_sum = 0
    ordered_sum = 0;

    iters = 100;
    num = 7 #TEST

    all_s = [(20,40), (20,60), (20,80), (20,100), (40,60), (40,80), (60,80), (60,100)];

    inventory_data = all_s[num];
    
    for _ in range(iters):
        new_cost, new_demands, new_roten, all_costs = iteration(inventory_data)

        [handling, ordering, shortage, ordered] = all_costs

        sum_cost += new_cost
        sum_demands += new_demands
        sum_roten += new_roten

        handling_sum += handling;
        ordering_sum += ordering;
        shortage_sum += shortage;
        ordered_sum += ordered;

    print("SMALL_S:", inventory_data[0], " BIG_S:", inventory_data[1])
    print("N:", num, " AND IN 10 THE AVERAGE COST IS:", sum_cost/iters)
    print("N:", num, " AND IN 10 THE AVERAGE DEMANDS IS:", sum_demands/(iters*120))
    print("N:", num, " AND IN 10 THE AVERAGE ROTEN IS:", sum_roten/(iters*120))

    print("N:", num, " AND IN 10 THE AVERAGE HANDLING IS:", handling_sum/(iters))
    print("N:", num, " AND IN 10 THE AVERAGE ORDERING IS:", ordering_sum/(iters))
    print("N:", num, " AND IN 10 THE AVERAGE SHORTAGE IS:", shortage_sum/(iters))
    print("N:", num, " AND IN 10 THE AVERAGE ORDERED IS:", ordered_sum/(iters*120))

if __name__ == "__main__":
    main()

