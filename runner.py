from grader_core.autograder.autograder import Grader
import sys

# Running the grader on the file that is passed in as the second argument.
grader = Grader(sys.argv[1]).run(sys.argv[2])

