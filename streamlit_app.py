"""Streamlit UI for YTSumAI - Offline YouTube Video Summarizer"""

import streamlit as st
import time
from pathlib import Path
import sys

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services import YouTubeDownloader, AudioTranscriber, TextSummarizer
from app.config import SUMMARIZATION_MODEL
from app.models.schemas import VideoMetadata


# Page configuration
st.set_page_config(
    page_title="YTSumAI - YouTube Summarizer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with modern, engaging design
st.markdown("""
<style>
    /* Global Styles with Gradient Background */
    .main {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 25%, #F093FB 50%, #F5576C 100%);
        padding: 0 !important;
    }
    .stApp {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 25%, #F093FB 50%, #F5576C 100%);
    }
    
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        letter-spacing: -0.03em;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    
    h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    }
    
    /* Main Container */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
        max-width: 750px !important;
    }
    
    /* Input Field - Large & Centered */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        padding: 20px 24px;
        font-size: 17px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        color: #1A1A1A;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        font-weight: 500;
        text-align: center;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9CA3AF;
        font-weight: 400;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.9);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25), 0 0 0 4px rgba(255, 255, 255, 0.2);
        background: #FFFFFF;
        transform: translateY(-2px);
    }
    
    /* Button - Glassmorphic & Large */
    .stButton > button {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        color: white;
        border-radius: 16px;
        padding: 18px 40px;
        font-size: 18px;
        font-weight: 700;
        border: 2px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.45);
        border-color: rgba(255, 255, 255, 0.7);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.3);
        transform: translateY(-4px) scale(1.02);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    /* Sidebar - Glass Effect */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(30px);
        border-right: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-bottom: 16px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Metrics - Glass Cards */
   .stMetric {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Result Cards - Premium Glass */
    .result-card {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(25px);
        padding: 32px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        margin: 24px 0;
        line-height: 1.8;
        color: #1A1A1A;
    }
    
    /* Expander - Glass Effect */
    .stExpander {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(20px);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        overflow: hidden;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
    }
    
    .stExpander summary {
        color: white !important;
        font-weight: 600 !important;
        padding: 16px 20px !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FFFFFF 0%, rgba(255, 255, 255, 0.85) 100%);
    }
    
    /* Success/Error Messages - Glass Cards */
    .stSuccess {
        background: rgba(76, 175, 80, 0.25);
        backdrop-filter: blur(20px);
        color: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        font-weight: 500;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.25);
        backdrop-filter: blur(20px);
        color: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #DC3545;
        box-shadow: 0 6px 20px rgba(244, 67, 54, 0.3);
        font-weight: 500;
    }
    
    .stInfo {
        background: rgba(33, 150, 243, 0.25);
        backdrop-filter: blur(20px);
        color: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #2196F3;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.3);
        font-weight: 500;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.25);
        backdrop-filter: blur(20px);
        color: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #FF9800;
        box-shadow: 0 6px 20px rgba(255, 152, 0, 0.3);
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid rgba(255, 255, 255, 0.2);
        margin: 40px 0;
    }
    
    /* Download Buttons - Glass Effect */
    .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        padding: 14px 26px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(255, 255, 255, 0.35);
        border-color: rgba(255, 255, 255, 0.65);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    /* Text Area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        font-size: 14px;
        line-height: 1.7;
        color: #1A1A1A;
        padding: 16px;
    }
    
    /* Checkbox & Slider */
    .stCheckbox label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }
    
    .stSlider {
        color: white !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #FFFFFF !important;
    }
    
    /* All text white */
    p, label, span {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'result' not in st.session_state:
    st.session_state.result = None


def check_ollama_models():
    """Check if required Ollama models are available"""
    transcriber = AudioTranscriber()
    summarizer = TextSummarizer()
    
    stt_available = transcriber.verify_model_available()
    sum_available = summarizer.verify_model_available()
    
    return stt_available, sum_available


def process_video(url: str, enable_diarization: bool = False, num_speakers: int = None):
    """Process YouTube video: download, transcribe, summarize"""
    
    downloader = YouTubeDownloader()
    transcriber = AudioTranscriber()
    summarizer = TextSummarizer()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        start_time = time.time()
        
        # Step 1: Download audio
        status_text.text("📥 Downloading audio from YouTube...")
        progress_bar.progress(10)
        audio_file, metadata = downloader.download_audio(url)
        progress_bar.progress(30)
        
        # Step 2: Transcribe audio (with optional diarization)
        if enable_diarization:
            status_text.text("🎤 Transcribing audio and identifying speakers...")
        else:
            status_text.text("🎤 Transcribing audio to text...")
        transcript = transcriber.transcribe_audio(audio_file, enable_diarization, num_speakers)
        progress_bar.progress(60)
        
        # Step 3: Summarize transcript
        status_text.text("📝 Generating summary...")
        summary = summarizer.summarize(transcript)
        progress_bar.progress(90)
        
        # Note: Audio file kept for verification (cleaned up on next download)
        progress_bar.progress(100)
        
        processing_time = time.time() - start_time
        
        # Calculate word counts
        transcript_word_count = len(transcript.split())
        summary_word_count = len(summary.split())
        
        status_text.text("✅ Processing complete!")
        
        return {
            'metadata': metadata,
            'transcript': transcript,
            'summary': summary,
            'processing_time': processing_time,
            'transcript_word_count': transcript_word_count,
            'summary_word_count': summary_word_count
        }
        
    except Exception as e:
        status_text.text("")
        progress_bar.empty()
        raise e


# Main UI - Hero Section
st.markdown("<br>", unsafe_allow_html=True)
st.title("YTSumAI")
st.markdown("<p style='font-size: 20px; color: rgba(255, 255, 255, 0.95); margin-top: -12px; text-align: center; font-weight: 400; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);'>Transform YouTube videos into concise summaries using local AI</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown(f"""
    **STT Model:** OpenAI Whisper (offline)  
    **Summarization:** `{SUMMARIZATION_MODEL}` (Ollama)
    """)
    
    st.divider()
    
    st.header("📊 Model Status")
    with st.spinner("Checking models..."):
        stt_ok = AudioTranscriber().verify_model_available()
        sum_ok = TextSummarizer().verify_model_available()
    
    if stt_ok:
        st.success("✅ Whisper (Offline) Available")
    else:
        st.error("❌ Whisper Not Installed\n\nRun: `pip install openai-whisper`")
    
    if sum_ok:
        st.success("✅ Summarization Model Available")
    else:
        st.error(f"❌ Summarization Model Not Found\n\nRun: `ollama pull {SUMMARIZATION_MODEL}`")
    
    st.divider()
    
    st.header("ℹ️ How It Works")
    st.markdown("""
    1. **Download** audio from YouTube
    2. **Transcribe** using offline Whisper
    3. **Summarize** using local LLM (Ollama)
    4. **100% offline** processing
    """)

# Main input area - centered
url = st.text_input(
    "YouTube Video URL",
    placeholder="Paste YouTube video URL here...",
    help="Enter the URL of any public YouTube video",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

submit_button = st.button("✨ SUMMARIZE", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Advanced Options (collapsible)
with st.expander("⚙️ Advanced Options", expanded=False):
    enable_diarization = st.checkbox(
        " 🎙️ Enable Speaker Diarization",
        value=False,
        help="Identify different speakers in the video (adds 3-5 min processing time)"
    )
    
    if enable_diarization:
        st.markdown("""
        <div style="background: #FFF3CD; padding: 12px; border-radius: 6px; border-left: 3px solid #FFC107; margin: 8px 0;">
            <small>💡 <strong>Tip:</strong> Best for podcasts, interviews, and panel discussions</small>
        </div>
        """, unsafe_allow_html=True)
        
        num_speakers = st.slider(
            "Expected number of speakers",
            min_value=2,
            max_value=10,
            value=2,
            help="Hint to improve accuracy (optional)"
        )
    else:
        num_speakers = None
        
    # Show estimated processing time
    if enable_diarization:
        st.info("⏱️ Estimated processing time: 7-12 minutes")
    else:
        st.info("⏱️ Estimated processing time: 3-6 minutes")

# Process video when button is clicked
if submit_button and url:
    if not (stt_ok and sum_ok):
        st.error("⚠️ Required models are not available. Please check the sidebar for setup instructions.")
    else:
        try:
            with st.spinner("Processing video..."):
                result = process_video(url, enable_diarization, num_speakers)
                st.session_state.result = result
            
            st.success("✅ Video processed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif submit_button and not url:
    st.warning("⚠️ Please enter a YouTube URL")

# Display results
if st.session_state.result:
    result = st.session_state.result
    metadata = result['metadata']
    
    st.markdown("---")
    st.header("📺 Video Information")
    
    # Video metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Title", metadata.title)
    with col2:
        st.metric("Channel", metadata.channel)
    with col3:
        duration_min = metadata.duration // 60
        st.metric("Duration", f"{duration_min} min")
    
    # Processing stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Processing Time", f"{result['processing_time']:.1f}s")
    with col2:
        st.metric("Transcript Words", f"{result['transcript_word_count']:,}")
    with col3:
        st.metric("Summary Words", f"{result['summary_word_count']:,}")
    
    st.markdown("---")
    
    # Summary
    st.header("📝 Summary")
    st.markdown(f"""
    <div class="result-card">
    {result['summary']}
    </div>
    """, unsafe_allow_html=True)
    
    # Transcript (expandable)
    st.markdown("---")
    with st.expander("📄 View Full Transcript", expanded=False):
        st.text_area(
            "Transcript",
            result['transcript'],
            height=400,
            label_visibility="collapsed"
        )
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="⬇️ Download Summary",
            data=result['summary'],
            file_name=f"{metadata.video_id}_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="⬇️ Download Transcript",
            data=result['transcript'],
            file_name=f"{metadata.video_id}_transcript.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255, 255, 255, 0.9); padding: 20px; font-size: 14px; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);'>
    <p>Built with Streamlit & OpenAI Whisper | 100% Offline Processing</p>
</div>
""", unsafe_allow_html=True)
