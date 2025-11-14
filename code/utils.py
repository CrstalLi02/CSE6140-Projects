"""
Utility functions for TSP solver.
"""

import math
import os


def write_solution(instance, args, length, order):
    """Write solution to output file in algorithm-specific subdirectory."""
    # Determine output filename and subdirectory based on algorithm
    if args.alg == "BF":
        outname = f"{instance}_BF_{args.time}.sol"
        subdir = "BF"
    elif args.alg == "Approx":
        outname = f"{instance}_Approx_{args.seed}.sol"
        subdir = "Approx"
    else:  # LS
        outname = f"{instance}_LS_{args.time}_{args.seed}.sol"
        subdir = "LS"
    
    # Create algorithm-specific output directory
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output", subdir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Write solution file
    outpath = os.path.join(output_dir, outname)
    with open(outpath, "w", encoding="utf8") as f:
        f.write(f"{length}\n")
        f.write(",".join(str(v) for v in order))
    print(f"Solution written to {outpath}")


def read_tsp(filename):
    """
    Read TSP instance from a .tsp file in TSPLIB format.
    Returns a dictionary mapping vertex ID to (x, y) coordinates.
    """
    coords = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("NODE_COORD_SECTION"):
                break
        for line in f:
            line = line.strip()
            if line == "EOF" or line == "":
                break
            parts = line.split()
            if len(parts) >= 3:
                vid = int(parts[0])
                x, y = float(parts[1]), float(parts[2])
                coords[vid] = (x, y)
    return coords


def dist(p1, p2):
    """Euclidean distance rounded to nearest integer."""
    return round(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))
