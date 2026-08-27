import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, M = data[0], data[1]
    P = data[2:]

    def evaluate(x, need_count=False):
        total_cost = 0
        total_count = 0
        for p in P:
            k = (x // p + 1) // 2
            if k:
                total_cost += k * k * p
                if total_cost > M:
                    return total_cost, total_count
                if need_count:
                    total_count += k
        return total_cost, total_count

    low = 0
    high = M + 1

    while high - low > 1:
        mid = (low + high) // 2
        cost, _ = evaluate(mid)
        if cost <= M:
            low = mid
        else:
            high = mid

    cost, count = evaluate(low, True)
    remaining = M - cost
    answer = count + remaining // (low + 1)

    print(answer)

if __name__ == "__main__":
    main()