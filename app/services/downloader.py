"""YouTube audio downloader using yt-dlp"""

import os
from pathlib import Path
from typing import Tuple, Dict
import yt_dlp
from app.config import DOWNLOAD_DIR, AUDIO_FORMAT, AUDIO_BITRATE, MAX_VIDEO_DURATION
from app.models.schemas import VideoMetadata


class YouTubeDownloader:
    """Downloads audio from YouTube videos"""
    
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
        self.audio_format = AUDIO_FORMAT
        
    def cleanup_old_files(self, keep_video_id: str = None) -> None:
        """
        Clean up old audio files before downloading new ones
        
        Args:
            keep_video_id: Optional video ID to keep, delete all others
        """
        try:
            if self.download_dir.exists():
                for ext in ['mp3', 'wav', 'm4a']:
                    for file in self.download_dir.glob(f"*.{ext}"):
                        # If keep_video_id is specified, skip that file
                        if keep_video_id and keep_video_id in file.stem:
                            continue
                        try:
                            os.remove(file)
                            print(f"Cleaned up old file: {file.name}")
                        except Exception as e:
                            print(f"Failed to cleanup {file}: {str(e)}")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        
    def _validate_audio_file(self, audio_file: Path) -> bool:
        """
        Validate audio file using ffprobe
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            True if file is valid, False otherwise
        """
        import subprocess
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 
                 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 
                 str(audio_file)],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and result.stdout.strip() != ''
        except Exception as e:
            print(f"Audio validation failed: {e}")
            return False
    
    def download_audio(self, url: str) -> Tuple[Path, VideoMetadata]:
        """
        Download audio from YouTube video
        
        Args:
            url: YouTube video URL
            
        Returns:
            Tuple of (audio_file_path, video_metadata)
            
        Raises:
            Exception: If download fails or video is too long
        """
        # Clean up old files before downloading new ones
        self.cleanup_old_files()
        
        # Try MP3 first, fallback to WAV if it fails
        formats_to_try = [
            ('mp3', AUDIO_BITRATE.replace('k', '')),
            ('wav', '192')  # WAV as fallback
        ]
        
        last_error = None
        
        for audio_format, quality in formats_to_try:
            try:
                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': audio_format,
                        'preferredquality': quality,
                    }],
                    'outtmpl': str(self.download_dir / '%(id)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': False,
                    # Additional options to bypass YouTube blocking
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                    'prefer_ffmpeg': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract video info first
                    info = ydl.extract_info(url, download=False)
                    
                    # Check video duration
                    duration = info.get('duration', 0)
                    if duration > MAX_VIDEO_DURATION:
                        raise ValueError(
                            f"Video duration ({duration}s) exceeds maximum allowed "
                            f"({MAX_VIDEO_DURATION}s)"
                        )
                    
                    # Create metadata
                    metadata = VideoMetadata(
                        title=info.get('title', 'Unknown'),
                        duration=duration,
                        channel=info.get('uploader', 'Unknown'),
                        video_id=info.get('id', ''),
                        url=url
                    )
                    
                    # Download the audio
                    print(f"Downloading audio as {audio_format.upper()}...")
                    ydl.download([url])
                    
                    # Construct the output file path
                    audio_file = self.download_dir / f"{info['id']}.{audio_format}"
                    
                    if not audio_file.exists():
                        raise FileNotFoundError(f"Downloaded audio file not found: {audio_file}")
                    
                    # Validate the downloaded file
                    print(f"Validating audio file...")
                    if not self._validate_audio_file(audio_file):
                        raise Exception(f"Downloaded {audio_format} file is corrupted or invalid")
                    
                    # Check file size (should be > 1KB)
                    if audio_file.stat().st_size < 1024:
                        raise Exception(f"Downloaded file is too small ({audio_file.stat().st_size} bytes)")
                    
                    print(f"✅ Audio file saved and validated: {audio_file.name}")
                    return audio_file, metadata
                    
            except Exception as e:
                last_error = e
                print(f"Failed to download as {audio_format}: {str(e)}")
                if audio_format != formats_to_try[-1][0]:
                    print(f"Trying fallback format...")
                continue
        
        # If we get here, all formats failed
        raise Exception(f"Failed to download audio in any format. Last error: {str(last_error)}")
