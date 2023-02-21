import pathlib
import sys

input_validators = pathlib.Path('tasks').glob('*/input_validator.py')

invalid_inputs = []

validator_cnt = 0
input_file_cnt = 0

for input_validator in input_validators:
    validator_cnt += 1
    for input_file in input_validator.parent.joinpath('inputs').iterdir():
        input_file_cnt += 1
        tmp_stdin = sys.stdin
        with open(input_file, 'r') as f:
            sys.stdin = f
            try:
                exec(open(input_validator).read(), {})
            except Exception as e:
                invalid_inputs.append([str(input_file), str(e)])
            sys.stdin = tmp_stdin

print(
    f"Found {validator_cnt} validator{'' if validator_cnt == 1 else 's'} and"
    f" {input_file_cnt} input file{'' if input_file_cnt == 1 else 's'}")
print()

if invalid_inputs:
    print("The following inputs failed validation:")
    print("\n".join(map(lambda x: f"{x[0]} ({x[1]})", invalid_inputs)))
    exit(1)
else:
    print("All inputs valid")
