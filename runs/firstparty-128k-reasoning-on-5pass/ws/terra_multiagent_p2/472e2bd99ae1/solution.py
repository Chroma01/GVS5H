import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    k = data[1]

    a = sorted(data[2:2 + n], reverse=True)
    b = sorted(data[2 + n:2 + 2 * n], reverse=True)
    c = sorted(data[2 + 2 * n:2 + 3 * n], reverse=True)

    n2 = n * n

    def value(i, j, l):
        x = a[i]
        y = b[j]
        z = c[l]
        return x * y + y * z + z * x

    initial = value(0, 0, 0)
    heap = [(-initial, 0)]
    visited = {0}

    answer = initial

    for _ in range(k):
        neg_value, code = heapq.heappop(heap)
        answer = -neg_value

        i, rem = divmod(code, n2)
        j, l = divmod(rem, n)

        if i + 1 < n:
            next_code = code + n2
            if next_code not in visited:
                visited.add(next_code)
                heapq.heappush(heap, (-value(i + 1, j, l), next_code))

        if j + 1 < n:
            next_code = code + n
            if next_code not in visited:
                visited.add(next_code)
                heapq.heappush(heap, (-value(i, j + 1, l), next_code))

        if l + 1 < n:
            next_code = code + 1
            if next_code not in visited:
                visited.add(next_code)
                heapq.heappush(heap, (-value(i, j, l + 1), next_code))

    print(answer)


if __name__ == "__main__":
    main()