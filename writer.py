from pathlib import Path

import paths
from execution_pipeline.types import TestResult, SubtestResult


def get_key_from_path(path: Path):
    return path.relative_to(paths.tasks_path).as_posix()


def get_json_subtest_result(subtest_result: SubtestResult):
    return {
        "language": subtest_result.language.value,
        "input_text_key": get_key_from_path(subtest_result.input_path),
        "code_file_str_key": get_key_from_path(subtest_result.code_path),
        "llm_executor_name": subtest_result.llm_executor.name,
        "predicted_output": subtest_result.predicted_output,
        "code_output": subtest_result.code_output,
        "correctly_predicted": subtest_result.correctly_predicted
    }


def get_json_test_results(test_results: list[TestResult]):
    res_json = {
        "input_texts": {},
        "code_file_strs": {},
        "task_infos": {},
        "results": []
    }

    for input_path in paths.tasks_path.glob("*/inputs/*"):
        res_json["input_texts"][get_key_from_path(input_path)] = input_path.read_text()

    for code_path in paths.tasks_path.glob("*/code/*"):
        res_json["code_file_strs"][get_key_from_path(code_path)] = code_path.read_text()

    for test_result in test_results:
        res_json["task_infos"][get_key_from_path(test_result.path)] = test_result.metadata
        for subtest_result in test_result.subtest_results:
            res_json["results"].append({
                "task_info_key": get_key_from_path(test_result.path),
                **get_json_subtest_result(subtest_result)
            })
    return res_json


