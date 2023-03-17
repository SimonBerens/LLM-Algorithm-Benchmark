import inspect
from asyncio import gather
from pathlib import Path

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    SystemMessage
)

from execution_pipeline.types import Executor

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

messages = [SystemMessage(
    content="You are a chatbot that predicts the output of python code given input that will be passed into stdin. "
            "Reply with the exact output of the code.")]

htemplate = HumanMessagePromptTemplate.from_template("Python code: {python_code}\nInput text: {input_text}")

for example in examples:
    messages.append(htemplate.format_messages(python_code=example["python_code"], input_text=example["input_text"])[0])
    messages.append(AIMessage(content=example["predicted_output"]))
messages.append(htemplate)


class PythonChatGptExecutor(Executor):

    def __init__(self, model_name):
        self.model_name = model_name
        chat = ChatOpenAI(temperature=0, model_name=model_name)
        self.llm_chain = LLMChain(llm=chat, prompt=ChatPromptTemplate.from_messages(messages))

    @property
    def name(self) -> str:
        return "llm_executor_python_" + self.model_name

    async def execute(self, code_path: Path, input_paths: list[Path]) -> list[str]:
        python_code = code_path.read_text()
        execution_coroutines = []
        for input_path in input_paths:
            input_text = input_path.read_text()
            execution_coroutine = self.llm_chain.arun(python_code=python_code, input_text=input_text)
            execution_coroutines.append(execution_coroutine)
        return list(await gather(*execution_coroutines))
