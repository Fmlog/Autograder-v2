from autograderstable.autograder.autograder import Grader
import sys

grader = Grader(sys.argv[1]).run(sys.argv[2])

