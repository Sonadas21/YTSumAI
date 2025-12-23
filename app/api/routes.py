"""API routes for YTSumAI"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse, VideoMetadata
from app.services import YouTubeDownloader, AudioTranscriber, TextSummarizer
import time

router = APIRouter()

# Initialize services
downloader = YouTubeDownloader()
transcriber = AudioTranscriber()
summarizer = TextSummarizer()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "YTSumAI",
        "version": "1.0.0"
    }


@router.get("/models")
async def check_models():
    """Check availability of required models"""
    stt_available = transcriber.verify_model_available()
    sum_available = summarizer.verify_model_available()
    
    return {
        "stt_model": {
            "name": "OpenAI Whisper (offline)",
            "available": stt_available
        },
        "summarization_model": {
            "name": summarizer.model,
            "available": sum_available
        }
    }


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_video(request: SummarizeRequest):
    """
    Summarize a YouTube video
    
    This endpoint:
    1. Downloads audio from the YouTube URL
    2. Transcribes the audio using OpenAI Whisper (offline)
    3. Summarizes the transcript using Ollama LLM
    4. Returns the transcript and summary
    
    Note: Audio files are kept for verification and cleaned up on next request
    """
    try:
        start_time = time.time()
        
        # Download audio
        audio_file, metadata = downloader.download_audio(str(request.url))
        
        # Transcribe audio
        transcript = transcriber.transcribe_audio(audio_file)
        
        # Summarize transcript
        summary = summarizer.summarize(transcript)
        
        # Note: Audio file kept for verification (cleaned up on next download)
        
        processing_time = time.time() - start_time
        
        # Calculate word counts
        transcript_word_count = len(transcript.split())
        summary_word_count = len(summary.split())
        
        return SummarizeResponse(
            metadata=metadata,
            transcript=transcript,
            summary=summary,
            processing_time=processing_time,
            transcript_word_count=transcript_word_count,
            summary_word_count=summary_word_count
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
