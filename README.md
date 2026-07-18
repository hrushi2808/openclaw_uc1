# Meeting Operations Assistant with OpenClaw

An automated system for processing meeting audio, generating transcripts, and communicating with participants. Uses **OpenClaw AI** with MCP (Model Context Protocol) servers for intelligent meeting operations.

## Architecture

```
OpenClaw AI (localhost:18789)
    ↓
MCP Servers (Tool Layer)
    ├── Audio MCP Server (Whisper Transcription)
    └── Email MCP Server (Gmail Communications)
    ↓
Data & Services
    ├── Audio Files Processing
    ├── Participant Database
    └── Email System
```

## Features

- **OpenClaw AI Integration** — Intelligent meeting assistant powered by OpenClaw
- **Audio Transcription** — Automatically transcribe meeting audio files (MP3, WAV, M4A, OGG, FLAC) using OpenAI Whisper
- **Email Communications** — Send automated follow-up emails to meeting participants via Gmail
- **Participant Management** — Centralized participant contact information
- **MCP Servers** — Modular architecture using FastMCP for seamless OpenClaw integration

## Project Structure

```
openclaw_uc1/
├── audio_mcp_server.py          # MCP server for audio transcription
├── email_mcp_server.py          # MCP server for email communications
├── participants.json            # Meeting participant information
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (not in repo)
├── audios/                     # Input audio files
├── audio_transcripts/          # Generated transcript files
└── README.md
```

## Quick Start

### 1. Clone or Set Up the Project

```bash
cd openclaw_uc1
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
EMAIL_ADDRESS=your-gmail@gmail.com
EMAIL_APP_PASSWORD=your-app-specific-password
```

**To get Gmail App Password:**
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Select "App passwords" (Mail, Windows Computer)
4. Copy the 16-character password to `.env`

### 5. Add Participants

Edit `participants.json` with your meeting participants:

```json
[
  {
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "name": "Jane Smith",
    "email": "jane@example.com"
  }
]
```

### 6. Start OpenClaw (Required)

This project requires a running OpenClaw Gateway on `localhost:18789`.

See [OPENCLAW_SETUP.md](./OPENCLAW_SETUP.md) for full installation and configuration steps.

Quick check that it's already running:

```bash
openclaw status
```

### 7. Start MCP Servers

**Terminal 1 - Audio Server:**
```bash
python audio_mcp_server.py
```

**Terminal 2 - Email Server:**
```bash
python email_mcp_server.py
```

Now the MCP servers are ready for OpenClaw to use!

## Dependencies

| Package | Purpose |
|---------|---------|
| `mcp` | Model Context Protocol framework for FastMCP servers |
| `openai-whisper` | Audio transcription engine |
| `torch` | PyTorch (required by Whisper) |
| `python-dotenv` | Load environment variables from `.env` |

## Usage

### Audio MCP Server

Transcribes new audio files in the `audios/` folder:

```bash
python audio_mcp_server.py
```

**Tool Available:**
- `process_new_meetings()` → Scans and transcribes new audio files, returns transcript text

**Supported Formats:** MP3, WAV, M4A, OGG, FLAC

### Email MCP Server

Sends emails to meeting participants:

```bash
python email_mcp_server.py
```

**Tool Available:**
- `send_email(to, subject, body)` → Sends email to specified participant

**Parameters:**
- `to` (str) — Recipient email address
- `subject` (str) — Email subject
- `body` (str) — Email body text

## OpenClaw Integration

OpenClaw uses these MCP servers as tools to perform meeting operations:

1. **Audio Transcription Flow:**
   - OpenClaw receives user request to process meetings
   - Calls `process_new_meetings()` tool from Audio MCP Server
   - Receives transcribed text and meeting content
   - Analyzes and summarizes for user

2. **Email Communication Flow:**
   - OpenClaw receives request to send follow-up emails
   - Calls `send_email()` tool from Email MCP Server
   - Emails sent to participants with meeting summaries or action items

3. **Automated Workflow:**
   - User provides meeting audio to `audios/` folder
   - Requests OpenClaw to "process meetings and send updates"
   - OpenClaw orchestrates both MCP servers automatically
   - Transcripts generated, analyzed, and emails sent

## Adding Audio Files

1. Place audio files in the `audios/` folder
2. Run `audio_mcp_server.py`
3. Transcripts are automatically saved to `audio_transcripts/` with naming pattern: `{filename}_transcript.txt`

## Configuration

### Whisper Model Size

Default: `base` model (~140MB)

Options: `tiny`, `base`, `small`, `medium`, `large`

To change, edit `audio_mcp_server.py`:

```python
model = whisper.load_model("small")  # or "medium", "large", etc.
```

### Email Configuration

- **SMTP Server:** Gmail SMTP (smtp.gmail.com:587)
- **Credentials:** App-specific password (more secure than account password)
- **Environment Variables:** Loaded from `.env`

## Security

- ⚠️ **Never commit `.env` file** — It contains sensitive credentials
- ✅ Ensure `.env` is in `.gitignore`
- ✅ Use app-specific passwords instead of account passwords
- ✅ Credentials loaded from environment variables, not hardcoded

## Example Workflow

### With OpenClaw (Recommended)

1. **Start the MCP Servers:**
   ```bash
   # Terminal 1 - Audio Server
   python audio_mcp_server.py
   
   # Terminal 2 - Email Server
   python email_mcp_server.py
   ```

2. **Upload meeting audio:**
   - Place audio files in `audios/` folder

3. **Ask OpenClaw to process meetings:**
   ```
   "Process all new meeting recordings and generate summaries"
   ```
   
   OpenClaw will:
   - Call `process_new_meetings()` to transcribe audio
   - Analyze the transcripts
   - Generate meeting summaries and action items

4. **Request automated follow-ups:**
   ```
   "Send follow-up emails to participants with meeting summaries"
   ```
   
   OpenClaw will:
   - Call `send_email()` for each participant
   - Send customized emails with meeting insights

## Troubleshooting

**Issue:** "Whisper model not found"
- **Solution:** Run `pip install --upgrade openai-whisper` and ensure `torch` is installed

**Issue:** "Email failed to send"
- **Solution:** Verify `.env` file has correct Gmail credentials and 2FA app password

**Issue:** "No new files detected"
- **Solution:** Ensure audio files are in `audios/` folder with supported extensions
