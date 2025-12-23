"""FastAPI application for YTSumAI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import SUMMARIZATION_MODEL

# Create FastAPI app
app = FastAPI(
    title="YTSumAI",
    description="Offline YouTube Video Summarizer using local AI models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "YTSumAI",
        "description": "Offline YouTube Video Summarizer",
        "version": "1.0.0",
        "models": {
            "stt": "OpenAI Whisper (offline)",
            "summarization": SUMMARIZATION_MODEL
        },
        "endpoints": {
            "health": "/api/health",
            "models": "/api/models",
            "summarize": "/api/summarize (POST)"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Startup event to verify configuration"""
    print("=" * 60)
    print("YTSumAI - Offline YouTube Video Summarizer")
    print("=" * 60)
    print(f"STT Model: OpenAI Whisper (offline)")
    print(f"Summarization Model: {SUMMARIZATION_MODEL}")
    print("=" * 60)
    print("API is ready!")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
