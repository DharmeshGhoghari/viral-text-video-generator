# Free local TTS + voice cloning setup
# =====================================
# This project keeps the existing `index.html` video generator intact and adds a separate
# FastAPI-based Text-to-Speech interface at `/tts`.
#
# Recommended local run on Windows:
#   1) python -m venv .venv
#   2) .venv\Scripts\activate
#   3) python -m pip install --upgrade pip
#   4) python -m pip install -r requirements.txt
#   5) python server.py
#
# Then open:
#   http://localhost:8000/tts
#
# Notes:
# - Voice reference file: Standard recording 32_20261008192509.mp3
# - The implementation tries to use Coqui XTTS-v2 for voice cloning, which is free and
#   open source, but model download and runtime memory usage depend on your local machine.
# - Gujarati support depends on the downloaded model and its actual language coverage.
# - The UI keeps the selected voice saved using browser localStorage; the default reference
#   voice file is reused automatically from the repository.

# The final application is implemented in `server.py` + `static/tts.html` + `static/tts.js`.
