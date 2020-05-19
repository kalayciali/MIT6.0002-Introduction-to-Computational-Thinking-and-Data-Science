###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Ali Kalaycı
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
import random

def build_eggs(numItems, maxWeight):
    eggs = []
    for i in range(numItems):
        eggs.append(random.randint(1, maxWeight))
    res= sorted(eggs)
    return tuple(res)

def dp_make_weight(egg_weights, target):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
        
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
        build_eggs func is used to give egg_weights
    target - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    # Recursive algorith without dynamic programming
    # don't expect too much performance
    if egg_weights == () or target == 0:
        result = (0, ())
    elif egg_weights[0] > target:
        #Explore right branch only (Don't take)
        result= dp_make_weight(egg_weights[1:], target)
    else:
        nextItem = egg_weights[0]
        #Explore left branch (take)
        withEgg, withTake = dp_make_weight(egg_weights[1:], target- nextItem)
        withEgg += 1
        #Explore right branch
        withoutEgg, withoutTake = dp_make_weight(egg_weights[1:], target)
        #Choose better branch
        if withEgg > withoutEgg:
            result = (withEgg, withTake + (nextItem,)) 
        else:
            result = (withoutEgg, withoutTake)
    return result

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = build_eggs(20,20)
    n = 99
    print("n = ", n)
    print("output:", dp_make_weight(egg_weights, n))
    print()