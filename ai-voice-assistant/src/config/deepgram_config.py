"""
Deepgram configuration for voice-to-text processing
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DeepgramConfig:
    """Configuration class for Deepgram API"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY not found in environment variables")
    
    # Deepgram transcription options
    TRANSCRIPTION_OPTIONS = {
        "model": "nova-2",  # Latest model for better accuracy
        "language": "en-US",
        "smart_format": True,  # Automatically formats text
        "punctuate": True,     # Adds punctuation
        "diarize": False,      # Speaker diarization (set to True if needed)
        "filler_words": False, # Remove filler words like "um", "uh"
        "profanity_filter": False,
        "redact": False,
        "keywords": [
            # E-commerce related keywords for better recognition
            "wedding", "elegant", "casual", "formal", "dress", "shirt", "pants",
            "shoes", "accessories", "price", "discount", "size", "color",
            "order", "tracking", "delivery", "cart", "checkout", "payment"
        ],
        "keyword_boost": "legacy"  # Boost recognition of keywords
    }
    
    # Audio processing settings
    AUDIO_CONFIG = {
        "sample_rate": 16000,  # 16kHz sample rate
        "channels": 1,         # Mono audio
        "chunk_size": 1024,    # Audio chunk size for streaming
        "format": "wav"        # Audio format
    }
    
    # Real-time streaming options
    STREAMING_OPTIONS = {
        "encoding": "linear16",
        "sample_rate": 16000,
        "channels": 1,
        "interim_results": True,  # Get partial results
        "endpointing": 300,      # 300ms of silence to end utterance
        "vad_events": True,      # Voice activity detection events
        "utterance_end_ms": 1000 # End utterance after 1 second of silence
    }

# Global config instance
deepgram_config = DeepgramConfig()
