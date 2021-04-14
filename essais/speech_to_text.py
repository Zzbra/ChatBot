import fileinput
import sys
import os
from subprocess import Popen, PIPE, STDOUT

p = Popen(['rasa', 'shell'], stdout=PIPE, stdin=PIPE, stderr=PIPE)


# for outline in p.stdout:
#     print(outline.rstrip())
#     outline = p.stdout

# p = os.popen("rasa shell")
for line in fileinput.input():
    # p.stdin.write(line)
    stdout_data = p.communicate(input=line.encode('utf-8'))[0]
    print(stdout_data.decode('utf-8'))
