input()
a = list(map(int, input().split()))
res = [0]
for num in a:
    res.append(res[-1] + num)
print(res)