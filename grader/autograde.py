from .models import Question, File
import importlib
from inspect import getmembers, isfunction


def autograde(id):
    file = File.objects.filter(id=id).first()
    var = str(file.file)
    file_name = var.split(".")[0]

    question = file.question
    all_results = {}
    for x in range(len(question.test_case)):

        # importing the uploaded file
        test_file = importlib.import_module(f'media.{file_name}')

        # getting the function to call
        func = getattr(test_file, question.function)

        # getting the test case
        test = question.test_case[str(x+1)]

        # getting the test results
        test_results = question.test_result[str(x+1)]

        # running the function
        # putting it inside a try and catch. so if there is an error it automatically makes it failed
        try:
            result = func(test)
        except:
            all_results[f"test case {x+1}"] = "failed"

        else:
            if result == test_results[0]:
                all_results[f"test case {x+1}"] = "passed"
            else:
                all_results[f"test case {x+1}"] = "failed"

    return all_results
