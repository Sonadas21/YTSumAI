"""Text summarization using Ollama LLM"""

import requests
from typing import List
from app.config import OLLAMA_BASE_URL, SUMMARIZATION_MODEL, MAX_SUMMARY_LENGTH, CHUNK_OVERLAP


class TextSummarizer:
    """Summarizes text using Ollama LLM with thinking capabilities"""
    
    def __init__(self):
        self.ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
        self.model = SUMMARIZATION_MODEL
        self.max_summary_length = MAX_SUMMARY_LENGTH
        
    def summarize(self, text: str) -> str:
        """
        Generate a summary of the given text
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
            
        Raises:
            Exception: If summarization fails
        """
        try:
            # Count words
            word_count = len(text.split())
            
            # For very long transcripts, use chunking strategy
            if word_count > 3000:
                return self._summarize_chunked(text)
            else:
                return self._summarize_single(text)
                
        except Exception as e:
            raise Exception(f"Summarization failed: {str(e)}")
    
    def _summarize_single(self, text: str) -> str:
        """
        Summarize text in a single request
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
        """
        prompt = f"""You are an expert at summarizing video transcripts. Your task is to create a concise, well-structured summary.

**Transcript:**
{text}

**Instructions:**
- Create a comprehensive summary in about {self.max_summary_length} words
- Organize the summary with clear sections/bullet points if appropriate
- Capture the main topics, key points, and important details
- Use clear, professional language
- Focus on the content, not the video format

**Summary:**"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
            }
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            summary = result.get('response', '').strip()
            
            if not summary:
                raise Exception("Empty summary received from model")
            
            return summary
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to communicate with Ollama: {str(e)}")
    
    def _summarize_chunked(self, text: str) -> str:
        """
        Summarize long text using map-reduce strategy
        
        Args:
            text: Long text to summarize
            
        Returns:
            Combined summary
        """
        # Split text into chunks
        words = text.split()
        chunk_size = 2000
        chunks = []
        
        for i in range(0, len(words), chunk_size - CHUNK_OVERLAP):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        print(f"Text is long ({len(words)} words), processing in {len(chunks)} chunks...")
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks, 1):
            print(f"Summarizing chunk {i}/{len(chunks)}...")
            
            chunk_prompt = f"""Summarize the following section of a video transcript. Focus on key points:

{chunk}

Summary:"""
            
            payload = {
                "model": self.model,
                "prompt": chunk_prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=300)
            response.raise_for_status()
            chunk_summary = response.json().get('response', '').strip()
            chunk_summaries.append(chunk_summary)
        
        # Combine chunk summaries into final summary
        combined = "\n\n".join(chunk_summaries)
        
        final_prompt = f"""Create a final comprehensive summary from these section summaries of a video transcript:

{combined}

Create a well-organized final summary in about {self.max_summary_length} words that captures all key points:"""

        payload = {
            "model": self.model,
            "prompt": final_prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        }
        
        response = requests.post(self.ollama_url, json=payload, timeout=300)
        response.raise_for_status()
        final_summary = response.json().get('response', '').strip()
        
        return final_summary
    
    def verify_model_available(self) -> bool:
        """
        Check if the summarization model is available in Ollama
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            list_url = f"{OLLAMA_BASE_URL}/api/tags"
            response = requests.get(list_url, timeout=10)
            response.raise_for_status()
            
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            return self.model in model_names or any(self.model in name for name in model_names)
            
        except Exception as e:
            print(f"Failed to verify model availability: {str(e)}")
            return False
