from mcp.server.fastmcp import FastMCP
import os
import whisper
from pathlib import Path

mcp = FastMCP("AudioServer")

# ── Paths ─────────────────────────────────────
BASE = Path(__file__).resolve().parent

AUDIO_DIR = os.path.join(BASE, "audios")
TRANSCRIPT_DIR = os.path.join(BASE, "audio_transcripts")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# ── Load Whisper once ─────────────────────────
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded.")


def is_new_file(filename):
    name = os.path.splitext(filename)[0]
    transcript_file = os.path.join(
        TRANSCRIPT_DIR,
        name + "_transcript.txt"
    )
    return not os.path.exists(transcript_file)


@mcp.tool()
def process_new_meetings() -> str:
    """
    Scan audio folder and transcribe only NEW files.
    Returns transcript text for OpenClaw reasoning.
    """

    audio_extensions = [
        ".mp3",
        ".wav",
        ".m4a",
        ".ogg",
        ".flac"
    ]

    new_files = []

    for filename in sorted(os.listdir(AUDIO_DIR)):

        file_path = os.path.join(
            AUDIO_DIR,
            filename
        )

        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        if ext not in audio_extensions:
            continue

        if is_new_file(filename):
            new_files.append(filename)

    if not new_files:
        return "NO_NEW_FILES"

    results = []

    for filename in new_files:

        try:
            print(f"Transcribing: {filename}")

            file_path = os.path.join(
                AUDIO_DIR,
                filename
            )

            name = os.path.splitext(filename)[0]

            result = model.transcribe(file_path)
            transcript = result["text"].strip()

            transcript_path = os.path.join(
                TRANSCRIPT_DIR,
                name + "_transcript.txt"
            )

            with open(
                transcript_path,
                "w",
                encoding="utf-8"
            ) as f:
                f.write(transcript)

            print(f"Saved: {transcript_path}")

            results.append(
                f"TRANSCRIPT_FILE: "
                f"{name}_transcript.txt\n"
                f"NEW_MEETING_TRANSCRIPT:\n"
                f"{transcript}"
            )

        except Exception as e:

            print(f"Failed: {filename}")

            results.append(
                f"ERROR processing "
                f"{filename}: {str(e)}"
            )

    return "\n\n===\n\n".join(results)




if __name__ == "__main__":
    mcp.run(transport="stdio")