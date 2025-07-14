"""
API Key Load Balancer
Manages multiple API keys to distribute load and avoid rate limits
"""

import os
import random
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from collections import defaultdict

logger = logging.getLogger(__name__)

class ProviderType(Enum):
    GEMINI = "gemini"

@dataclass
class APIKeyInfo:
    """Information about an API key"""
    key: str
    provider: ProviderType
    usage_count: int = 0
    last_used: float = 0
    is_available: bool = True
    rpm_limit: int = 100  # requests per minute
    current_minute_count: int = 0
    minute_start: float = 0

class APIKeyManager:
    """Manages API keys with load balancing and rate limiting"""
    
    def __init__(self):
        self.api_keys: Dict[str, APIKeyInfo] = {}
        self.provider_keys: Dict[ProviderType, List[str]] = defaultdict(list)
        self.load_api_keys()
        
    def load_api_keys(self):
        """Load API keys from environment variables"""
        # Load Gemini keys (now supporting up to 6 keys)
        for i in range(1, 7):  # GEMINI_API_KEY_1 through GEMINI_API_KEY_6
            key = os.getenv(f"GEMINI_API_KEY_{i}")
            if key:
                key_id = f"gemini_{i}"
                self.api_keys[key_id] = APIKeyInfo(
                    key=key,
                    provider=ProviderType.GEMINI,
                    rpm_limit=60  # Gemini typically has lower limits
                )
                self.provider_keys[ProviderType.GEMINI].append(key_id)
                logger.info(f"Loaded Gemini API key {i}")
        
        logger.info(f"Total API keys loaded: {len(self.api_keys)}")
        logger.info(f"Gemini keys: {len(self.provider_keys[ProviderType.GEMINI])}")
    
    def _reset_minute_counters(self, key_info: APIKeyInfo):
        """Reset rate limit counters if a minute has passed"""
        current_time = time.time()
        if current_time - key_info.minute_start >= 60:
            key_info.current_minute_count = 0
            key_info.minute_start = current_time
    
    def get_available_key(self, provider: ProviderType, agent_name: str = None) -> Optional[str]:
        """Get an available API key for the specified provider"""
        available_keys = []
        
        for key_id in self.provider_keys[provider]:
            key_info = self.api_keys[key_id]
            self._reset_minute_counters(key_info)
            
            # Skip the rate-limited key (gemini_1 based on the previous error)
            if key_id == "gemini_1":
                logger.debug(f"Skipping rate-limited key: {key_id}")
                continue
            
            # Check if key is available and under rate limit
            if (key_info.is_available and 
                key_info.current_minute_count < key_info.rpm_limit):
                available_keys.append((key_id, key_info))
        
        if not available_keys:
            logger.warning(f"No available {provider.value} keys found for {agent_name}")
            # Emergency fallback: try any key except gemini_1
            for key_id in self.provider_keys[provider]:
                if key_id != "gemini_1":
                    key_info = self.api_keys[key_id]
                    if key_info.is_available:
                        logger.warning(f"Emergency fallback: using {key_id} for {agent_name}")
                        return key_info.key
            return None
        
        # For agent-specific assignment, try to maintain consistency
        if agent_name:
            # Try to assign specific keys to specific agents
            preferred_keys = {
                'intent_analyzer': 'gemini_2',
                'database_search': 'gemini_3', 
                'response_generator': 'gemini_5'  # Changed from gemini_4 to gemini_5
            }
            
            preferred_key_id = preferred_keys.get(agent_name)
            if preferred_key_id:
                for key_id, key_info in available_keys:
                    if key_id == preferred_key_id:
                        # Update usage statistics
                        key_info.usage_count += 1
                        key_info.current_minute_count += 1
                        key_info.last_used = time.time()
                        
                        logger.info(f"Assigned {preferred_key_id} to {agent_name}")
                        return key_info.key
        
        # Fallback: Sort by usage count (least used first) and last used time
        available_keys.sort(key=lambda x: (x[1].usage_count, x[1].last_used))
        
        # Select the least used key
        selected_key_id, selected_key_info = available_keys[0]
        
        # Update usage statistics
        selected_key_info.usage_count += 1
        selected_key_info.current_minute_count += 1
        selected_key_info.last_used = time.time()
        
        logger.info(f"Assigned {selected_key_id} to {agent_name or 'unknown agent'}")
        return selected_key_info.key
    
    def mark_key_error(self, api_key: str, error_type: str = "rate_limit"):
        """Mark a key as having an error"""
        for key_id, key_info in self.api_keys.items():
            if key_info.key == api_key:
                if error_type == "rate_limit":
                    # Temporarily disable key for rate limit
                    key_info.is_available = False
                    # Re-enable after 1 minute
                    asyncio.create_task(self._re_enable_key(key_id, 60))
                elif error_type == "invalid":
                    # Disable key permanently for invalid key errors
                    key_info.is_available = False
                logger.warning(f"Marked {key_id} as {error_type} error")
                break
    
    async def _re_enable_key(self, key_id: str, delay: int):
        """Re-enable a key after a delay"""
        await asyncio.sleep(delay)
        if key_id in self.api_keys:
            self.api_keys[key_id].is_available = True
            logger.info(f"Re-enabled {key_id}")
    
    def get_key_for_agent(self, agent_name: str) -> Optional[str]:
        """Get a dedicated API key for a specific agent"""
        # Dedicated agent assignments to avoid rate limiting
        agent_assignments = {
            "intent_agent": "gemini_1",
            "product_query_agent": "gemini_2", 
            "advisor_agent": "gemini_3",
            "order_status_agent": "gemini_4",
            "coordinator_agent": "gemini_5",
            # gemini_6 as backup/spare
        }
        
        # Get dedicated key for this agent
        assigned_key_id = agent_assignments.get(agent_name)
        
        if assigned_key_id and assigned_key_id in self.api_keys:
            key_info = self.api_keys[assigned_key_id]
            self._reset_minute_counters(key_info)
            
            # Check if dedicated key is available
            if key_info.is_available and key_info.current_minute_count < key_info.rpm_limit:
                key_info.usage_count += 1
                key_info.current_minute_count += 1
                key_info.last_used = time.time()
                logger.info(f"Using dedicated key {assigned_key_id} for agent {agent_name}")
                return key_info.key
            else:
                logger.warning(f"Dedicated key {assigned_key_id} for agent {agent_name} is rate limited")
        
        # Fallback: try to get any available Gemini key
        backup_key = self.get_available_key(ProviderType.GEMINI, agent_name)
        if backup_key:
            logger.info(f"Using backup key for agent {agent_name}")
            return backup_key
        
        logger.error(f"No available API keys for agent {agent_name}")
        return None
    
    def get_usage_stats(self) -> Dict:
        """Get usage statistics for all keys"""
        stats = {
            "total_keys": len(self.api_keys),
            "available_keys": sum(1 for k in self.api_keys.values() if k.is_available),
            "providers": {},
            "keys": {}
        }
        
        for provider in ProviderType:
            provider_keys = self.provider_keys[provider]
            available_count = sum(1 for k_id in provider_keys 
                                if self.api_keys[k_id].is_available)
            stats["providers"][provider.value] = {
                "total": len(provider_keys),
                "available": available_count,
                "usage": sum(self.api_keys[k_id].usage_count for k_id in provider_keys)
            }
        
        for key_id, key_info in self.api_keys.items():
            stats["keys"][key_id] = {
                "provider": key_info.provider.value,
                "usage_count": key_info.usage_count,
                "current_minute_count": key_info.current_minute_count,
                "is_available": key_info.is_available,
                "rpm_limit": key_info.rpm_limit
            }
        
        return stats

# Global API key manager instance
api_key_manager = APIKeyManager()
