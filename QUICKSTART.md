# YTSumAI

Offline YouTube Video Summarizer using local AI models.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify setup**:
   ```bash
   python verify_setup.py
   ```

3. **Pull Ollama summarization model**:
   ```bash
   ollama pull llama3.1:8b-instruct-q4_K_M
   ```

4. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

> **Note:** OpenAI Whisper model downloads automatically on first use (~150MB)

See [README.md](README.md) for full documentation.
