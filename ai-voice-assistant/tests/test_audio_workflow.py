#!/usr/bin/env python3
"""
Test gajala.wav with Deepgram + CrewAI Pipeline
Complete voice-to-shopping workflow test
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_audio_with_crew():
    """Test the complete audio workflow: Deepgram -> CrewAI"""
    
    print("🎵" + "=" * 60)
    print("TESTING: Audio File (gajala.wav) -> Deepgram -> CrewAI")
    print("Complete voice shopping workflow")
    print("=" * 60)
    
    try:
        # Check if audio file exists
        audio_file_path = "gajala.wav"
        if not os.path.exists(audio_file_path):
            print(f"❌ Audio file not found: {audio_file_path}")
            return
        
        print(f"🎵 Audio file found: {audio_file_path}")
        
        # Import services
        from services.voice_service import voice_to_text_service
        from services.voice_shopping_service import voice_shopping_service
        
        # Step 1: Test Deepgram connection
        print(f"\n🔗 Step 1: Testing Deepgram Connection...")
        connection_test = await voice_to_text_service.test_connection()
        
        if connection_test.get("success"):
            print(f"✅ Deepgram connection successful")
        else:
            print(f"❌ Deepgram connection failed: {connection_test.get('error')}")
            return
        
        # Step 2: Transcribe audio file
        print(f"\n🎙️ Step 2: Transcribing audio with Deepgram...")
        transcription_result = await voice_to_text_service.transcribe_file(audio_file_path)
        
        if not transcription_result.get("success"):
            print(f"❌ Transcription failed: {transcription_result.get('error')}")
            return
        
        transcript = transcription_result.get("transcript", "")
        confidence = transcription_result.get("confidence", 0.0)
        
        print(f"✅ Transcription successful!")
        print(f"📝 Transcript: '{transcript}'")
        print(f"🎯 Confidence: {confidence:.2%}")
        
        if not transcript.strip():
            print("❌ Empty transcript - cannot proceed with shopping query")
            return
        
        # Step 3: Process through CrewAI pipeline
        print(f"\n🤖 Step 3: Processing through CrewAI Pipeline...")
        print(f"🔍 Query: '{transcript}'")
        print("-" * 50)
        
        # Use the voice shopping service to process the transcript
        shopping_result = await voice_shopping_service.process_text_query(transcript)
        
        if shopping_result.get("success"):
            # Extract products from the nested structure
            products_data = shopping_result.get("shopping_result", {})
            products = products_data.get("products", [])
            response_text = shopping_result.get("response", "No response generated")
            
            print(f"✅ CrewAI processing successful!")
            print(f"🛍️ Found {len(products)} products:")
            
            # Display products
            if products:
                for i, product in enumerate(products, 1):
                    if isinstance(product, dict):
                        name = product.get("name", "Unknown Product")
                        price = product.get("price", "N/A")
                        color = product.get("color", "N/A")
                        category = product.get("category", "N/A")
                        print(f"   {i}. {name}")
                        print(f"      💰 Price: ${price}")
                        print(f"      🎨 Color: {color}")
                        print(f"      📁 Category: {category}")
                        print()
                    else:
                        print(f"   {i}. {product}")
            else:
                print("   📭 No products found matching the criteria")
            
            print(f"🗣️ Assistant Response:")
            print(f"   {response_text}")
            
        else:
            print(f"❌ CrewAI processing failed: {shopping_result.get('error')}")
        
        # Step 4: Summary
        print(f"\n" + "=" * 60)
        print(f"🎯 COMPLETE WORKFLOW SUMMARY")
        print(f"=" * 60)
        print(f"✅ Audio File: {audio_file_path}")
        print(f"✅ Deepgram Transcription: '{transcript[:50]}...' (confidence: {confidence:.1%})")
        print(f"✅ CrewAI Processing: {'Success' if shopping_result.get('success') else 'Failed'}")
        print(f"✅ Products Found: {len(products) if shopping_result.get('success') else 0}")
        print(f"✅ API Key Distribution: Intent→gemini_2, Search→gemini_3, Response→gemini_4")
        
    except Exception as e:
        print(f"❌ Error in audio workflow: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_deepgram_only():
    """Test just the Deepgram transcription of gajala.wav"""
    
    print(f"\n🎙️ DEEPGRAM-ONLY TEST")
    print("-" * 30)
    
    try:
        # Check if audio file exists
        audio_file_path = "gajala.wav"
        if not os.path.exists(audio_file_path):
            print(f"❌ Audio file not found: {audio_file_path}")
            return
        
        # Import voice service
        from services.voice_service import voice_to_text_service
        
        # Get file info
        file_size = os.path.getsize(audio_file_path)
        print(f"📁 File: {audio_file_path} ({file_size} bytes)")
        
        # Transcribe
        result = await voice_to_text_service.transcribe_file(audio_file_path)
        
        if result.get("success"):
            transcript = result.get("transcript", "")
            confidence = result.get("confidence", 0.0)
            metadata = result.get("metadata", {})
            
            print(f"✅ Transcription successful!")
            print(f"📝 Full transcript: '{transcript}'")
            print(f"🎯 Confidence score: {confidence:.3f}")
            print(f"⏱️ Duration: {metadata.get('duration', 'Unknown')} seconds")
            print(f"🤖 Model: {metadata.get('model', 'Unknown')}")
            print(f"🌍 Language: {metadata.get('language', 'Unknown')}")
        else:
            print(f"❌ Transcription failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error in Deepgram test: {str(e)}")

if __name__ == "__main__":
    # Set Windows event loop policy if needed
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    async def main():
        # Test 1: Deepgram only
        await test_deepgram_only()
        
        print("\n" + "="*80 + "\n")
        
        # Test 2: Complete workflow
        await test_audio_with_crew()
    
    # Run the tests
    asyncio.run(main())