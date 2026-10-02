# SSH Failed-Login Analyzer

> **Status:** Work in progress — built as a learning project by an undergraduate IT/Cybersecurity student (not yet graduated). Feedback and suggestions are welcome.

A Python script that parses Linux SSH authentication logs (`auth.log`), counts failed login attempts per IP and per username, and flags IPs that look like brute-force attempts.

## What it does

- Parses `Failed password` events from `auth.log`, handling both the legacy `sshd` and modern `sshd-session` log formats.
- Counts failed attempts per source IP (IPv4 and IPv6) and per targeted username.
- Flags any IP with 3 or more failed attempts as suspicious.

## Why

Built as a hands-on SOC/Blue Team practice project: generate real SSH failed-login traffic on a Kali Linux VM, then parse and detect it programmatically instead of manually grepping logs.

## Usage

\`\`\`bash
python3 analyzer.py samples/auth_sample.log
\`\`\`

## Example output

\`\`\`
Failed attempts per IP:
  127.0.0.1: 6
  ::1: 2

Failed attempts per username:
  user2: 2
  user1: 2
  admin: 1
  root: 1
  test: 1
  guest: 1

Suspicious IPs (>= 3 failed attempts):
  [ALERT] 127.0.0.1 with 6 failed attempts
\`\`\`

## How the sample log was generated

1. Installed and enabled \`rsyslog\` and \`openssh-server\` on Kali Linux (not present by default).
2. Ran several SSH login attempts with wrong passwords against \`localhost\`/\`127.0.0.1\`, using valid and invalid usernames.
3. Copied \`/var/log/auth.log\` into \`samples/auth_sample.log\` for reproducible testing.

## Screenshots

See \`screenshots/\` for the setup process and the script detecting a brute-force pattern.

## Next steps (v2 ideas)

- Treat \`::1\` and \`127.0.0.1\` as the same host (merge loopback addresses).
- Add a time-window check (e.g. 5 attempts within 60 seconds) instead of a flat count.
- Export results to CSV/JSON for use in a SIEM pipeline.
- Package as a CLI tool with configurable threshold.
