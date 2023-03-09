n, q = map(int, input().split())
for _ in range(q):
    t, u, v = map(int, input().split())
    assert 0 <= u < n
    assert 0 <= v < n
    assert t == 0 or t == 1
