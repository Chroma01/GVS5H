import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1]

    costs = [(0, 1) if bit == 48 else (1, 0) for bit in a]

    while len(costs) > 1:
        next_costs = []
        for i in range(0, len(costs), 3):
            children = costs[i:i + 3]
            best0 = best1 = float("inf")

            for mask in range(8):
                ones = 0
                cost = 0
                for j in range(3):
                    value = (mask >> j) & 1
                    ones += value
                    cost += children[j][value]

                if ones >= 2:
                    if cost < best1:
                        best1 = cost
                else:
                    if cost < best0:
                        best0 = cost

            next_costs.append((best0, best1))

        costs = next_costs

    root_zero, root_one = costs[0]
    original_value = 0 if root_zero == 0 else 1
    print(costs[0][1 - original_value])


if __name__ == "__main__":
    solve()