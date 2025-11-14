#!/usr/bin/env python3
"""Executes the TSP solver based on user-specified algorithm and parameters."""
import argparse
import time

from approx.algo_approx import approx_tsp
from bf.algo_bf import bf_tsp
from ls.algo_ls import ls_tsp


def main():
    """Parse arguments and run TSP solver."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", required=True, help="input .tsp file")
    parser.add_argument(
        "-alg", required=True, choices=["BF", "Approx", "LS"], help="algorithm type"
    )
    parser.add_argument(
        "-time", type=int, default=None, help="cutoff seconds (optional)"
    )
    parser.add_argument("-seed", type=int, default=42, help="random seed (optional)")
    args = parser.parse_args()

    start_t = time.time()
    if args.alg == "BF":
        bf_tsp(args)
    elif args.alg == "Approx":
        approx_tsp(args)
    else:
        ls_tsp(args)
    print(f"Runtime: {time.time()-start_t:.10f}s")


if __name__ == "__main__":
    main()
