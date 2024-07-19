#!/usr/bin/env python3

from faster_whisper import WhisperModel
from flask import Flask, Response, request
from typing import Iterator

import argparse
import io
import logging
import time
import os

app = Flask(__name__)


logger = logging.getLogger("point")

model_size = os.getenv("WHISPER_MODEL_SIZE", "base")

def transcribe(audio_file: io.BytesIO) -> Iterator[str]:
    header = time.strftime("%Y-%m-%d %H:%M:%S") + f", transcript with {model_size}"
    logger.info(header)
    yield (header + "\n\n")

    # TODO: configurable model path
    whisper = WhisperModel(
        model_size, download_root="./whisper-models", device="cpu"
    )
    segments, _ = whisper.transcribe(
        audio_file,
        beam_size=2,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    for t in segments:
        logger.info(f"[{str(t.start).rjust(8)}->{str(t.end).rjust(8)}] {t.text}")
        yield (t.text + "\n")


@app.route("/transcript", methods=["POST"])
def transcript_file():

    if not request.mimetype.startswith("audio"):
        return Response(
            "Invalid request. Please use an audio content type for the transcript.",
            status=400,
            mimetype="text/plain",
        )

    audio = io.BytesIO(request.data)

    return Response(transcribe(audio), mimetype="text/plain")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"""Transcribe audio to text.

This is a very simple Whisper endpoint which can be used like so:

    curl -X POST -T some-audio.mp3 -H 'Content-Type: audio/mp3' http://<host>:<port>/transcript

The trancript will be streamed as plain text.

(On first use, the {model_size} Whisper model is automatically downloaded
in a folder called 'whisper-models' in the current directory.)
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="The port on which the HTTP server will listen.",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="The host IP to bind to.")
    parser.add_argument("--verbose", action="store_true", help="Output MORE LOGS")

    args = parser.parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    app.run(host=args.host, port=args.port, threaded=True)
