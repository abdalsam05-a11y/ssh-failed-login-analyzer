import re
import sys
from collections import Counter

PATTERN = re.compile(
    r"sshd(?:-session)?\[\d+\]: Failed password for (?:invalid user )?(\S+) from (\S+) port \d+"
)

THRESHOLD = 3

path = sys.argv[1]
by_ip = Counter()
by_user = Counter()

with open(path) as f:
    for line in f:
        match = PATTERN.search(line)
        if match:
            user, ip = match.groups()
            by_ip[ip] += 1
            by_user[user] += 1

print("Failed attempts per IP:")
for ip, count in by_ip.most_common():
    print(f"  {ip}: {count}")

print("\nFailed attempts per username:")
for user, count in by_user.most_common():
    print(f"  {user}: {count}")

print(f"\nSuspicious IPs (>= {THRESHOLD} failed attempts):")
suspicious = [ip for ip, count in by_ip.items() if count >= THRESHOLD]
if suspicious:
    for ip in suspicious:
        print(f"  [ALERT] {ip} with {by_ip[ip]} failed attempts")
else:
    print("  None")
