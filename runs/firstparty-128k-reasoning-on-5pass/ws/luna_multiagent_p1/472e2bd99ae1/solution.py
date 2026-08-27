import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k_limit = data[0], data[1]

    a = data[2:2 + n]
    b = data[2 + n:2 + 2 * n]
    c = data[2 + 2 * n:2 + 3 * n]

    a.sort(reverse=True)
    b.sort(reverse=True)
    c.sort(reverse=True)

    n2 = n * n

    def value(i, j, k):
        return a[i] * b[j] + b[j] * c[k] + c[k] * a[i]

    start_value = value(0, 0, 0)
    heap = [(-start_value, 0)]
    visited = {0}

    answer = start_value

    for _ in range(k_limit):
        neg_value, state = heapq.heappop(heap)
        answer = -neg_value

        i = state // n2
        rem = state - i * n2
        j = rem // n
        l = rem - j * n

        if i + 1 < n:
            nxt = state + n2
            if nxt not in visited:
                visited.add(nxt)
                heapq.heappush(heap, (-value(i + 1, j, l), nxt))

        if j + 1 < n:
            nxt = state + n
            if nxt not in visited:
                visited.add(nxt)
                heapq.heappush(heap, (-value(i, j + 1, l), nxt))

        if l + 1 < n:
            nxt = state + 1
            if nxt not in visited:
                visited.add(nxt)
                heapq.heappush(heap, (-value(i, j, l + 1), nxt))

    print(answer)


if __name__ == "__main__":
    main()