import inspect
from pathlib import Path

from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate

from execution_pipeline.types import Executor

llm = OpenAI()

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

example_prompt = PromptTemplate(input_variables=["python_code", "input_text", "predicted_output"],
                                template="Python code: {python_code}\nInput text: {input_text}\n{predicted_output}")

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Python code: {python_code}\nInput text: {input_text}\n",
    input_variables=["python_code", "input_text"]
)

llm_chain = LLMChain(prompt=prompt, llm=llm)


class PythonOpenAiExecutor(Executor):
    @property
    def name(self) -> str:
        return "llm_executor_python_openai"

    def __init__(self):
        pass

    def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        execution_results = []
        python_code = code_path.read_text()
        for input_path in input_paths:
            input_text = input_path.read_text()
            execution_result = llm_chain.run(python_code=python_code, input_text=input_text)
            execution_results.append(execution_result)
        return execution_results
