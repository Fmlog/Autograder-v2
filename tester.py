from autograderstable.autograder.autograder import AutograderPaths, Grader
import sys

from autograderstable.autograder import guide
# current_dir = 'media/upload/9BICLG'
# guide.main(AutograderPaths(current_dir))

grader = Grader(sys.argv[1]).run(sys.argv[2])

