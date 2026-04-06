# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
responsibly.

**Do not open a public issue.** Instead, email the maintainers directly or use
GitHub's [private vulnerability reporting](../../security/advisories/new) feature.

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Scope

This project sends prompts to external LLM APIs (OpenAI by default). Security
considerations include:

- **API key exposure** — Keys are read from environment variables and never
  logged or stored in artifacts. Do not commit `.env` files.
- **Prompt injection** — The AI orchestration layer uses a fixed system prompt
  with constitution-level constraints. User input is passed as the user message,
  not injected into the system prompt.
- **Output validation** — All AI responses are scanned for executable code
  before being written to disk. This is a defense-in-depth measure, not a
  guarantee against all forms of prompt injection.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
