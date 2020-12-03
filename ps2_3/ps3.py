# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y  
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + '{0}, {1}'.format(self.x, self.y)


# === Problem 1
class RectRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        ## coded ##
        if type(width) == int and type(height)==int and type(dirt_amount)== int:
            self.width= width
            self.height= height
            self.rect_room= {}
            for x in range(width):
                for y in range(height):
                    self.rect_room[(x,y)]= dirt_amount
        else:
            raise ValueError('only int acceptable')
        
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        ## coded ##
        x, y= pos.get_x(),  pos.get_y()
        x_int= math.floor(x)
        y_int= math.floor(y)
        dirt = self.rect_room[(x_int, y_int)]
        self.rect_room[(x_int, y_int)] = dirt- capacity
        if self.rect_room[(x_int, y_int)] < 0:
            self.rect_room[(x_int, y_int)] = 0   

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        ## coded ##
        if self.rect_room[(m,n)] == 0:
            return True
        return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        ## coded ##
        num=0
        for dirt in self.rect_room.values():
            if dirt == 0:
                num += 1
        return num
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        ## coded ##
        x, y= pos.get_x(),  pos.get_y()
        x_int= math.floor(x)
        y_int= math.floor(y)
        if (x_int, y_int) in self.rect_room.keys():
            return True
        return False
    
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.rect_room[(m,n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        return len(self.rect_room)
        
    def get_random_posit(self):
        """
        Returns: a Position object; a random position inside the room
        """
        ## coded ##
        x= round(random.uniform(0, (self.width- 0.01)), 2)
        y= round(random.uniform(0, (self.height- 0.01)), 2)
        return Position(x,y)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        ## coded ##
        self.room= room
        self.posit= room.get_random_posit()
        self.direct= round(random.uniform(0, 359.99), 2)
        self.capacity= capacity
        if speed >= 0:
            self.speed= speed
        else:
            raise ValueError('speed cant be negative')
        
    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.posit

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direct
    
    
    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.posit= position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direct= direction


# === Problem 2
class EmptyRoom(RectRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.rect_room)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        return self.is_position_in_room(pos)
        
    def get_random_posit(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return RectRoom.get_random_posit(self)

class FurnishedRoom(RectRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furnited = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furnited.append((i,j))             
        print(self.furnited)
    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        if (m,n) in self.furnited:
            return True
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        ## coded ##
        x, y= pos.get_x(),  pos.get_y()
        x_int= math.floor(x)
        y_int= math.floor(y)
        print('1')
        if (x_int, y_int) in self.furnited:
            return True
        return False
    
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        ## coded ##
        if self.is_position_in_room(pos):
            if not self.is_position_furnished( pos) :
                return True
        return False
        
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return len(self.rect_room)- len(self.furnited)
    
    def get_random_posit(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        ## coded ##
        while True:
            posit= RectRoom.get_random_posit(self)
            if self.is_position_valid( posit):
                return posit
    



# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        ## coded ##
        room= self.room
        posit_now= self.get_robot_position()
        direct_now= self.get_robot_direction()
        # to check the tile is clean or not, indices taken
        x_int, y_int= math.floor(posit_now.get_x()), math.floor(posit_now.get_y())
        node_list= []
        if not room.is_tile_cleaned(x_int, y_int):
            # if it is not clean
            room.clean_tile_at_position(posit_now, self.capacity)
            # trying to locate the robot to the same tile
            new_posit= posit_now.get_new_position(direct_now, self.speed)
            x_new, y_new= new_posit.get_x(), new_posit.get_y()
            if x_int< x_new < x_int+1 and y_int< y_new < y_int+1:
                # i force it to locate the same tile
                if room.is_position_valid(new_posit):
                    self.set_robot_position(new_posit)
        else:
            # append tile as clean
            node_list.append((x_int,y_int))
            new_posit= posit_now.get_new_position(direct_now, self.speed)
            x_int, y_int= math.floor(new_posit.get_x()), math.floor(new_posit.get_y())
            # force it to select uncleaned tile
            if not (x_int, y_int) in node_list:
                # if random tile not in cleaned list
                if room.is_position_valid(new_posit):
                    self.set_robot_position(new_posit)
            
            new_direct= round(random.uniform(0, 359.99), 2)
            self.set_robot_direction(new_direct)

from test_robot_movement import test_robot_movement 
# Uncomment this line to see your implementation of StandardRobot in action!
#test_robot_movement(StandardRobot, EmptyRoom)
#test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        ## coded ##
        room= self.room
        posit_now= self.get_robot_position()
        direct_now= self.get_robot_direction()
        
        if self.gets_faulty():
            # faulty robot
            new_posit= posit_now.get_new_position(direct_now, self.speed)
            if room.is_position_valid(new_posit):
                self.set_robot_position(new_posit)
                new_direct= round(random.uniform(0, 359.99), 2)
                self.set_robot_direction(new_direct)
                
        
        else:
            # same code
            x_int, y_int= math.floor(posit_now.get_x()), math.floor(posit_now.get_y())
            node_list= []
            if not room.is_tile_cleaned(x_int, y_int):
                
                room.clean_tile_at_position(posit_now, self.capacity)
                new_posit= posit_now.get_new_position(direct_now, self.speed)
                x_new, y_new= new_posit.get_x(), new_posit.get_y()
                
                if x_int< x_new < x_int+1 and y_int< y_new < y_int+1:
                    if room.is_position_valid(new_posit):
                        self.set_robot_position(new_posit)
            else:
                node_list.append((x_int,y_int))
                new_posit= posit_now.get_new_position(direct_now, self.speed)
                x_int, y_int= math.floor(new_posit.get_x()), math.floor(new_posit.get_y())
                if not (x_int, y_int) in node_list:
                    if room.is_position_valid(new_posit):
                        self.set_robot_position(new_posit)
            
                new_direct= round(random.uniform(0, 359.99), 2)
                self.set_robot_direction(new_direct)
                
        
#    
# test_robot_movement(FaultyRobot, EmptyRoom)

from statistics import mean
# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    ## coded ##
    # you can uncomment commented lines to see anim
    # anim was given I didn't code it
    clock= []
#    anim = ps3_visualize.RobotVisualization(num_robots, width, height,False, 0.2)
    for trial in range(num_trials):
        room= EmptyRoom(width, height, dirt_amount)
        phase= 0
        while room.get_num_cleaned_tiles()/ room.get_num_tiles() < min_coverage:
#            robots= []
            for num in range(num_robots):
                robot= robot_type(room, speed, capacity)
                robot.update_position_and_clean()
#                robots.append(robot)
#            anim.update(room, robots)
            phase += 1  
#        anim.done()
        clock.append(phase)
    return mean(clock)

## Experiments

# different experiments

#print ('avg for 50 trial  5x5 1 robot frac= 1: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
#print ('avg for 50 trial 10x10 1 robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, StandardRobot)))
#print ('avg time steps for 10x10 1 robot frac= 0.9: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
#print ('avg time steps for 20x20 1 robot frac= 0.5: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
#print ('avg time steps for 20x20 3 robot frac= 0.5: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))


# For one robot, 50 trial for each, room size and type of robot is different

#print ('avg for 50 trial 10x30 standard robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 10, 30, 3, 0.8, 50, StandardRobot)))
#print ('avg for 50 trial 10x30 faulty robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 10, 30, 3, 0.8, 50, FaultyRobot)))
#print ('avg for 50 trial 20x15 standard robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 20, 15, 3, 0.8, 50, StandardRobot)))
#print ('avg for 50 trial 20x15 faulty robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 20, 15, 3, 0.8, 50, FaultyRobot)))
#print ('avg for 50 trial 50x6 standard robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 50, 6, 3, 0.8, 50, StandardRobot)))
#print ('avg for 50 trial 50x6 faulty robot frac= 0.8: ' + str(run_simulation(1, 1.0, 1, 50, 6, 3, 0.8, 50, FaultyRobot)))

import matplotlib.pyplot as plt

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    plt.figure(0)
    plt.plot(num_robot_range, times1)
    plt.plot(num_robot_range, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'FaultyRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('images/diff_numRobot.png')

    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    plt.figure(1)
    plt.plot(aspect_ratios, times1)
    plt.plot(aspect_ratios, times2)
    plt.title(title)
    plt.legend(('StandardRobot', 'FaultyRobot'))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('images/diff_roomSize.png')


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio (width/height)', 'Time / steps')
