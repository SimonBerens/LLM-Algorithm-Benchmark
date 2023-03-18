import inspect

examples = [
    {
        "python_code":
            """
            n = int(input())
            print(n ** 2)
            """,
        "input_text":
            """
            10
            """,
        "predicted_output":
            """
            100
            """
    },
    {
        "python_code":
            """
            n = int(input())
            a = list(map(int, input().split()))
            print(" ".join(map(lambda x: n * x, a)))
            """,
        "input_text":
            """
            3
            1 2 3 -15
            """,
        "predicted_output":
            """
            3 6 9 -45
            """
    },
    {
        "python_code":
            """
            s = input()
            print(s[::-1] * 2)
            """,
        "input_text":
            """
            hello world
            """,
        "predicted_output":
            """
            dlrow ollehdlrow olleh
            """
    },
    {
        "python_code":
            """
            a = list(map(int, input().split()))
            print(min(a), max(a))
            print(a.index(a[0]))
            print(a)
            """,
        "input_text":
            """
            10 8 -3 -6 5 8 9 -9 7 -4
            """,
        "predicted_output":
            """
            -9 10
            0
            [10, 8, -3, -6, 5, 8, 9, -9, 7, -4]
            """
    },
]

for example in examples:
    for key in example.keys():
        example[key] = inspect.cleandoc(example[key])
