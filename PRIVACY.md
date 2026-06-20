# Privacy Policy

_Last updated: 2026-06-20_

This Privacy Policy explains how **Kawaii PC Repair** (the "Software") handles
data. The idea and creative direction for this project belong to **Feris** (the
"Author"); the code was written by the AI assistant **Claude**.

## The short version

**Feris does not collect anything from people using the tool.** There is no
telemetry, no analytics, no tracking, no accounts, and no data of any kind sent
to the Author or to any server controlled by the Author. The Software is not a
service — it is a program that runs entirely on your own computer.

## What data is collected

**None.** The Software does not collect, store, transmit, sell, or share any
personal information or usage data with the Author or with any third party
controlled by the Author.

## How the Software runs

- The Software runs **locally** on your own Windows computer.
- It starts a small web server that listens **only** on `127.0.0.1` (localhost) —
  your own machine. This server is **not** exposed to the internet or your local
  network, and the Author has no access to it.
- The output of the repair commands is shown **only** on the page in your own
  browser and is not sent anywhere.
- The Software does not require an account, login, email, or any registration.

## Outbound network connections

The Software is offline-by-design. The only times it may use the internet are
operations **you** trigger, which contact **Microsoft and other first-party
services directly** (never the Author):

- **Full Diagnostics** runs a connectivity check by pinging a public DNS address
  (`8.8.8.8`) to tell you whether your internet is working. No personal data is
  sent.
- **Repair VC++** downloads the official Microsoft Visual C++ redistributables
  from Microsoft's servers (`https://aka.ms/...`) so it can repair them.
- The web page loads fonts from Google Fonts for its appearance.

These connections go to those third parties under **their** privacy policies, not
the Author's. The Author neither receives nor logs any of this activity. If you
prefer to avoid all outbound connections, simply do not run the modules listed
above and run the tool on an offline machine.

## Local changes the Software makes

The Software runs standard Windows maintenance commands that may modify your
system (for example, deleting temporary files, resetting network settings, or
repairing system files). These actions happen **on your computer only** and are
not reported to anyone. See [TERMS.md](TERMS.md) for details and the disclaimer.

## Children's privacy

The Software does not knowingly collect any information from anyone, including
children.

## Forks and modified versions

This Privacy Policy describes the **original** Software as published by the
Author. Anyone who forks or modifies the Software is solely responsible for the
privacy practices of their own version. The Author is not responsible for data
practices introduced by third parties.

## Changes to this policy

This Privacy Policy may be updated from time to time. Any changes will be posted
in this file.

## Contact

Questions can be directed to Feris via [https://mez.ink/ferisooo](https://mez.ink/ferisooo).

---

_Made with 💖 for Feris._
</content>
