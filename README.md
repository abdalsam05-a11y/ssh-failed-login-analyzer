# SSH Failed-Login Analyzer

> **Status:** Work in progress — built as a learning project by an undergraduate IT/Cybersecurity student (not yet graduated). Feedback and suggestions are welcome.

A Python script that parses Linux SSH authentication logs (`auth.log`), counts failed login attempts per IP and per username, and flags IPs that look like brute-force attempts.

## What it does

- Parses `Failed password` events from `auth.log`, handling both the legacy `sshd` and modern `sshd-session` log formats.
- Counts failed attempts per source IP (IPv4 and IPv6) and per targeted username.
- Flags any IP with 3 or more failed attempts as suspicious.

## Why

Built as a hands-on SOC/Blue Team practice project: generate real SSH failed-login traffic, then parse and detect it programmatically instead of manually grepping logs.

## Usage

\`\`\`bash
python3 analyzer.py samples/kali_attack_sample.log
\`\`\`

## Example output

\`\`\`
Failed attempts per IP:
  192.168.241.129: 10

Failed attempts per username:
  msfadmin: 10

Suspicious IPs (>= 3 failed attempts):
  [ALERT] 192.168.241.129 with 10 failed attempts
\`\`\`

## How the sample log was generated

1. Set up a two-VM lab: Kali Linux (attacker) and Metasploitable 2 (target), both on the same host-only network.
2. Used Hydra from Kali to run an SSH brute-force attempt against Metasploitable with a small custom wordlist of wrong passwords.
3. Copied the relevant entries from Metasploitable's `/var/log/auth.log` into `samples/kali_attack_sample.log` for reproducible testing.

An earlier version of this project used `samples/auth_sample.log`, generated from local SSH attempts on `127.0.0.1`/`::1` on a single machine — kept in the repo for reference.

## Screenshots

See `screenshots/` for the setup process and the script detecting a brute-force pattern.

## Next steps (v2 ideas)

- Treat `::1` and `127.0.0.1` as the same host (merge loopback addresses).
- Add a time-window check (e.g. 5 attempts within 60 seconds) instead of a flat count.
- Export results to CSV/JSON for use in a SIEM pipeline.
- Package as a CLI tool with configurable threshold.
