"""
Local Search TSP solver using Simulated Annealing with 2-opt neighborhood.

This module implements a local search heuristic for the Traveling Salesman Problem.
The algorithm uses:
1. Greedy Nearest Neighbor for initial solution construction
2. 2-opt local search for neighborhood exploration
3. Simulated Annealing for accepting worse solutions to escape local optima
"""

import math
import os
import random
import time

from utils import dist, read_tsp, write_solution


def calculate_tour_length(tour, coords):
    """
    Calculate the total length of a tour.
    
    Args:
        tour: List of vertex IDs representing the tour order
        coords: Dictionary mapping vertex ID to (x, y) coordinates
    
    Returns:
        Total tour length (sum of Euclidean distances)
    """
    total = 0
    n = len(tour)
    for i in range(n):
        city1 = coords[tour[i]]
        city2 = coords[tour[(i + 1) % n]]
        total += dist(city1, city2)
    return total


def nearest_neighbor(coords, start_node=None):
    """
    Construct initial tour using Greedy Nearest Neighbor heuristic.
    
    Args:
        coords: Dictionary mapping vertex ID to (x, y) coordinates
        start_node: Starting node (if None, uses first node)
    
    Returns:
        List of vertex IDs representing the tour
    """
    nodes = list(coords.keys())
    if start_node is None:
        start_node = nodes[0]
    
    unvisited = set(nodes)
    tour = [start_node]
    unvisited.remove(start_node)
    
    current = start_node
    while unvisited:
        
        nearest = min(unvisited, key=lambda node: dist(coords[current], coords[node]))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return tour


def two_opt_swap(tour, i, j):
    """
    Perform 2-opt swap: reverse the tour segment between positions i and j.
    
    Args:
        tour: Current tour
        i: Start position of segment to reverse
        j: End position of segment to reverse
    
    Returns:
        New tour with reversed segment
    """
    
    new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
    return new_tour


def calculate_delta(tour, coords, i, j):
    """
    Calculate the change in tour length for a 2-opt swap without creating new tour.
    This is more efficient than recalculating the entire tour length.
    
    Args:
        tour: Current tour
        coords: Coordinates dictionary
        i: Start position
        j: End position
    
    Returns:
        Change in tour length (negative means improvement)
    """
    n = len(tour)
    
   
    old_dist = (dist(coords[tour[i]], coords[tour[(i+1) % n]]) +
                dist(coords[tour[j]], coords[tour[(j+1) % n]]))
    
   
    new_dist = (dist(coords[tour[i]], coords[tour[j]]) +
                dist(coords[tour[(i+1) % n]], coords[tour[(j+1) % n]]))
    
    return new_dist - old_dist


def simulated_annealing_tsp(coords, cutoff_time, seed):
    """
    Solve TSP using Simulated Annealing with 2-opt neighborhood.
    
    Args:
        coords: Dictionary mapping vertex ID to (x, y) coordinates
        cutoff_time: Maximum time allowed in seconds
        seed: Random seed for reproducibility
    
    Returns:
        Tuple of (best_tour, best_length)
    """
    random.seed(seed)
    start_time = time.time()
    
    
    print("Generating initial solution using Nearest Neighbor...")
    current_tour = nearest_neighbor(coords)
    current_length = calculate_tour_length(current_tour, coords)
    
   
    best_tour = current_tour[:]
    best_length = current_length
    
    print(f"Initial solution length: {current_length}")
    
    
    n = len(coords)
    initial_temp = 10000.0
    final_temp = 0.1
    cooling_rate = 0.9995
    
    temperature = initial_temp
    iterations = 0
    improvements = 0
    time_check_interval = 100  
    
    print("Starting Simulated Annealing...")
    
    while temperature > final_temp:
        
        if iterations % time_check_interval == 0:
            elapsed = time.time() - start_time
            if elapsed >= cutoff_time:
                print(f"\nTime limit reached after {elapsed:.2f} seconds")
                break
            
            
            if iterations % 10000 == 0 and iterations > 0:
                print(f"Iteration {iterations:,} | Best: {best_length} | "
                      f"Current: {current_length} | Temp: {temperature:.2f} | "
                      f"Time: {elapsed:.2f}s")
        
        
        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)
        
        if j - i == 1:
            iterations += 1
            continue
        
        
        delta = calculate_delta(current_tour, coords, i, j)
        
        
        if delta < 0:
           
            current_tour = two_opt_swap(current_tour, i, j)
            current_length += delta
            improvements += 1
            
            
            if current_length < best_length:
                best_tour = current_tour[:]
                best_length = current_length
        else:
            
            acceptance_prob = math.exp(-delta / temperature)
            if random.random() < acceptance_prob:
                current_tour = two_opt_swap(current_tour, i, j)
                current_length += delta
        
        
        temperature *= cooling_rate
        iterations += 1
    
    elapsed = time.time() - start_time
    print(f"\nSimulated Annealing completed:")
    print(f"  Total iterations: {iterations:,}")
    print(f"  Improvements found: {improvements:,}")
    print(f"  Initial length: {calculate_tour_length(nearest_neighbor(coords), coords)}")
    print(f"  Best length found: {best_length}")
    print(f"  Improvement: {((calculate_tour_length(nearest_neighbor(coords), coords) - best_length) / calculate_tour_length(nearest_neighbor(coords), coords) * 100):.2f}%")
    print(f"  Total time: {elapsed:.2f}s")
    
    return best_tour, best_length


def ls_tsp(args):
    """
    Main entry point for Local Search TSP solver.
    
    Args:
        args: Command-line arguments containing:
            - inst: Path to TSP instance file
            - time: Cutoff time in seconds
            - seed: Random seed for reproducibility
    """
   
    coords = read_tsp(args.inst)
    print(f"Loaded {len(coords)} cities from {args.inst}")
    
    
    best_tour, best_length = simulated_annealing_tsp(coords, args.time, args.seed)
    
   
    instance = os.path.splitext(os.path.basename(args.inst))[0]
    write_solution(instance, args, best_length, best_tour)
