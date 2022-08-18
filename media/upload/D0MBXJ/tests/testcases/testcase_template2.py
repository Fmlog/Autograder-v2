# student_submission is provided by autograder, represents student's module, and can be used freely
# PASS(), RESULT(res), FAIL(), and CHECK_STDOUT() are also provided by autograder and can be used freely


def main():
    # You can call any function from student's file like this.
    # It can have any arguments and return values -- use it like any other function.
    result = student_submission.twoSum([3,2,4], 6) # nums = [3,2,4], target = 6

    SOME_EXPECTED_RESULT = [1,2]
    if result == SOME_EXPECTED_RESULT:
        PASS()
    else:
        FAIL()

main()
