m, n = map(int, input().split())

assert 0 <= m <= 4 and n >= 0

if m == 1:
    assert n <= 500
elif m == 2:
    assert n <= 350
elif m == 3:
    assert n <= 6
elif m == 4:
    assert n == 0
