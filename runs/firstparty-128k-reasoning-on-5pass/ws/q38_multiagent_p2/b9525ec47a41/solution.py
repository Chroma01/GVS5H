import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[1]
    MOD = 998244353

    v1 = v2 = v3 = v4 = v5 = v8 = v9 = v10 = v11 = v12 = v13 = v15 = 0
    v9 = 1

    cnt = 0
    for c in s:
        if c == 48:  # '0'
            t1 = v1 + v2 + v3
            t2 = t1 + v9 + v11
            t4 = v4 + v8 + v9 + v12 + v13
            t5 = v5 + v10 + v11 + v15
            t8 = v4 + v8 + v12
            t10 = v5 + v10 + v13 + v15

            v1 = t1
            v2 = t2
            v4 = t4
            v5 = t5
            v8 = t8
            v10 = t10
        else:        # '1'
            t1 = v1 + v2 + v3
            t2 = t1 + v9 + v11
            t3 = t1 + v3
            t4 = v4 + v8 + v9 + v12 + v13
            t5 = v5 + v10 + v11 + v15
            t8 = v4 + v8 + v12
            t10 = v5 + v10 + v13 + v15
            t11 = v9 + v11
            t12 = v4 + v8 + v12 + v12
            t13 = v9 + v13
            t15 = v5 + v10 + v11 + v13 + v15 + v15

            v1 = t1
            v2 = t2
            v3 = t3
            v4 = t4
            v5 = t5
            v8 = t8
            v9 = 0
            v10 = t10
            v11 = t11
            v12 = t12
            v13 = t13
            v15 = t15

        cnt += 1
        if cnt == 32:
            v1 %= MOD
            v2 %= MOD
            v3 %= MOD
            v4 %= MOD
            v5 %= MOD
            v8 %= MOD
            v9 %= MOD
            v10 %= MOD
            v11 %= MOD
            v12 %= MOD
            v13 %= MOD
            v15 %= MOD
            cnt = 0

    ans = (v1 + v3 + v5 + v8 + v9 + v10 + v11 + v12 + v13 + v15) % MOD
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()