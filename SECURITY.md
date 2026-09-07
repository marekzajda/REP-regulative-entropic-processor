# Security Policy

REPNet Community Edition is a research-oriented open-source project.

## Supported version

Security and integrity fixes target the current Community Edition release line.

| Version | Supported |
|---|---|
| 1.x | Yes |
| historical/private research branches | Not part of this public repository |

## Reporting a vulnerability

Please do not publish credentials, private datasets, local memory databases, machine-specific state, or other sensitive material in a public issue.

For code-level vulnerabilities that can be discussed publicly, open an issue with a minimal reproduction and avoid including secrets or personal data.

For sensitive reports, use GitHub's private vulnerability reporting feature when available for this repository.

## Public repository boundary

This repository must not contain:

- API tokens or credentials;
- local `.env` files;
- private memory databases;
- unreleased model checkpoints;
- raw forensic research payloads;
- machine-specific automation secrets;
- private research orchestration state.

The `.gitignore` and review policy are designed to keep those classes of data out of Community Edition.
