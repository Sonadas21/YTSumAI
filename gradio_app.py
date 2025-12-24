"""Gradio UI for YTSumAI - Offline YouTube Video Summarizer"""

import gradio as gr
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.downloader import YouTubeDownloader
from app.services.transcriber import AudioTranscriber
from app.services.summarizer import TextSummarizer
from app.config import SUMMARIZATION_MODEL


def check_models():
    """Check if required models are available"""
    transcriber = AudioTranscriber()
    summarizer = TextSummarizer()
    
    stt_ok = transcriber.verify_model_available()
    sum_ok = summarizer.verify_model_available()
    
    return stt_ok, sum_ok


def process_video(url, enable_diarization, num_speakers, progress=gr.Progress()):
    """Process YouTube video and return results"""
    if not url:
        return None, None, "⚠️ Please enter a YouTube URL"
    
    try:
        downloader = YouTubeDownloader()
        transcriber = AudioTranscriber()
        summarizer = TextSummarizer()
        
        # Progress updates
        progress(0.1, desc="📥 Downloading audio...")
        audio_file, metadata = downloader.download_audio(url)
        
        progress(0.3, desc="🎤 Transcribing audio..." + (" & identifying speakers" if enable_diarization else ""))
        transcript = transcriber.transcribe_audio(
            audio_file,
            enable_diarization=enable_diarization,
            num_speakers=num_speakers if enable_diarization else None
        )
        
        progress(0.6, desc="📝 Generating summary...")
        summary = summarizer.summarize(transcript)
        
        progress(1.0, desc="✅ Complete!")
        
        # Format metadata
        info = f"""
## 📺 Video Information

**Title:** {metadata.title}  
**Channel:** {metadata.channel}  
**Duration:** {metadata.duration // 60} minutes  
**Video ID:** {metadata.video_id}
"""
        
        return summary, transcript, info
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        return None, None, error_msg


# Custom CSS for minimal, clean design
custom_css = """
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #000000;
}

#title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #1A1A1A;
    margin-bottom: 0.3rem;
    margin-top: 1rem;
}

#subtitle {
    text-align: center;
    font-size: 1rem;
    color: #6A737D;
    margin-bottom: 1.5rem;
}

.input-box input {
    border-radius: 8px !important;
    border: 1.5px solid #E1E4E8 !important;
    background: #FFFFFF !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
}

.input-box input:focus {
    border-color: #0366D6 !important;
    box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.1) !important;
}

.submit-btn {
    background: #0366D6 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: white !important;
    text-transform: uppercase !important;
    letter-spacing: 0.02em !important;
}

.submit-btn:hover {
    background: #0256C2 !important;
    box-shadow: 0 4px 12px rgba(3, 102, 214, 0.25) !important;
}

footer {
    text-align: center;
    color: #6A737D;
    padding: 1rem;
    font-size: 13px;
    margin-top: 2rem;
}
"""

# Check model status
stt_ok, sum_ok = check_models()
model_status = f"""
**Model Status**

{'✅ Whisper Available' if stt_ok else '❌ Whisper Not Found'}  
{'✅ LLM Available' if sum_ok else f'❌ Pull: `ollama pull {SUMMARIZATION_MODEL}`'}
"""

# Build Gradio Interface
with gr.Blocks(title="YTSumAI - YouTube Summarizer") as app:
    
    # Header
    gr.Markdown("# YTSumAI", elem_id="title")
    gr.Markdown(
        "Transform YouTube videos into concise summaries using local AI",
        elem_id="subtitle"
    )
    
    # Main Interface
    with gr.Row():
        with gr.Column(scale=3):
            url_input = gr.Textbox(
                label="",
                placeholder="Paste YouTube video URL here...",
                lines=1,
                elem_classes=["input-box"]
            )
            
            # Advanced Options
            with gr.Accordion("⚙️ Advanced Options", open=False):
                enable_diarization = gr.Checkbox(
                    label="🎙️ Enable Speaker Diarization",
                    value=False,
                    info="Identify different speakers (adds 3-5 min processing time)"
                )
                
                num_speakers = gr.Slider(
                    label="Expected number of speakers",
                    minimum=2,
                    maximum=10,
                    step=1,
                    value=2,
                    visible=False,
                    info="Optional hint to improve accuracy"
                )
                
                # Show/hide speaker count based on diarization toggle
                enable_diarization.change(
                    fn=lambda x: gr.update(visible=x),
                    inputs=[enable_diarization],
                    outputs=[num_speakers]
                )
            
            submit_btn = gr.Button(
                "✨ SUMMARIZE",
                variant="primary",
                size="lg",
                elem_classes=["submit-btn"]
            )
        
        with gr.Column(scale=1):
            gr.Markdown(model_status)
    
    # Output Section
    with gr.Row():
        with gr.Column():
            info_output = gr.Markdown(label="Video Info")
    
    with gr.Row():
        with gr.Column():
            summary_output = gr.Textbox(
                label="📝 Summary",
                lines=6
            )
    
    with gr.Row():
        with gr.Column():
            with gr.Accordion("📄 Full Transcript", open=False):
                transcript_output = gr.Textbox(
                    label="",
                    lines=10
                )
    
    # Footer
    gr.Markdown(
        """
        <footer>
        Built with Gradio & OpenAI Whisper | 100% Offline Processing
        </footer>
        """,
        elem_id="footer"
    )
    
    # Event handlers
    submit_btn.click(
        fn=process_video,
        inputs=[url_input, enable_diarization, num_speakers],
        outputs=[summary_output, transcript_output, info_output]
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        css=custom_css
    )
