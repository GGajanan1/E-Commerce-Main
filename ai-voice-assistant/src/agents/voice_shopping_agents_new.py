"""
4-Step Voice Shopping Agents
Clean CrewAI agents for the linear pipeline with distributed API keys
"""

import os
from crewai import Agent, LLM
from src.tools.schema_intent_tool import intent_analyzer_tool
from src.tools.direct_mongodb_query_tool import direct_mongodb_query_tool
from src.services.api_key_manager import APIKeyManager, ProviderType

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
        
        # Create LLM instances for each agent
        self.llms = {
            'intent': LLM(
                model="gemini/gemini-2.0-flash",
                api_key=self.agent_keys['intent']
            ),
            'search': LLM(
                model="gemini/gemini-2.0-flash", 
                api_key=self.agent_keys['search']
            ),
            'response': LLM(
                model="gemini/gemini-2.0-flash",
                api_key=self.agent_keys['response']
            )
        }
        
        print(f"🔑 Agent Key Distribution:")
        print(f"  Intent Agent: ...{self.agent_keys['intent'][-10:]}")
        print(f"  Search Agent: ...{self.agent_keys['search'][-10:]}")
        print(f"  Response Agent: ...{self.agent_keys['response'][-10:]}")
    
    def _get_agent_key(self, agent_name: str) -> str:
        """Get a specific API key for an agent"""
        api_key = self.api_key_manager.get_available_key(ProviderType.GEMINI, agent_name)
        if not api_key:
            # Fallback to environment variable if key manager fails
            return os.getenv("GEMINI_API_KEY_2", os.getenv("GEMINI_API_KEY_1"))
        return api_key
    
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
            tools=[]  # Will use voice service directly
        )
    
    def intent_analysis_agent(self):
        """
        Step 2: Text → Schema JSON Agent
        Converts transcribed text to complete schema JSON
        """
        return Agent(
            role="Shopping Intent Analyzer",
            goal="Convert user text to complete product schema JSON that can be used directly as MongoDB query filter",
            backstory="""You are an expert at understanding shopping requests and 
            extracting structured information. You analyze user text and return a 
            complete JSON schema that can be directly used as a MongoDB query filter.
            Your output must be a valid JSON object with fields that match the database structure.""",
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            tools=[intent_analyzer_tool],
            llm=self.llms['intent']  # Use dedicated API key for intent analysis
        )
    
    def database_search_agent(self):
        """
        Step 3: JSON Schema → Product Results Agent
        Uses JSON schema directly as MongoDB query filter
        """
        return Agent(
            role="Direct MongoDB Query Executor",
            goal="Take JSON schema from intent analysis and use it directly as MongoDB query filter to find products",
            backstory="""You are a MongoDB query specialist who takes JSON schemas 
            from the intent analysis and uses them directly as database query filters. 
            You understand how to map schema fields to MongoDB query operators like 
            $in for arrays, $lt/$gt for price ranges, and direct equality for simple fields.
            
            Example usage:
            - User says: "Show me blue t-shirts"
            - Intent JSON: {"category": "t-shirt", "colors": "blue"}
            - MongoDB Query: {"category": "t-shirt", "colors": "blue"}
            
            You execute the query and return matching products.""",
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            tools=[direct_mongodb_query_tool],
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
