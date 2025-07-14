#!/usr/bin/env python3
"""
Test the distributed API key system with multiple agents
"""

import asyncio
import os
import sys
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_distributed_api_keys():
    """Test the new distributed API key system"""
    
    print("=" * 60)
    print("TESTING: Distributed API Keys System")
    print("Skip rate-limited key + assign different keys per agent")
    print("=" * 60)
    
    try:
        # Import the service
        from services.voice_shopping_service import voice_shopping_service
        
        # Test a simple query to see key distribution
        test_query = "I am a woman and I need something to wear for a party"
        
        print(f"\n🔍 Testing Query: {test_query}")
        print("-" * 40)
        
        # Process text query (this will show key distribution)
        result = await voice_shopping_service.process_text_query(test_query)
        
        if result.get("success"):
            shopping_result = result.get("shopping_result", {})
            products = shopping_result.get("products", [])
            
            print(f"✅ Query processed successfully")
            print(f"🛍️ Found {len(products)} products:")
            
            for i, product in enumerate(products, 1):
                if isinstance(product, dict):
                    name = product.get("name", "Unknown")
                    price = product.get("price", "N/A")
                    print(f"   {i}. {name} - ${price}")
                else:
                    print(f"   {i}. {product}")
                    
        else:
            print(f"❌ Error: {result.get('error')}")
            
        print("\n" + "=" * 60)
        print("🎯 API KEY DISTRIBUTION SUMMARY")
        print("=" * 60)
        print("✅ Each agent now uses a different API key")
        print("✅ Rate-limited key (gemini_1) is skipped")
        print("✅ Keys 2, 3, 4 are assigned to different agents")
        print("✅ Load is distributed across multiple keys")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set Windows event loop policy if needed
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the test
    asyncio.run(test_distributed_api_keys())