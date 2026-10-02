import re
import sys

PATTERN = re.compile(
    r"sshd(?:-session)?\[\d+\]: Failed password for (?:invalid user )?(\S+) from (\S+) port \d+"
)

path = sys.argv[1]

with open(path) as f:
    for line in f:
        match = PATTERN.search(line)
        if match:
            user, ip = match.groups()
            print(line.split()[0], user, ip)
