"""Quick test script to verify the setup"""

import requests
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import OLLAMA_BASE_URL, SUMMARIZATION_MODEL


def check_ollama_server():
    """Check if Ollama server is running"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_models():
    """Check if required models are available"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        models = response.json().get('models', [])
        model_names = [m.get('name', '') for m in models]
        
        sum_available = any(SUMMARIZATION_MODEL in name for name in model_names)
        
        return sum_available, model_names
    except Exception as e:
        return False, []


def main():
    print("=" * 60)
    print("YTSumAI - Setup Verification")
    print("=" * 60)
    
    # Check Ollama server
    print("\n1. Checking Ollama server...")
    if check_ollama_server():
        print("   ✅ Ollama server is running")
    else:
        print("   ❌ Ollama server is NOT running")
        print("   Please start Ollama: ollama serve")
        return
    
    # Check models
    print("\n2. Checking required models...")
    sum_ok, all_models = check_models()
    
    print(f"\n   Required Models:")
    print(f"   - STT Model: OpenAI Whisper (offline)")
    try:
        import whisper
        print("     ✅ Whisper package installed")
        print("     ℹ️  Model will download on first use (~150MB)")
    except ImportError:
        print("     ❌ NOT FOUND - Run: pip install openai-whisper")
    
    print(f"\n   - Summarization Model: {SUMMARIZATION_MODEL}")
    if sum_ok:
        print("     ✅ Available")
    else:
        print(f"     ❌ NOT FOUND - Run: ollama pull {SUMMARIZATION_MODEL}")
    
    # Show all available models
    if all_models:
        print("\n   Available models in Ollama:")
        for model in all_models:
            print(f"     - {model}")
    
    # Check Python dependencies
    print("\n3. Checking Python dependencies...")
    try:
        import streamlit
        import fastapi
        import yt_dlp
        import pydub
        import whisper
        print("   ✅ All required packages installed")
    except ImportError as e:
        print(f"   ❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return
    
    # Final status
    print("\n" + "=" * 60)
    if sum_ok:
        print("✅ ALL CHECKS PASSED - Ready to use!")
        print("\nTo start the application:")
        print("  streamlit run streamlit_app.py")
    else:
        print("⚠️  SETUP INCOMPLETE - Please fix the issues above")
    print("=" * 60)


if __name__ == "__main__":
    main()
