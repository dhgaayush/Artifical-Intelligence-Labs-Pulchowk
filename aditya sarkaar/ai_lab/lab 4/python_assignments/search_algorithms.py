"""
Lab 4: Informed and Uninformed Search Strategies
Romanian Map — Route Finding from Arad to Bucharest

Program by: Chandan Kumar Shah
Roll No: 080BCT023
"""

# ═══════════════════════════════════════════════════════════════
# ROMANIAN MAP (from AIMA — Russell & Norvig)
# ═══════════════════════════════════════════════════════════════

graph = {
    'Arad':          {'Zerind': 75,  'Sibiu': 140,  'Timisoara': 118},
    'Zerind':        {'Arad': 75,    'Oradea': 71},
    'Oradea':        {'Zerind': 71,  'Sibiu': 151},
    'Sibiu':         {'Arad': 140,   'Oradea': 151, 'Fagaras': 99, 'RimnicuVilcea': 80},
    'Timisoara':     {'Arad': 118,   'Lugoj': 111},
    'Lugoj':         {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia':       {'Lugoj': 70,   'Drobeta': 75},
    'Drobeta':       {'Mehadia': 75, 'Craiova': 120},
    'Craiova':       {'Drobeta': 120, 'RimnicuVilcea': 146, 'Pitesti': 138},
    'RimnicuVilcea': {'Sibiu': 80,   'Craiova': 146, 'Pitesti': 97},
    'Fagaras':       {'Sibiu': 99,   'Bucharest': 211},
    'Pitesti':       {'RimnicuVilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest':     {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu':       {'Bucharest': 90},
    'Urziceni':      {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova':       {'Urziceni': 98, 'Eforie': 86},
    'Eforie':        {'Hirsova': 86},
    'Vaslui':        {'Urziceni': 142, 'Iasi': 92},
    'Iasi':          {'Vaslui': 92,   'Neamt': 87},
    'Neamt':         {'Iasi': 87}
}

# Straight-line distance to Bucharest (heuristic)
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242,
    'Eforie': 161, 'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151,
    'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 100, 'RimnicuVilcea': 193, 'Sibiu': 253,
    'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

START = 'Arad'
GOAL = 'Bucharest'


# ═══════════════════════════════════════════════════════════════
# 1. BREADTH-FIRST SEARCH (BFS)
# ═══════════════════════════════════════════════════════════════

def bfs(graph, start, goal):
    """BFS: Explores all nodes at depth d before depth d+1.
    Finds the shortest path in terms of number of hops."""
    visited = set()
    queue = [(start, [start])]
    visited.add(start)
    exploration_order = []

    while queue:
        node, path = queue.pop(0)
        exploration_order.append(node)

        if node == goal:
            return path, exploration_order

        for neighbor in sorted(graph[node].keys()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, exploration_order


# ═══════════════════════════════════════════════════════════════
# 2. UNIFORM-COST SEARCH (UCS)
# ═══════════════════════════════════════════════════════════════

import heapq

def ucs(graph, start, goal):
    """UCS: Expands the node with the lowest path cost g(n).
    Finds the cheapest path (optimal for non-negative edge costs)."""
    visited = set()
    pq = [(0, start, [start])]
    exploration_order = []

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)
        exploration_order.append(node)

        if node == goal:
            return path, cost, exploration_order

        for neighbor, edge_cost in sorted(graph[node].items()):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))

    return None, float('inf'), exploration_order


# ═══════════════════════════════════════════════════════════════
# 3. DEPTH-FIRST SEARCH (DFS)
# ═══════════════════════════════════════════════════════════════

def dfs(graph, start, goal):
    """DFS: Explores as deep as possible before backtracking.
    Does NOT guarantee optimal or shortest path."""
    visited = set()
    stack = [(start, [start])]
    exploration_order = []

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue
        visited.add(node)
        exploration_order.append(node)

        if node == goal:
            return path, exploration_order

        # Push neighbors in reverse alphabetical order so
        # alphabetically first neighbor is explored first
        for neighbor in sorted(graph[node].keys(), reverse=True):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None, exploration_order


# ═══════════════════════════════════════════════════════════════
# 4. ITERATIVE-DEEPENING DFS (IDDFS)
# ═══════════════════════════════════════════════════════════════

def dls(graph, node, goal, depth, visited, path):
    """Depth-Limited Search: DFS with a depth limit."""
    if depth == 0 and node == goal:
        return True, path
    if depth > 0:
        for neighbor in sorted(graph[node].keys()):
            if neighbor not in visited:
                visited.add(neighbor)
                found, result = dls(graph, neighbor, goal, depth - 1,
                                    visited, path + [neighbor])
                if found:
                    return True, result
                visited.discard(neighbor)
    return False, None


def iddfs(graph, start, goal, max_depth=20):
    """IDDFS: Repeatedly applies DLS with increasing depth limits.
    Combines BFS's completeness with DFS's memory efficiency."""
    exploration_order = []

    for depth in range(max_depth + 1):
        visited = {start}
        found, path = dls(graph, start, goal, depth, visited, [start])
        exploration_order.append(f"Depth {depth}: visited {sorted(visited)}")

        if found:
            return path, depth, exploration_order

    return None, -1, exploration_order


# ═══════════════════════════════════════════════════════════════
# 5. GREEDY BEST-FIRST SEARCH
# ═══════════════════════════════════════════════════════════════

def greedy_best_first(graph, start, goal, heuristic):
    """Greedy Best-First: Expands the node with the lowest heuristic h(n).
    Fast but does NOT guarantee optimal path."""
    visited = set()
    # (heuristic, node, path)
    pq = [(heuristic[start], start, [start])]
    exploration_order = []

    while pq:
        h, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)
        exploration_order.append(node)

        if node == goal:
            # Calculate path cost
            cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, cost, exploration_order

        for neighbor in sorted(graph[node].keys()):
            if neighbor not in visited:
                heapq.heappush(pq, (heuristic[neighbor], neighbor, path + [neighbor]))

    return None, float('inf'), exploration_order


# ═══════════════════════════════════════════════════════════════
# 6. A* SEARCH
# ═══════════════════════════════════════════════════════════════

def a_star(graph, start, goal, heuristic):
    """A*: Expands node with lowest f(n) = g(n) + h(n).
    Optimal when heuristic is admissible (never overestimates)."""
    visited = set()
    # (f_score, g_score, node, path)
    pq = [(heuristic[start], 0, start, [start])]
    exploration_order = []

    while pq:
        f, g, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)
        exploration_order.append(node)

        if node == goal:
            return path, g, exploration_order

        for neighbor, edge_cost in sorted(graph[node].items()):
            if neighbor not in visited:
                new_g = g + edge_cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float('inf'), exploration_order


# ═══════════════════════════════════════════════════════════════
# HELPER: Calculate path cost
# ═══════════════════════════════════════════════════════════════

def path_cost(graph, path):
    return sum(graph[path[i]][path[i+1]] for i in range(len(path) - 1))


# ═══════════════════════════════════════════════════════════════
# MAIN — Run all algorithms
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("ROMANIAN MAP — ROUTE FINDING: ARAD -> BUCHAREST")
    print("Lab 4: Informed and Uninformed Search Strategies")
    print("=" * 60)
    print("Program by: Chandan Kumar Shah")
    print("Roll No: 080BCT023\n")

    # ── 1. BFS ─────────────────────────────────────────────
    print("=" * 60)
    print("1. BREADTH-FIRST SEARCH (BFS)")
    print("=" * 60)
    bfs_path, bfs_explored = bfs(graph, START, GOAL)
    bfs_cost = path_cost(graph, bfs_path)
    print(f"Path Found: {' -> '.join(bfs_path)}")
    print(f"Path Cost:  {bfs_cost}")
    print(f"Hops:       {len(bfs_path) - 1}")
    print(f"Nodes Explored: {bfs_explored}")
    print()

    # ── 2. UCS ─────────────────────────────────────────────
    print("=" * 60)
    print("2. UNIFORM-COST SEARCH (UCS)")
    print("=" * 60)
    ucs_path, ucs_cost, ucs_explored = ucs(graph, START, GOAL)
    print(f"Path Found: {' -> '.join(ucs_path)}")
    print(f"Path Cost:  {ucs_cost}")
    print(f"Hops:       {len(ucs_path) - 1}")
    print(f"Nodes Explored: {ucs_explored}")
    print()

    # ── 3. DFS ─────────────────────────────────────────────
    print("=" * 60)
    print("3. DEPTH-FIRST SEARCH (DFS)")
    print("=" * 60)
    dfs_path, dfs_explored = dfs(graph, START, GOAL)
    dfs_cost = path_cost(graph, dfs_path)
    print(f"Path Found: {' -> '.join(dfs_path)}")
    print(f"Path Cost:  {dfs_cost}")
    print(f"Hops:       {len(dfs_path) - 1}")
    print(f"Nodes Explored: {dfs_explored}")
    print()

    # ── 4. IDDFS ──────────────────────────────────────────
    print("=" * 60)
    print("4. ITERATIVE-DEEPENING DFS (IDDFS)")
    print("=" * 60)
    iddfs_path, iddfs_depth, iddfs_explored = iddfs(graph, START, GOAL)
    iddfs_cost = path_cost(graph, iddfs_path)
    print(f"Path Found: {' -> '.join(iddfs_path)}")
    print(f"Path Cost:  {iddfs_cost}")
    print(f"Hops:       {len(iddfs_path) - 1}")
    print(f"Found at Depth: {iddfs_depth}")
    print("Depth-by-depth exploration:")
    for entry in iddfs_explored:
        print(f"  {entry}")
    print()

    # ── 5. Greedy Best-First ──────────────────────────────
    print("=" * 60)
    print("5. GREEDY BEST-FIRST SEARCH")
    print("=" * 60)
    greedy_path, greedy_cost, greedy_explored = greedy_best_first(
        graph, START, GOAL, heuristic)
    print(f"Path Found: {' -> '.join(greedy_path)}")
    print(f"Path Cost:  {greedy_cost}")
    print(f"Hops:       {len(greedy_path) - 1}")
    print(f"Nodes Explored: {greedy_explored}")
    print()

    # ── 6. A* ──────────────────────────────────────────────
    print("=" * 60)
    print("6. A* SEARCH")
    print("=" * 60)
    astar_path, astar_cost, astar_explored = a_star(
        graph, START, GOAL, heuristic)
    print(f"Path Found: {' -> '.join(astar_path)}")
    print(f"Path Cost:  {astar_cost}")
    print(f"Hops:       {len(astar_path) - 1}")
    print(f"Nodes Explored: {astar_explored}")
    print()

    # ── COMPARISON ─────────────────────────────────────────
    print("=" * 60)
    print("COMPARISON OF ALL SEARCH ALGORITHMS")
    print("=" * 60)
    print(f"{'Algorithm':<25} {'Path':<45} {'Cost':<10} {'Hops'}")
    print("-" * 90)
    print(f"{'BFS':<25} {' -> '.join(bfs_path):<45} {bfs_cost:<10} {len(bfs_path)-1}")
    print(f"{'UCS':<25} {' -> '.join(ucs_path):<45} {ucs_cost:<10} {len(ucs_path)-1}")
    print(f"{'DFS':<25} {' -> '.join(dfs_path):<45} {dfs_cost:<10} {len(dfs_path)-1}")
    print(f"{'IDDFS':<25} {' -> '.join(iddfs_path):<45} {iddfs_cost:<10} {len(iddfs_path)-1}")
    print(f"{'Greedy Best-First':<25} {' -> '.join(greedy_path):<45} {greedy_cost:<10} {len(greedy_path)-1}")
    print(f"{'A*':<25} {' -> '.join(astar_path):<45} {astar_cost:<10} {len(astar_path)-1}")
    print("-" * 90)
    print()
    print("Program by: Chandan Kumar Shah")
    print("Roll No: 080BCT023")
