"""Audio transcription using offline Whisper model"""

import whisper
from pathlib import Path
from typing import List
from pydub import AudioSegment
from app.config import CHUNK_DURATION_MINUTES


class AudioTranscriber:
    """Transcribes audio using offline Whisper model"""
    
    def __init__(self):
        self.chunk_duration_ms = CHUNK_DURATION_MINUTES * 60 * 1000
        self.model = None
        
    def _load_model(self):
        """Lazy load the Whisper model"""
        if self.model is None:
            print("Loading Whisper model (this may take a moment on first run)...")
            # Use 'base' model for good balance of speed and accuracy
            # Options: tiny, base, small, medium, large
            self.model = whisper.load_model("base")
            print("Whisper model loaded successfully!")
        return self.model
        
    def transcribe_audio(
        self, 
        audio_file: Path,
        enable_diarization: bool = False,
        num_speakers: int = None
    ) -> str:
        """
        Transcribe audio file to text using offline Whisper
        
        Args:
            audio_file: Path to audio file
            enable_diarization: Whether to identify speakers
            num_speakers: Expected number of speakers (optional hint)
            
        Returns:
            Complete transcript text (with speaker labels if diarization enabled)
            
        Raises:
            Exception: If transcription fails
        """
        try:
            # Load the model
            model = self._load_model()
            
            # Check if audio needs to be chunked
            audio = AudioSegment.from_file(audio_file)
            
            if len(audio) > self.chunk_duration_ms:
                transcript = self._transcribe_chunked(audio_file, model)
            else:
                transcript = self._transcribe_single(audio_file, model)
            
            # Add speaker labels if diarization is enabled
            if enable_diarization:
                try:
                    from app.services.diarizer import SpeakerDiarizer
                    diarizer = SpeakerDiarizer()
                    segments = diarizer.diarize_audio(audio_file, num_speakers)
                    if segments:
                        transcript = diarizer.merge_with_transcript(transcript, segments)
                except Exception as e:
                    print(f"Diarization failed, continuing with plain transcript: {e}")
            
            return transcript
                
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _transcribe_single(self, audio_file: Path, model) -> str:
        """
        Transcribe a single audio file using Whisper
        
        Args:
            audio_file: Path to audio file
            model: Loaded Whisper model
            
        Returns:
            Transcript text
        """
        print(f"Transcribing audio file: {audio_file.name}")
        
        # Transcribe using Whisper (fully offline)
        result = model.transcribe(
            str(audio_file),
            fp16=False,  # Use fp32 for CPU compatibility
            language='en',  # Auto-detect if None, specify for faster processing
            verbose=False
        )
        
        transcript = result['text'].strip()
        
        if not transcript:
            raise Exception("Whisper returned empty transcription")
        
        print(f"Transcription complete: {len(transcript)} characters")
        return transcript
    
    def _transcribe_chunked(self, audio_file: Path, model) -> str:
        """
        Transcribe long audio by splitting into chunks
        
        Args:
            audio_file: Path to audio file
            model: Loaded Whisper model
            
        Returns:
            Combined transcript text
        """
        audio = AudioSegment.from_file(audio_file)
        transcripts = []
        num_chunks = (len(audio) + self.chunk_duration_ms - 1) // self.chunk_duration_ms
        
        print(f"Audio is long ({len(audio)/1000/60:.1f} min), splitting into {num_chunks} chunks...")
        
        for i in range(0, len(audio), self.chunk_duration_ms):
            chunk = audio[i:i + self.chunk_duration_ms]
            chunk_num = i // self.chunk_duration_ms + 1
            
            print(f"Transcribing chunk {chunk_num}/{num_chunks}...")
            
            # Export chunk to temp file
            temp_file = audio_file.parent / f"temp_chunk_{chunk_num}.mp3"
            chunk.export(temp_file, format="mp3")
            
            try:
                # Transcribe chunk
                chunk_transcript = self._transcribe_single(temp_file, model)
                transcripts.append(chunk_transcript)
            finally:
                # Cleanup temp file
                if temp_file.exists():
                    temp_file.unlink()
        
        # Combine all transcripts
        full_transcript = " ".join(transcripts)
        return full_transcript
    
    def verify_model_available(self) -> bool:
        """
        Check if Whisper is available (always true if package is installed)
        
        Returns:
            True if whisper package is available
        """
        try:
            import whisper
            return True
        except ImportError:
            return False

