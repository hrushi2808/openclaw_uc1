# OpenClaw Setup

This project runs on top of **OpenClaw**, a local AI agent gateway that acts as the LLM and tool-orchestration layer. OpenClaw itself is not part of this repository — it must be installed and running separately before the MCP servers here (`audio_mcp_server.py`, `email_mcp_server.py`) can be used.

This document covers only what's needed to get OpenClaw running for this project. For anything beyond that, see the official docs: https://docs.openclaw.ai

---

## What OpenClaw Does Here

OpenClaw runs a local **Gateway** (default `localhost:18789`) that:

- Hosts the LLM the agent uses to reason and respond
- Exposes interfaces for interacting with the agent (browser dashboard or terminal)
- Loads and calls the MCP servers in this repo as tools, based on what the user asks for

Nothing in this repo talks to an LLM directly — every request goes through the OpenClaw Gateway first.

---

## 1. Install OpenClaw

Follow the official install guide for your platform:
https://docs.openclaw.ai/install

Verify it installed correctly:

```bash
openclaw --version
```

---

## 2. Run Onboarding (with Background Service)

```bash
openclaw onboard --install-daemon
```

This does two things in one step:

1. Runs the guided onboarding wizard — verifies model/provider access with a live completion, and generates your Gateway auth token.
2. Installs the Gateway as a background service, so it starts automatically after login instead of needing to be started manually every time.

On Windows, `--install-daemon` first tries to create a Scheduled Task, falling back to a Startup folder entry for the current user if that's not permitted.

If you've already completed onboarding and only want to add the background service afterward:

```bash
openclaw gateway install
```

---

## 3. Register the MCP Servers (CLI)

Register each MCP server with a single command — no manual config file editing required:

```bash
openclaw mcp set audio '{"command":"python","args":["path/to/openclaw_uc1/audio_mcp_server.py"]}'
openclaw mcp set email '{"command":"python","args":["path/to/openclaw_uc1/email_mcp_server.py"]}'
```

Replace `path/to/openclaw_uc1/` with the actual path to this project on your machine.

Verify both are registered:

```bash
openclaw mcp list
openclaw mcp show audio
openclaw mcp show email
```

Restart the Gateway for changes to take effect (see step 5).

---

## 4. Model Configuration

This project uses a cloud-hosted Ollama model as the agent's primary model, not a local one. This avoids memory/context-window issues that come up with locally-hosted models on machines without a dedicated GPU.

The model is chosen once during onboarding, but can be changed at any time afterward with:

```bash
openclaw models set ollama/kimi-k2.5:cloud
openclaw models status
```

`models status` confirms which model is currently active.

Any non-reasoning cloud model works — reasoning-enabled models can leak internal "thinking" text into responses when accessed through certain integrations, so a non-reasoning model is recommended here.

---

## 5. Start / Restart the Gateway

If installed as a background service (recommended, via step 2):

```bash
openclaw gateway restart
```

To run it in the foreground for a single terminal session instead:

```bash
openclaw gateway run
```

---

## 6. Confirm It's Working

Two interfaces are available:

**Browser dashboard (Control UI):**
```bash
openclaw dashboard
```

**Terminal chat (TUI):**
```bash
openclaw tui
```

Send a test message in either. If it responds, the Gateway, model, and MCP servers are wired up correctly and you're ready to use the project as described in the main [README.md](./README.md).

---

## Notes

- **Auth token:** Your Gateway token is generated during onboarding and stored in `openclaw.json`. Keep it private — it grants full access to your agent.
- **Local only:** By default, the Gateway binds to `localhost`, meaning only your machine can reach it. Don't expose it externally without understanding the security implications — see OpenClaw's own docs on Gateway security.
- **Troubleshooting OpenClaw itself** (installation issues, model errors, Gateway not starting) is outside the scope of this repo — refer to https://docs.openclaw.ai or their Discord for support.
