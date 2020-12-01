###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Ali Kalaycı
# Collaborators:
# Time:

from ps1_partition import get_partitions
# helper code it generates permutations

import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    print("Loading word list from file...")
    f= open(filename, 'r')
    cows= {}
    for line in f:
        ans=line.split(',')
        cows[ans[0]]=int(ans[1])
    print('{0} cows loaded'.format(len(cows)), '\n')
    return cows


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # sorting cows according to their weights
    cow_list=sorted(cows.items(), key= lambda x: x[1], reverse= True)
    weight= 0
    result= []
    while len(cow_list) != 0:
        trip= []
        weight= 0
        # copied list required to remove things
        copied= cow_list[:]
        for i in range(len(copied)):
            if (weight+copied[i][1]) <= limit:
                trip.append(copied[i][0])
                weight += copied[i][1]
                cow_list.remove(copied[i])
        print('weight of trip:',weight)
        print('trip taken', trip, '\n')
        result.append(trip)
    return result

cows= load_cows('ps1_cow_data.txt')
#greedy_cow_transport(cows)

# Problem 3
def brute_force(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that
        #Explore right branch
        #Choose better one minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dict of {name (string): weight (int)}
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # shallow copy of dict
    cow_dict = cows.copy()
    res= []
    for partit in get_partitions(cow_dict.keys()):
        weighover= False
        for trip in partit:
            weigh= 0
            for cow in trip:
                weigh +=cow_dict[cow]            
            if weigh >= limit:
                weighover= True
                break
        if weighover:
            continue
        elif len(res) == 0 or len(res) > len(partit):
            res= partit
    return res

def test_bruteforce():
    cows= load_cows('ps1_cow_data.txt')
    res= brute_force(cows)
    print(res)
    print(len(res))
    return res        

#test_bruteforce()
# Problem 4
    
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows= load_cows('ps1_cow_data.txt')
    start = time.time()
    res= brute_force(cows)
    end= time.time()
    print(res)
    print('brute force time '+ str(end-start)+ '\n')
    start = time.time()
    res=  greedy_cow_transport(cows)
    end= time.time()
    print(res)
    print('greedy time '+ str(end-start))
    return 1
compare_cow_transport_algorithms()
