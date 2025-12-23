"""Pydantic models for request/response validation"""

from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class VideoMetadata(BaseModel):
    """Metadata about the YouTube video"""
    title: str
    duration: int  # seconds
    channel: str
    video_id: str
    url: str


class SummarizeRequest(BaseModel):
    """Request model for video summarization"""
    url: HttpUrl = Field(..., description="YouTube video URL")
    max_duration: Optional[int] = Field(None, description="Maximum video duration in seconds")


class TranscriptSegment(BaseModel):
    """Individual transcript segment with timestamp"""
    start_time: float
    end_time: float
    text: str


class SummarizeResponse(BaseModel):
    """Response model containing transcript and summary"""
    metadata: VideoMetadata
    transcript: str
    summary: str
    processing_time: float  # seconds
    transcript_word_count: int
    summary_word_count: int
