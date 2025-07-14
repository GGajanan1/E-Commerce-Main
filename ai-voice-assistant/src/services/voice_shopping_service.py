"""
Voice Shopping Service - Main orchestrator for voice-based e-commerce
Integrates Deepgram voice-to-text with CrewAI shopping agents
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
import tempfile
import os
import sys

# Add parent directories to path
current_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(src_dir)
sys.path.extend([src_dir, root_dir])

from services.voice_service import voice_to_text_service
from crews.voice_shopping_crew import VoiceShoppingCrew

logger = logging.getLogger(__name__)

class VoiceShoppingService:
    """
    Main service that orchestrates voice shopping workflow:
    1. Voice Input (audio file or stream) -> Deepgram
    2. Deepgram transcription -> Intent Agent
    3. Intent Agent -> Product Search Agent -> Response
    """
    
    def __init__(self):
        """Initialize the voice shopping service"""
        self.voice_service = voice_to_text_service
        self.shopping_crew = VoiceShoppingCrew()
        
    async def process_voice_file(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process voice shopping request from audio file
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            Dict[str, Any]: Complete shopping response with products
        """
        try:
            logger.info(f"Processing voice file: {audio_file_path}")
            
            # Step 1: Convert voice to text using Deepgram
            transcription_result = await self.voice_service.transcribe_file(audio_file_path)
            
            if not transcription_result.get("success"):
                return {
                    "success": False,
                    "error": f"Voice transcription failed: {transcription_result.get('error')}",
                    "stage": "voice_to_text"
                }
            
            transcript = transcription_result.get("transcript", "").strip()
            confidence = transcription_result.get("confidence", 0.0)
            
            logger.info(f"Transcription: '{transcript}' (confidence: {confidence})")
            
            if not transcript:
                return {
                    "success": False,
                    "error": "No speech detected in audio",
                    "stage": "voice_to_text"
                }
            
            # Step 2: Process transcript through CrewAI shopping pipeline
            shopping_result = await self._process_text_query(transcript)
            
            # Step 3: Combine voice metadata with shopping results
            return {
                "success": True,
                "voice_input": {
                    "transcript": transcript,
                    "confidence": confidence,
                    "metadata": transcription_result.get("metadata", {})
                },
                "shopping_result": shopping_result
            }
            
        except Exception as e:
            logger.error(f"Error processing voice file: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "stage": "processing"
            }
    
    async def process_voice_bytes(self, audio_bytes: bytes, mime_type: str = "audio/wav") -> Dict[str, Any]:
        """
        Process voice shopping request from audio bytes
        
        Args:
            audio_bytes (bytes): Raw audio data
            mime_type (str): Audio MIME type
            
        Returns:
            Dict[str, Any]: Complete shopping response
        """
        try:
            logger.info(f"Processing voice bytes ({len(audio_bytes)} bytes)")
            
            # Step 1: Convert voice to text using Deepgram
            transcription_result = await self.voice_service.transcribe_bytes(audio_bytes, mime_type)
            
            if not transcription_result.get("success"):
                return {
                    "success": False,
                    "error": f"Voice transcription failed: {transcription_result.get('error')}",
                    "stage": "voice_to_text"
                }
            
            transcript = transcription_result.get("transcript", "").strip()
            confidence = transcription_result.get("confidence", 0.0)
            
            logger.info(f"Transcription: '{transcript}' (confidence: {confidence})")
            
            if not transcript:
                return {
                    "success": False,
                    "error": "No speech detected in audio",
                    "stage": "voice_to_text"
                }
            
            # Step 2: Process transcript through CrewAI shopping pipeline
            shopping_result = await self._process_text_query(transcript)
            
            # Step 3: Combine results
            return {
                "success": True,
                "voice_input": {
                    "transcript": transcript,
                    "confidence": confidence,
                    "metadata": transcription_result.get("metadata", {})
                },
                "shopping_result": shopping_result
            }
            
        except Exception as e:
            logger.error(f"Error processing voice bytes: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "stage": "processing"
            }
    
    async def process_text_query(self, text_query: str) -> Dict[str, Any]:
        """
        Process text shopping query directly (bypass voice-to-text)
        
        Args:
            text_query (str): User's shopping query as text
            
        Returns:
            Dict[str, Any]: Shopping response
        """
        try:
            logger.info(f"Processing text query: '{text_query}'")
            
            shopping_result = await self._process_text_query(text_query)
            
            return {
                "success": True,
                "text_input": {
                    "query": text_query
                },
                "shopping_result": shopping_result
            }
            
        except Exception as e:
            logger.error(f"Error processing text query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "stage": "text_processing"
            }
    
    async def _process_text_query(self, query: str) -> Dict[str, Any]:
        """
        Internal method to process text through CrewAI shopping pipeline
        
        Args:
            query (str): User query text
            
        Returns:
            Dict[str, Any]: Shopping result from CrewAI
        """
        try:
            logger.info(f"Running CrewAI pipeline for: '{query}'")
            
            # Run the CrewAI shopping crew using the correct method
            crew_result = self.shopping_crew.process_text_request(query)
            
            # Parse crew result
            if isinstance(crew_result, str):
                # Try to parse as JSON if it's a string
                try:
                    parsed_result = json.loads(crew_result)
                    return {
                        "success": True,
                        "products": parsed_result.get("products", []),
                        "intent": parsed_result.get("intent", {}),
                        "message": parsed_result.get("message", ""),
                        "raw_response": crew_result
                    }
                except json.JSONDecodeError:
                    # If not JSON, treat as plain text response
                    return {
                        "success": True,
                        "message": crew_result,
                        "products": [],
                        "intent": {},
                        "raw_response": crew_result
                    }
            else:
                # Direct dict/object result
                return {
                    "success": True,
                    "products": crew_result.get("products", []) if hasattr(crew_result, 'get') else [],
                    "intent": crew_result.get("intent", {}) if hasattr(crew_result, 'get') else {},
                    "message": str(crew_result),
                    "raw_response": crew_result
                }
                
        except Exception as e:
            logger.error(f"Error in CrewAI pipeline: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "products": [],
                "intent": {},
                "message": f"Failed to process query: {str(e)}"
            }
    
    async def start_live_shopping(self, on_transcription=None, on_result=None):
        """
        Start live voice shopping session with real-time transcription
        
        Args:
            on_transcription: Callback for transcription events
            on_result: Callback for shopping results
            
        Returns:
            WebSocket connection for live audio streaming
        """
        try:
            logger.info("Starting live voice shopping session")
            
            # Create callback for handling transcription
            async def handle_transcription(message):
                try:
                    data = json.loads(message)
                    
                    # Check if this is a final transcript
                    if data.get("is_final"):
                        transcript = data.get("channel", {}).get("alternatives", [{}])[0].get("transcript", "")
                        
                        if transcript.strip():
                            logger.info(f"Final transcript: {transcript}")
                            
                            # Trigger transcription callback
                            if on_transcription:
                                await on_transcription(transcript)
                            
                            # Process through shopping pipeline
                            shopping_result = await self._process_text_query(transcript)
                            
                            # Trigger result callback
                            if on_result:
                                await on_result({
                                    "transcript": transcript,
                                    "shopping_result": shopping_result
                                })
                                
                except Exception as e:
                    logger.error(f"Error handling transcription: {str(e)}")
            
            # Create WebSocket connection
            connection_result = await self.voice_service.create_websocket_connection(
                on_message=handle_transcription
            )
            
            if connection_result.get("success"):
                return connection_result.get("connection")
            else:
                raise Exception(connection_result.get("error", "Failed to create WebSocket connection"))
                
        except Exception as e:
            logger.error(f"Error starting live shopping: {str(e)}")
            return None
    
    async def test_voice_shopping(self, test_audio_path: str = None) -> Dict[str, Any]:
        """
        Test the complete voice shopping pipeline
        
        Args:
            test_audio_path (str): Optional path to test audio file
            
        Returns:
            Dict[str, Any]: Test results
        """
        try:
            logger.info("Testing voice shopping pipeline")
            
            # Test 1: Text query (bypass voice)
            text_result = await self.process_text_query("I want a red dress for a party")
            
            results = {
                "text_test": text_result,
                "voice_test": None,
                "deepgram_test": None
            }
            
            # Test 2: Deepgram connection
            deepgram_test = await self.voice_service.test_connection()
            results["deepgram_test"] = deepgram_test
            
            # Test 3: Voice file (if provided)
            if test_audio_path and os.path.exists(test_audio_path):
                voice_result = await self.process_voice_file(test_audio_path)
                results["voice_test"] = voice_result
            
            return {
                "success": True,
                "tests": results,
                "message": "Voice shopping pipeline test completed"
            }
            
        except Exception as e:
            logger.error(f"Error testing voice shopping: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Voice shopping test failed"
            }

# Global service instance
voice_shopping_service = VoiceShoppingService()
