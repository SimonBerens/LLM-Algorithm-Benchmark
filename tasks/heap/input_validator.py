n = int(input())

l = 0
for _ in range(n):
    t, *rest = map(int, input().split())
    if t == 0:
        l += 1
        assert len(rest) == 1
    elif t == 1:
        l -= 1
        assert l > 0
        assert len(rest) == 0
    else:
        assert l > 0
        assert len(rest) == 0
