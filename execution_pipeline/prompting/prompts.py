from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema import SystemMessage, AIMessage

from execution_pipeline.prompting import few_shot_examples

zero_shot_template = PromptTemplate(input_variables=["python_code", "input_text"],
                                    template="Python code: {python_code}\nInput text: {input_text}")

example_prompt = PromptTemplate(input_variables=["python_code", "input_text", "predicted_output"],
                                template="Python code: {python_code}\nInput text: {input_text}\n{predicted_output}")

few_shot_template = FewShotPromptTemplate(
    examples=few_shot_examples.examples,
    example_prompt=example_prompt,
    suffix="Python code: {python_code}\nInput text: {input_text}\n",
    input_variables=["python_code", "input_text"]
)

few_shot_messages = [SystemMessage(
    content="You are a chatbot that predicts the output of python code given input that will be passed into stdin. "
            "Reply with the exact output of the code.")]

htemplate = HumanMessagePromptTemplate.from_template("Python code: {python_code}\nInput text: {input_text}")

for example in few_shot_examples.examples:
    few_shot_messages.append(
        htemplate.format_messages(python_code=example["python_code"], input_text=example["input_text"])[0])
    few_shot_messages.append(AIMessage(content=example["predicted_output"]))
few_shot_messages.append(htemplate)

zero_shot_messages = [few_shot_messages[0], few_shot_messages[-1]]
