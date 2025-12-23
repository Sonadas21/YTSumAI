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
        
    def cleanup_old_files(self) -> None:
        """
        Clean up old audio files before downloading new ones
        This keeps the last downloaded file for verification
        """
        try:
            if self.download_dir.exists():
                for file in self.download_dir.glob(f"*.{self.audio_format}"):
                    try:
                        os.remove(file)
                        print(f"Cleaned up old file: {file.name}")
                    except Exception as e:
                        print(f"Failed to cleanup {file}: {str(e)}")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        
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
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': AUDIO_BITRATE.replace('k', ''),
            }],
            'outtmpl': str(self.download_dir / '%(id)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            # Additional options to bypass YouTube blocking
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }
        
        try:
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
                ydl.download([url])
                
                # Construct the output file path
                audio_file = self.download_dir / f"{info['id']}.{self.audio_format}"
                
                if not audio_file.exists():
                    raise FileNotFoundError(f"Downloaded audio file not found: {audio_file}")
                
                print(f"✅ Audio file saved: {audio_file.name} (available for verification)")
                return audio_file, metadata
                
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"Failed to download video: {str(e)}")
        except Exception as e:
            raise Exception(f"Error downloading audio: {str(e)}")
