"""
2-Approximation TSP solver using MST and DFS preorder traversal.
"""

import os

from utils import dist, read_tsp, write_solution


def prim_mst(coords):
    """Return parent[] of MST using O(N^2) Prim."""
    n = len(coords)
    verts = sorted(coords.keys())
    idx = {v: i for i, v in enumerate(verts)}
    rev = {i: v for v, i in idx.items()}
    inmst = [False] * n
    key = [float("inf")] * n
    parent = [-1] * n
    key[0] = 0

    for _ in range(n):
        u = -1
        minval = float("inf")
        for i in range(n):
            if not inmst[i] and key[i] < minval:
                minval = key[i]
                u = i
        if u == -1:
            break
        inmst[u] = True
        pu = coords[rev[u]]
        for v in range(n):
            if not inmst[v]:
                w = dist(pu, coords[rev[v]])
                if w < key[v]:
                    key[v] = w
                    parent[v] = u
    parent_ids = {}
    for i in range(1, n):
        parent_ids[rev[i]] = rev[parent[i]]
    return parent_ids


def build_adj(parent):
    """Build adjacency list from parent dictionary."""
    adj = {}
    for v, p in parent.items():
        adj.setdefault(v, []).append(p)
        adj.setdefault(p, []).append(v)
    return adj


def dfs_preorder(adj, start):
    """Perform DFS preorder traversal and return visiting order."""
    visited = set()
    order = []

    def dfs(u):
        visited.add(u)
        order.append(u)
        for v in adj.get(u, []):
            if v not in visited:
                dfs(v)

    dfs(start)
    return order


def tour_length(order, coords):
    """Compute total length of the tour given visiting order."""
    total = 0
    for i, node in enumerate(order):
        a = coords[node]
        b = coords[order[(i + 1) % len(order)]]
        total += dist(a, b)
    return total


def approx_tsp(args):
    """2-Approximation TSP solver using MST and DFS preorder traversal."""
    coords = read_tsp(args.inst)
    parent = prim_mst(coords)
    adj = build_adj(parent)
    start = min(coords.keys())
    order = dfs_preorder(adj, start)
    length = tour_length(order, coords)
    instance = os.path.splitext(os.path.basename(args.inst))[0]
    write_solution(instance, args, length, order)
