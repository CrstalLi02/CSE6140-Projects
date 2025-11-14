import itertools
import math
import os
import time

from utils import dist, read_tsp, write_solution


def calculate_tour_distance(tour, coords):
    total_distance = 0
    n = len(tour)
    
    for i in range(n):
        city1 = coords[tour[i]]
        city2 = coords[tour[(i + 1) % n]]
        total_distance += dist(city1, city2)
    
    return total_distance


def brute_force_tsp(coords, cutoff_time):
    city_ids = sorted(coords.keys())
    n = len(city_ids)
    
    first_city = city_ids[0]
    remaining_cities = city_ids[1:]
    
    best_tour = None
    best_distance = float('inf')
    total_permutations = 0
    permutations_to_check = math.factorial(n - 1)
    completed = False
    
    start_time = time.time()

    for perm in itertools.permutations(remaining_cities):
        elapsed_time = time.time() - start_time
        if elapsed_time >= cutoff_time:
            print(f"\nTime cutoff reached after {elapsed_time:.2f} seconds")
            print(f"Checked {total_permutations:,} / {permutations_to_check:,} permutations")
            break
        
        tour = [first_city] + list(perm)

        distance = calculate_tour_distance(tour, coords)
        
        if distance < best_distance:
            best_distance = distance
            best_tour = tour
        
        total_permutations += 1
        
        if total_permutations % 10000 == 0:
            print(f"Progress: {total_permutations:,} permutations | "
                  f"Best: {best_distance} | "
                  f"Time: {elapsed_time:.2f}s")
    else:
        completed = True
        elapsed_time = time.time() - start_time
        print(f"\nCompleted all {total_permutations:,} permutations in {elapsed_time:.2f} seconds")
    
    print(f"Best solution found: {best_distance}")
    
    return best_tour, best_distance, completed


def bf_tsp(args):    

    coords = read_tsp(args.inst)
    print(f"Successfully loaded {len(coords)} cities from {args.inst}\n")
    
    best_tour, best_distance, completed = brute_force_tsp(coords, args.time)

    if best_tour is None:
        print("Error: No solution found within time limit")
        return

    instance = os.path.splitext(os.path.basename(args.inst))[0]
    write_solution(instance, args, best_distance, best_tour)
