# Australia Map Colouring Problem (Constraint Satisfaction)
# Regions: WA, NT, Q, NSW, V, SA, T
# Domain : {red, green, blue}
# Constraint: adjacent regions must have different colours.

from itertools import product

REGIONS = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
COLOURS = ["red", "green", "blue"]

# Adjacency list (undirected).
ADJACENT = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "Q", "SA"],
    "Q": ["NT", "NSW", "SA"],
    "NSW": ["Q", "V", "SA"],
    "V": ["NSW", "SA"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "T": [],  # Tasmania has no mainland neighbours.
}


def is_valid(assignment):
    """Check whether every adjacency constraint is satisfied."""
    for region, colour in assignment.items():
        for neighbour in ADJACENT[region]:
            if assignment.get(neighbour) == colour:
                return False
    return True


def solve():
    """Find the first valid colouring by brute-force search."""
    for combo in product(COLOURS, repeat=len(REGIONS)):
        assignment = dict(zip(REGIONS, combo))
        if is_valid(assignment):
            return assignment
    return None


if __name__ == "__main__":
    solution = solve()
    if solution:
        print("Australia Map Colouring Solution:")
        for region in REGIONS:
            print(f"  {region} = {solution[region]}")
    else:
        print("No valid colouring found.")
