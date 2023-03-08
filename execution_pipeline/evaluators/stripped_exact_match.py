class StrippedExactMatch:
    def __init__(self):
        pass

    def is_valid(self, execution_result: str, llm_output: str):
        return execution_result.strip() == llm_output.strip()
