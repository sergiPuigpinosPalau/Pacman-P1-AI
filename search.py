# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from node import Node
import sys

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return blindGraphSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    return blindGraphSearch(problem,util.Queue())


def blindGraphSearch(problem, fringe):
    """Search the shallowest nodes in the search tree first."""
    #Similar to blindTreeSearch but this one checks wether the current state has already been expanded previously
    expand = {}
    fringe.push(Node(problem.getStartState()))
    while True:
        if fringe.isEmpty():
            print "It run out of Nodes to expand wich means that there's NO SOLUTION"
            sys.exit(-1)
        n = fringe.pop()
        if problem.isGoalState(n.state):
            return n.total_path()
        if n.state in expand: continue
        expand[n.state] = n
        for state,action,cost in problem.getSuccessors(n.state):
            ns = Node(state,n,action,cost)
            if not ns.state in expand:
                fringe.push(ns)


def uniformCostSearch(problem):
    #garantiza que ha llegado por el camino minimo
    generated = {}
    fringe = util.PriorityQueue()
    n = Node(problem.getStartState())
    fringe.push(n,n.cost)
    generated[n.state] = [n,'F'] #nodo esta en el fringe
    while True:
        if fringe.isEmpty():
            print "It run out of Nodes to expand wich means that there's NO SOLUTION"
            sys.exit(-1)
        n = fringe.pop()
        if problem.isGoalState(n.state):
            return n.total_path()
        #Mirem si l'estat del node actual coincideix amb el d'algun node amb el mateix estat pero que ja haigui sigut expanded 
        #Si es el cas, es salta el node ja que voldra dir que ja havia un node amb el mateix estat i amb menys cost que ha sigut expanded
        if generated[n.state][1] == 'E': continue 

        generated[n.state] = [n,'E'] #nodo en el expanded
        for state,action,cost in problem.getSuccessors(n.state):
            ns = Node(state, n, action, n.cost + cost)
            #Donem sempre per Valida la condicio generated[ns.state][1] == 'F'
            #Ja que en cas de no ser-ho, voldra dir que el node amb el mateix estat que esta al generated, ha sigut expanded previament 
            # i llavors sera 100% segur que aquest tindra menys cost que el que estas comparan actualment ja que el cost del actual == cost del cami que porte fet fins ara (optim) + seu cost
            if (not ns.state in generated) or ns.cost < generated[ns.state][0].cost:
                fringe.push(ns, ns.cost)
                generated[ns.state] = [ns,'F']

#elif generated[ns.state][1] == 'F' and ns.cost < generated[ns.state][0].cost:

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #heuristic(state)
    #UCS + modific
    #garantiza que ha llegado por el camino minimo
    generated = {}
    fringe = util.PriorityQueue()
    n = Node(problem.getStartState())
    fringe.push(n,n.cost)
    generated[n.state] = [n,'F'] #nodo esta en el fringe
    while True:
        if fringe.isEmpty():
            print "It run out of Nodes to expand wich means that there's NO SOLUTION"
            sys.exit(-1)
        n = fringe.pop()
        if problem.isGoalState(n.state):
            return n.total_path()
        #Mirem si l'estat del node actual coincideix amb el d'algun node amb el mateix estat pero que ja haigui sigut expanded 
        #Si es el cas, es salta el node ja que voldra dir que ja havia un node amb el mateix estat i amb menys cost que ha sigut expanded
        if generated[n.state][1] == 'E': continue 
        generated[n.state] = [n,'E'] #nodo en el expanded
        for state,action,cost in problem.getSuccessors(n.state):
            #g(n')=g(n)+c(n,n')
            gNPrima=n.cost + cost    
            ns = Node(state, n, action, gNPrima)
            if not ns.state in generated or ns.cost < generated[ns.state][0].cost:
                #f(n')=max(f(n), g(n') + h(n')) 
                fringe.push(ns, max(n.cost, ns.cost + heuristic(state,problem)))
                generated[ns.state] = [ns,'F']


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


