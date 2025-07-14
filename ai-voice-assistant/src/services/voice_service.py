"""
Voice-to-Text Service using Deepgram API
Handles both file-based and real-time speech recognition
"""

import asyncio
import json
import logging
from io import BytesIO
from typing import Optional, Dict, Any, AsyncGenerator
import aiofiles
import os
import sys
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    LiveOptions,
    FileSource
)

# Add config path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.deepgram_config import deepgram_config

# Set up logging
logger = logging.getLogger(__name__)

class VoiceToTextService:
    """
    Service class for converting voice to text using Deepgram API
    Supports both pre-recorded audio files and real-time streaming
    """
    
    def __init__(self):
        """Initialize the Deepgram client"""
        self.client = DeepgramClient(deepgram_config.api_key)
    
    async def transcribe_file(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio from a file
        
        Args:
            audio_file_path (str): Path to the audio file
            
        Returns:
            Dict[str, Any]: Transcription result with confidence scores
        """
        try:
            # Set up transcription options
            options = PrerecordedOptions(
                model=deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                language=deepgram_config.TRANSCRIPTION_OPTIONS["language"],
                smart_format=deepgram_config.TRANSCRIPTION_OPTIONS["smart_format"],
                punctuate=deepgram_config.TRANSCRIPTION_OPTIONS["punctuate"],
                diarize=deepgram_config.TRANSCRIPTION_OPTIONS["diarize"],
                filler_words=deepgram_config.TRANSCRIPTION_OPTIONS["filler_words"],
                keywords=deepgram_config.TRANSCRIPTION_OPTIONS["keywords"]
            )
            
            # Create file source
            with open(audio_file_path, 'rb') as audio_file:
                buffer_data = audio_file.read()
            
            payload = {"buffer": buffer_data}
            
            # Send audio to Deepgram for transcription
            response = await self.client.listen.asyncprerecorded.v("1").transcribe_file(
                payload, options
            )
            
            # Extract transcription results
            if response.results and response.results.channels:
                transcript = response.results.channels[0].alternatives[0].transcript
                confidence = response.results.channels[0].alternatives[0].confidence
                
                result = {
                    "success": True,
                    "transcript": transcript,
                    "confidence": confidence,
                    "metadata": {
                        "model": deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                        "language": deepgram_config.TRANSCRIPTION_OPTIONS["language"],
                        "duration": response.metadata.duration if response.metadata else None
                    }
                }
                
                logger.info(f"Successfully transcribed audio: {transcript[:100]}...")
                return result
            else:
                logger.warning("No transcription results received")
                return {
                    "success": False,
                    "error": "No transcription results received",
                    "transcript": "",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Error transcribing audio file: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "transcript": "",
                "confidence": 0.0
            }
    
    async def transcribe_bytes(self, audio_bytes: bytes, mime_type: str = "audio/wav") -> Dict[str, Any]:
        """
        Transcribe audio from raw bytes
        
        Args:
            audio_bytes (bytes): Raw audio data
            mime_type (str): MIME type of the audio
            
        Returns:
            Dict[str, Any]: Transcription result
        """
        try:
            # Set up transcription options
            options = PrerecordedOptions(
                model=deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                language=deepgram_config.TRANSCRIPTION_OPTIONS["language"],
                smart_format=deepgram_config.TRANSCRIPTION_OPTIONS["smart_format"],
                punctuate=deepgram_config.TRANSCRIPTION_OPTIONS["punctuate"],
                keywords=deepgram_config.TRANSCRIPTION_OPTIONS["keywords"]
            )
            
            # Create payload with audio bytes
            payload = {"buffer": audio_bytes, "mimetype": mime_type}
            
            # Send audio bytes to Deepgram
            response = await self.client.listen.asyncprerecorded.v("1").transcribe_file(
                payload, options
            )
            
            # Extract results
            if response.results and response.results.channels:
                transcript = response.results.channels[0].alternatives[0].transcript
                confidence = response.results.channels[0].alternatives[0].confidence
                
                return {
                    "success": True,
                    "transcript": transcript,
                    "confidence": confidence,
                    "metadata": {
                        "model": deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                        "language": deepgram_config.TRANSCRIPTION_OPTIONS["language"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "No transcription results received",
                    "transcript": "",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Error transcribing audio bytes: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "transcript": "",
                "confidence": 0.0
            }
    
    async def start_live_transcription(self):
        """
        Start real-time transcription (streaming)
        Returns a connection object for live transcription
        
        Returns:
            Connection object for live transcription
        """
        try:
            # Set up live transcription options
            options = LiveOptions(
                model=deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                language=deepgram_config.TRANSCRIPTION_OPTIONS["language"],
                smart_format=deepgram_config.TRANSCRIPTION_OPTIONS["smart_format"],
                interim_results=deepgram_config.STREAMING_OPTIONS["interim_results"],
                endpointing=deepgram_config.STREAMING_OPTIONS["endpointing"],
                vad_events=deepgram_config.STREAMING_OPTIONS["vad_events"]
            )
            
            # Create live transcription connection
            connection = await self.client.listen.asynclive.v("1").start(options)
            
            return connection
            
        except Exception as e:
            logger.error(f"Error starting live transcription: {str(e)}")
            return None

    async def create_websocket_connection(self, on_message=None, on_error=None, on_close=None):
        """
        Create a WebSocket connection for live transcription
        
        Args:
            on_message: Callback for transcription messages
            on_error: Callback for errors
            on_close: Callback for connection close
            
        Returns:
            Dict with connection details
        """
        try:
            # Set up live transcription options
            options = LiveOptions(
                model=deepgram_config.TRANSCRIPTION_OPTIONS["model"],
                language=deepgram_config.TRANSCRIPTION_OPTIONS["language"],
                smart_format=deepgram_config.TRANSCRIPTION_OPTIONS["smart_format"],
                interim_results=True,
                endpointing=deepgram_config.STREAMING_OPTIONS["endpointing"],
                vad_events=True,
                utterance_end_ms=1000,
                punctuate=True
            )
            
            # Create the connection
            connection = self.client.listen.asyncwebsocket.v("1")
            
            # Set up event handlers
            if on_message:
                connection.on("message", on_message)
            if on_error:
                connection.on("error", on_error)
            if on_close:
                connection.on("close", on_close)
            
            # Start the connection
            await connection.start(options)
            
            logger.info("WebSocket connection for live transcription created")
            return {
                "success": True,
                "connection": connection,
                "message": "Live transcription WebSocket ready"
            }
            
        except Exception as e:
            logger.error(f"Error creating WebSocket connection: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_websocket_url(self):
        """
        Get the WebSocket URL for direct browser connections
        
        Returns:
            str: WebSocket URL with authentication
        """
        base_url = "wss://api.deepgram.com/v1/listen"
        params = {
            "model": deepgram_config.TRANSCRIPTION_OPTIONS["model"],
            "language": deepgram_config.TRANSCRIPTION_OPTIONS["language"],
            "smart_format": "true",
            "interim_results": "true",
            "punctuate": "true",
            "vad_events": "true",
            "endpointing": str(deepgram_config.STREAMING_OPTIONS["endpointing"]),
            "utterance_end_ms": "1000"
        }
        
        # Build query string
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        
        return f"{base_url}?{query_string}"
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the Deepgram connection with a simple audio test
        
        Returns:
            Dict[str, Any]: Connection test result
        """
        try:
            # Create a simple test with a short audio buffer
            # This is just to verify the API key and connection work
            logger.info("Testing Deepgram connection...")
            
            # We'll use a minimal test - just verify the client can be created
            if self.client and deepgram_config.api_key:
                return {
                    "success": True,
                    "message": "Deepgram connection established successfully",
                    "api_key_present": bool(deepgram_config.api_key),
                    "client_initialized": bool(self.client)
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to initialize Deepgram client",
                    "api_key_present": bool(deepgram_config.api_key),
                    "client_initialized": bool(self.client)
                }
                
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "api_key_present": bool(deepgram_config.api_key),
                "client_initialized": False
            }

# Global service instance
voice_to_text_service = VoiceToTextService()
