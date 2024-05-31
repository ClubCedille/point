#!/usr/bin/env python3

from faster_whisper import WhisperModel
import argparse
from pathlib import Path
import time

import logging

logger = logging.getLogger("virgule")

model_size = "base"


def transcribe(audio_file: str, text_file: Path):
    whisper = WhisperModel(
        model_size, download_root="./whisper-models", compute_type="int8"
    )
    segments, _ = whisper.transcribe(
        audio_file,
        beam_size=2,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    with open(text_file, "a") as text:
        text.write(time.strftime("%Y-%m-%d %H:%M:%S") + f", {model_size}\n\n")
        for t in segments:
            logger.info(f"[{str(t.start).rjust(8)}->{str(t.end).rjust(8)}] {t.text}")
            text.write(t.text + "\n")


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio to text")
    parser.add_argument("--audio-path", type=str, help="Path to an audio file")
    parser.add_argument(
        "--output", type=Path, help="Path the output text file of the transcription"
    )
    parser.add_argument("--verbose", action="store_true", help="Path to an audio file")

    args = parser.parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    if args.audio_path and args.output:
        transcribe(args.audio_path, args.output)
    else:
        logger.error("MISSING ARGUMENTS, PLEASE ARGUE")
        parser.print_help()


if __name__ == "__main__":
    main()
