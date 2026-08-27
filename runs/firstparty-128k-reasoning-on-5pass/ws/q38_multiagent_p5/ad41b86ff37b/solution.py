import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    adj = [[] for _ in range(n + 1)]

    idx = 1
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    # Bucket vertices by their original degree using linked lists.
    head = [-1] * (n + 1)
    nxt = [-1] * (n + 1)
    max_deg = 0

    for v in range(1, n + 1):
        d = len(adj[v])
        if d > max_deg:
            max_deg = d
        if d >= 2:
            nxt[v] = head[d]
            head[d] = v

    cnt = [0] * (n + 1)
    max_cnt = 0
    best = 0

    adj_l = adj
    cnt_l = cnt
    head_l = head
    nxt_l = nxt

    # Sweep thresholds d = y + 1 from high to low.
    for d in range(max_deg, 1, -1):
        v = head_l[d]
        if v == -1:
            continue

        while v != -1:
            for u in adj_l[v]:
                cu = cnt_l[u] + 1
                cnt_l[u] = cu
                if cu > max_cnt:
                    max_cnt = cu
            v = nxt_l[v]

        val = 1 + d * max_cnt
        if val > best:
            best = val

    sys.stdout.write(str(n - best) + "\n")

if __name__ == "__main__":
    main()