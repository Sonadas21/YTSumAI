# YTSumAI - Offline YouTube Video Summarizer

An end-to-end AI system that downloads YouTube videos, transcribes audio using offline speech-to-text (Whisper), and generates concise summaries using local LLMs - **100% offline, no cloud APIs required**.

![Project Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11-blue)

## 🎯 Overview

YTSumAI is a complete offline solution for YouTube video summarization that leverages:
- **yt-dlp** for downloading YouTube audio
- **OpenAI Whisper** (offline) for speech-to-text transcription
- **Llama 3.1 8B** local LLM for intelligent summarization  
- **Gradio** for a clean, modern web interface (recommended)
- **Streamlit** as an alternative UI option
- **FastAPI** for optional REST API access

### Key Features

✅ **100% Offline Processing** - No cloud APIs, complete data privacy  
✅ **Modern Web UI** - Clean Gradio interface with minimal design (or Streamlit alternative)  
✅ **Smart Chunking** - Handles videos of any length (tested up to 2+ hours)  
✅ **Speaker Diarization** - Optional speaker identification for multi-person content 🎙️ **NEW**  
✅ **REST API** - Optional FastAPI backend for programmatic access  
✅ **Docker Support** - Easy deployment with containerization  
✅ **Progress Tracking** - Real-time updates during processing  
✅ **Export Options** - Download transcripts and summaries

## 📋 Prerequisites

Before running this project, ensure you have:

1. **Python 3.11+** installed
2. **FFmpeg** installed (required by yt-dlp for audio extraction)
   
   **Windows Installation Options:**
   
   **Option 1: Using winget (Recommended for Windows 10/11)**
   ```powershell
   winget install ffmpeg
   ```
   After installation, **restart your terminal** for PATH changes to take effect.
   
   **Option 2: Using Chocolatey**
   ```powershell
   choco install ffmpeg
   ```
   
   **Option 3: Manual Installation**
   - Download from: https://github.com/BtbN/FFmpeg-Builds/releases
   - Download: `ffmpeg-master-latest-win64-gpl.zip`
   - Extract to `C:\ffmpeg`
   - Add to PATH:
     1. Search "Environment Variables" in Windows
     2. Edit "Path" under System Variables
     3. Add `C:\ffmpeg\bin`
     4. **Restart terminal/IDE**
   
   **Verify Installation:**
   ```bash
   ffmpeg -version
   ```
   
   **Linux/Ubuntu:**
   ```bash
   sudo apt-get install ffmpeg
   ```
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```

3. **Ollama** installed and running
   - Download from [ollama.ai](https://ollama.ai)
   - Ensure Ollama service is running: `ollama serve`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd YTSumAI
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Pull Required Ollama Models

```bash
# Pull Llama model for summarization (Whisper downloads automatically on first use)
ollama pull llama3.1:8b-instruct-q4_K_M
```

> [!NOTE]
> OpenAI Whisper model (~150MB) will download automatically on first transcription.
> No manual installation required!

### 4. Configuration

Copy the example environment file and customize if needed:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS
```

Default configuration:
```env
OLLAMA_BASE_URL=http://localhost:11434
SUMMARIZATION_MODEL=llama3.1:8b-instruct-q4_K_M
MAX_VIDEO_DURATION=7200
DOWNLOAD_DIR=./downloads
```

> [!TIP]
> The `STT_MODEL` configuration is no longer needed - OpenAI Whisper runs independently!

### 5. Run the Application

#### Option A: Gradio UI (Recommended ⭐)

```bash
python gradio_app.py
```

Then open your browser to: **http://localhost:7860**

#### Option B: Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then open your browser to: **http://localhost:8501**

#### Option C: FastAPI Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API documentation available at: **http://localhost:8000/docs**

### 6. Using the Application

1. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

2. **Open the Gradio or Streamlit UI** in your browser

3. **Enter a YouTube URL** and configure options:
   - Paste the video URL
   - **(Optional)** Expand "Advanced Options" to enable speaker diarization
   - **Enable Speaker Diarization** for multi-speaker content (podcasts, interviews)
   - Set expected number of speakers (helps improve accuracy)

4. **Click "🚀 Summarize"**

5. **Wait for processing** - The app will:
   - Download the audio
   - Transcribe it to text
   - **(If enabled)** Identify different speakers
   - Generate a summary
   
6. **View results** and download transcripts/summaries

---

## 🎙️ Speaker Diarization (Optional Feature)

### What is Speaker Diarization?

Speaker diarization identifies "who spoke when" in audio with multiple speakers. Perfect for:
- 🎙️ **Podcasts** - Multi-host shows
- 🗣️ **Interviews** - Host + guest conversations
- 💼 **Panel Discussions** - Multiple participants
- 🎓 **Lectures with Q&A** - Professor + students

### How to Use

1. **Enable in UI:**
   - Expand "⚙️ Advanced Options"
   - Check "🎙️ Enable Speaker Diarization" 
   - Set expected speaker count (optional hint)

2. **Processing Time:**
   - Standard mode: 3-6 minutes
   - With diarization: 7-12 minutes (+3-5 min)

3. **Output Format:**
   ```
   [Speaker 1] Welcome to today's podcast...
   [Speaker 2] Thanks for having me!
   [Speaker 1] Let's dive into the topic...
   ```

### Configuration

**Requirements:**
```bash
pip install pyannote.audio torch torchaudio
```

**Models:**
- Auto-downloads on first use (~300 MB)
- Cached globally in `~/.cache/torch/`
- Requires ~3-4 GB RAM additional

### When to Use / Skip

**✅ Use Diarization For:**
- Podcasts with 2+ hosts
- Interview formats
- Panel discussions
- Roundtable conversations

**❌ Skip Diarization For:**
- Solo tutorials/vlogs
- Single-speaker lectures
- Music videos/performances
- News with one anchor

> [!TIP]
> Diarization is **OFF by default** for optimal speed. Enable only when needed!

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
# Make sure Ollama is running on your host machine
ollama serve

# Build and start the container
docker-compose up --build
```

Access the application at: **http://localhost:8501**

### Docker Notes

- The container uses `network_mode: host` to access Ollama running on your host machine
- Downloads are persisted in a volume mount
- Environment variables can be configured in `.env` file

## 🏗️ Architecture

```
YTSumAI/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── main.py                # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── downloader.py      # YouTube audio downloader
│       ├── transcriber.py     # Speech-to-text service
│       └── summarizer.py      # Text summarization service
├── static/                    # (Unused with Streamlit)
├── downloads/                 # Temporary audio files
├── streamlit_app.py          # Streamlit UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

### Component Details

#### 1. **YouTube Downloader** (`downloader.py`)
- Uses `yt-dlp` to extract audio from YouTube videos
- Validates video duration against configurable limits
- Extracts metadata (title, channel, duration)
- Automatic cleanup of downloaded files

#### 2. **Audio Transcriber** (`transcriber.py`)
- Integrates with Ollama Whisper model
- Implements chunking for videos > 30 minutes
- Processes audio segments separately and combines results
- Handles audio format conversion with `pydub`

#### 3. **Text Summarizer** (`summarizer.py`)
- Uses Qwen 2.5 LLM via Ollama
- Implements map-reduce strategy for long transcripts
- Chunk summaries are combined into final comprehensive summary
- Configurable summary length and style

#### 4. **Streamlit UI** (`streamlit_app.py`)
- Modern glassmorphism design with gradients
- Real-time progress tracking
- Model availability checking
- Download options for transcripts and summaries
- Responsive layout

#### 5. **FastAPI Backend** (`main.py`, `routes.py`)
- RESTful API endpoints
- Health checks and model verification
- Swagger/OpenAPI documentation
- CORS support for web integration

## 🎨 Design Choices & Justifications

### Model Selection

**Speech-to-Text: OpenAI Whisper (Offline)**
- Industry-leading accuracy for speech recognition
- Supports 99+ languages with automatic detection
- Optimized for various audio quality levels
- Runs 100% locally on CPU or GPU
- No API calls or internet required (after initial download)
- Multiple model sizes available (tiny, base, small, medium, large)

**Available Whisper Models:**

| Model | Size | Speed | Accuracy | Memory | Use Case |
|-------|------|-------|----------|--------|----------|
| `tiny` | ~39 MB | Fastest | Lowest | ~1 GB | Quick tests, prototyping |
| `base` | **~142 MB** | **Fast** | **Good** | **~1.5 GB** | **Default (Balanced)** ✅ |
| `small` | ~466 MB | Medium | Better | ~2 GB | Higher quality needs |
| `medium` | ~1.5 GB | Slower | Very Good | ~5 GB | Professional use |
| `large` | ~2.9 GB | Slowest | Best | ~10 GB | Maximum accuracy |

> [!TIP]
> We use the **`base`** model as it provides the best balance between speed, accuracy, and resource usage for most YouTube videos. You can change this in [`transcriber.py`](app/services/transcriber.py) line 23.

**Model Selection Rationale:**
- **Base model** chosen for optimal speed/quality trade-off
- Downloads automatically on first use (~142 MB)
- Fast enough for real-time-ish transcription
- Accurate enough for YouTube content
- Low memory footprint (~1.5 GB RAM)
- Works well on consumer hardware without GPU

**Summarization: Llama 3.1 (8B parameters, quantized)**
- Excellent instruction following
- Fast inference with 4-bit quantization
- Good balance between quality and speed
- Strong performance on abstractive summarization tasks

### Trade-offs Considered

1. **Model Size vs. Accuracy**
   - Chose 3B parameter model for faster inference
   - For higher quality, can swap to larger models (7B, 8B)
   
2. **Chunking Strategy**
   - Videos > 30 minutes are processed in chunks
   - Prevents memory issues and timeout errors
   - Slight context loss at chunk boundaries (mitigated with overlap)

3. **Processing Time vs. Quality**
   - Current configuration optimized for reasonable wait times
   - Can adjust temperature and top_p for different quality/speed trade-offs

## 📊 Performance Considerations

### Typical Processing Times

| Video Length | Download | Transcription | Summarization | Total |
|-------------|----------|---------------|---------------|-------|
| 5 minutes   | 10-20s   | 30-60s       | 20-30s       | ~1-2 min |
| 30 minutes  | 30-60s   | 5-10 min     | 1-2 min      | ~7-13 min |
| 1 hour      | 1-2 min  | 15-25 min    | 2-4 min      | ~18-31 min |

*Note: Times vary based on hardware, internet speed, and model efficiency*

### Optimization Tips

1. **Use GPU acceleration** if available (Ollama will auto-detect)
2. **Increase chunk size** for faster processing (may increase memory usage)
3. **Use smaller models** for faster inference (trade-off: lower quality)
4. **Pre-download frequently used videos** to skip download step

## 🧠 Challenges Faced

### 1. Context Window Limitations & Chunking
One of the primary challenges was **summarizing transcripts** from long YouTube videos (e.g., >1 hour) with the **Llama 3.1 8B** model, which has a limited context window. Passing the entire transcript at once would result in token overflow errors.

**Solution:** Implemented a **Map-Reduce summarization strategy**:
- **Map:** Split the transcript into manageable 4000-token chunks with overlap to preserve context.
- **Reduce:** Summarize each chunk independently, then combine and refine these partial summaries into a final coherent output.

### 2. Offline Dependency Management
Ensuring a strictly offline experience while keeping setup easy was difficult, particularly with **FFmpeg** (for audio) and **Ollama** (for LLMs).

**Solution:** 
- Created detailed, OS-specific installation guides for FFmpeg.
- Leveraged **Ollama's** self-contained architecture to handle model weights locally without complex Python environments (like PyTorch/Transformers) for the LLM part.
- Used **Whisper's** automatic model downloading (on first run) to balance the "offline" requirement with initial ease of use.

### 3. Balancing Inference Speed vs. Quality
Running two heavy models (Whisper + Llama 3) locally on consumer hardware can be slow.

**Solution:** 
- Selected **Whisper `base`** model as the default: it offers the best speed-to-accuracy ratio for clear YouTube audio.
- Used **4-bit quantized** Llama 3.1 models via Ollama to drastically reduce RAM usage and increase inference speed without significant quality loss compared to fp16 models.

## 🔧 API Usage

### Endpoints

**Health Check**
```bash
GET /api/health
```

**Check Models**
```bash
GET /api/models
```

**Summarize Video**
```bash
POST /api/summarize
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Example Response**
```json
{
  "metadata": {
    "title": "Example Video",
    "duration": 300,
    "channel": "Example Channel",
    "video_id": "dQw4w9WgXcQ",
    "url": "https://youtube.com/watch?v=..."
  },
  "transcript": "Full transcript text...",
  "summary": "Concise summary...",
  "processing_time": 45.2,
  "transcript_word_count": 1200,
  "summary_word_count": 150
}
```

## ❗ Troubleshooting

### Common Issues

**1. "Whisper Not Installed"**
```bash
pip install openai-whisper
```

> [!NOTE]
> The Whisper model will download automatically (~150MB) on first use.

**2. "Connection refused to Ollama"**
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in `.env`

**3. "FFmpeg not found" or "Postprocessing: ffprobe and ffmpeg not found"**

This is the most common issue on Windows. FFmpeg is required for audio extraction.

**Solutions:**

1. **Install FFmpeg** (if not installed):
   ```powershell
   # Recommended: Using winget (Windows 10/11)
   winget install ffmpeg
   
   # OR using Chocolatey
   choco install ffmpeg
   ```

2. **After installation, MUST restart your terminal/IDE completely**
   - Close all PowerShell/CMD windows
   - Close VS Code/IDE if running
   - Reopen and test: `ffmpeg -version`

3. **If still not working, manually add to PATH:**
   - Find FFmpeg location (usually `C:\ffmpeg\bin` or `C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin`)
   - Add to System PATH:
     1. Windows Search → "Environment Variables"
     2. System Properties → Environment Variables
     3. Under "System variables", select "Path" → Edit
     4. Click "New" → Add `C:\ffmpeg\bin` (or your FFmpeg bin path)
     5. Click OK on all dialogs
     6. **Restart terminal completely**

4. **Verify it works:**
   ```bash
   ffmpeg -version
   # Should show: ffmpeg version N-xxxxx-gxxxxxxx
   ```

**Common Error Messages:**
- `ERROR: Postprocessing: ffprobe and ffmpeg not found` → FFmpeg not in PATH
- `ffmpeg: command not found` → FFmpeg not installed or not in PATH
- Video downloads but won't convert → FFmpeg missing

**Note:** The warning `Couldn't find ffmpeg or avconv` from pydub is harmless during startup, but FFmpeg must be installed for actual video processing.


**4. "Video too long" error**
- Increase `MAX_VIDEO_DURATION` in `.env`
- Note: Longer videos take more time to process

**5. Docker can't connect to Ollama**
- Use `network_mode: host` in docker-compose.yml
- Or set `OLLAMA_BASE_URL=http://host.docker.internal:11434`

## 🚧 Future Enhancements

- [ ] Speaker diarization support
- [ ] Multiple language detection and transcription
- [ ] Timestamp-based summary sections
- [ ] Batch processing for multiple videos
- [ ] Summary customization (bullet points, paragraphs, key quotes)
- [ ] Export to PDF/Word formats
- [ ] Video thumbnail extraction
- [ ] Progress persistence (resume interrupted processing)


## 📧 Contact

For questions or support, please open an issue on GitHub or send mail on dass21656@gmail.com.
