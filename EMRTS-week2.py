# 4-gallon project
from collections import deque

def water_jug_bfs():
    visited = set()
    queue = deque()

    # Each state is represented as (5-gallon, 3-gallon, steps)
    queue.append((0, 0, []))
    solutions = []

    while queue:
        jug5, jug3, steps = queue.popleft()

        if jug5 == 4:
            solutions.append(steps)
            print("Solution found in", len(steps), "steps:")
            for i, step in enumerate(steps, 1):
                print(f"{i}. {step}")
            print("-" * 30)

        if (jug5, jug3) in visited:
            continue
        visited.add((jug5, jug3))

        possible_moves = [
            (5, jug3, "Fill 5-gallon bucket"),
            (jug5, 3, "Fill 3-gallon bucket"),
            (0, jug3, "Empty 5-gallon bucket"),
            (jug5, 0, "Empty 3-gallon bucket"),
            (jug5 - min(jug5, 3 - jug3), jug3 + min(jug5, 3 - jug3), "Pour 5-gallon into 3-gallon bucket"),
            (jug5 + min(jug3, 5 - jug5), jug3 - min(jug3, 5 - jug5), "Pour 3-gallon into 5-gallon bucket"),
        ]

        for new5, new3, action in possible_moves:
            if (new5, new3) not in visited:
                queue.append((new5, new3, steps + [action]))

    print(f"Total solutions found: {len(solutions)}")

# Run it
water_jug_bfs()
