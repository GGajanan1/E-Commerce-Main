"""
4-Step Voice Shopping Agents
Clean CrewAI agents for the linear pipeline with distributed API keys
"""

import os
from crewai import Agent, LLM
from src.tools.schema_intent_tool import intent_analyzer_tool
from src.tools.real_mcp_product_tool import real_mcp_product_search_tool
from src.services.api_key_manager import APIKeyManager, ProviderType
import logging

logger = logging.getLogger(__name__)

class VoiceShoppingAgents:
    """Factory for creating the 4-step pipeline agents with distributed API keys"""
    
    def __init__(self):
        """Initialize with distributed LLM configurations"""
        self.api_key_manager = APIKeyManager()
        
        # Create separate LLM instances for each agent to distribute load
        # Skip the rate-limited key and use different keys for each agent
        self.agent_keys = {
            'intent': self._get_agent_key('intent_analyzer'),
            'search': self._get_agent_key('database_search'),
            'response': self._get_agent_key('response_generator')
        }
        
        # Create LLM instances for each agent with fallback
        self.llms = {
            'intent': self._create_llm_with_fallback('intent_analyzer'),
            'search': self._create_llm_with_fallback('database_search'),
            'response': self._create_llm_with_fallback('response_generator')
        }
        
        print(f"🔑 Agent Key Distribution:")
        print(f"  Intent Agent: ...{self.agent_keys['intent'][-10:]}")
        print(f"  Search Agent: ...{self.agent_keys['search'][-10:]}")
        print(f"  Response Agent: ...{self.agent_keys['response'][-10:]}")
    
    def _get_agent_key(self, agent_name: str) -> str:
        """Get a specific API key for an agent with fallback"""
        api_key = self.api_key_manager.get_available_key(ProviderType.GEMINI, agent_name)
        
        if not api_key:
            # Fallback to any available key
            logger.warning(f"No preferred key for {agent_name}, trying fallback")
            api_key = self.api_key_manager.get_available_key(ProviderType.GEMINI)
            
        if not api_key:
            # Last resort: use the first available key regardless of rate limits
            logger.warning(f"No available keys found, using emergency fallback")
            for key_id, key_info in self.api_key_manager.api_keys.items():
                if key_info.provider == ProviderType.GEMINI and key_id != "gemini_1":
                    api_key = key_info.key
                    break
                    
        if not api_key:
            raise ValueError(f"No API keys available for {agent_name}")
            
        return api_key
    
    def _create_llm_with_fallback(self, agent_name: str) -> LLM:
        """Create LLM with error handling and fallback"""
        api_key = self._get_agent_key(agent_name)
        
        try:
            return LLM(
                model="gemini/gemini-2.0-flash",
                api_key=api_key,
                temperature=0.7,
                max_tokens=1024
            )
        except Exception as e:
            logger.error(f"Failed to create LLM for {agent_name}: {e}")
            # Try with a different model or key
            fallback_key = self._get_agent_key(f"{agent_name}_fallback")
            return LLM(
                model="gemini/gemini-1.5-flash",  # Fallback to older model
                api_key=fallback_key,
                temperature=0.7,
                max_tokens=1024
            )
    
    def voice_transcription_agent(self):
        """
        Step 1: Voice → Text Agent
        Handles voice transcription using Deepgram
        """
        return Agent(
            role="Voice Transcription Specialist",
            goal="Convert audio input to accurate text using Deepgram API",
            backstory="""You are an expert in speech recognition and audio processing. 
            Your job is to accurately transcribe user voice input into clean, readable text 
            that can be processed by the intent analysis system.""",
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            tools=[],  # Will use voice service directly
            llm=self.llms['intent']  # Use intent LLM for voice processing
        )
    
    def intent_analysis_agent(self):
        """
        Step 2: Text → Schema JSON Agent
        Converts transcribed text to complete schema JSON
        """
        return Agent(
            role="User Intent Analyst",
            goal=(
                "Accurately understand every detail of the user's shopping request. "
                "Your final answer MUST be a structured JSON object that extracts all relevant "
                "attributes like product type, color, occasion, and style based on the user's text."
            ),
            backstory=(
                "You are an expert in understanding fashion and shopping-related language. "
                "Your sole purpose is to translate unstructured user requests into a precise, "
                "structured JSON format that a database search system can directly use. "
                "You must use the 'User Intent Analyzer' tool to perform this translation. "
                "Do not add any conversational text to your final answer; it must only be the JSON object."
            ),
            # The agent has access to our custom tool
            tools=[intent_analyzer_tool],
            verbose=True, # Set to True to see the agent's thought process
            allow_delegation=False,
            llm=self.llms['intent']  # Use dedicated API key for intent analysis
        )
    
    def database_search_agent(self):
        """
        Step 3: Schema → Product Results Agent
        Directly uses JSON schema as MongoDB query filter
        """
        return Agent(
            role="Direct Database Query Executor",
            goal="Use the JSON schema directly as a MongoDB query filter to find matching products",
            backstory="""You are a MongoDB query specialist who takes JSON schemas 
            from the intent analysis and uses them directly as database filters. 
            You understand how to map schema fields to MongoDB query operators like 
            $in for arrays, $lt/$gt for price ranges, and direct equality for simple fields.""",
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            tools=[],  # No tools needed - direct query execution
            llm=self.llms['search']  # Use dedicated API key for search
        )
    
    def response_generation_agent(self):
        """
        Step 4: Products → Natural Language Response Agent
        Converts product results into friendly shopping assistant response
        """
        return Agent(
            role="Shopping Assistant Response Generator",
            goal="Create natural, helpful responses based on product search results",
            backstory="""You are a friendly shopping assistant who helps customers 
            find products. You present search results in an engaging, helpful way 
            and offer suggestions when needed.""",
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            tools=[],
            llm=self.llms['response']  # Use dedicated API key for responses
        )
