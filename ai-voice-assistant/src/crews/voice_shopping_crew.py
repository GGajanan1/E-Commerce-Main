"""
Voice Shopping Crew
Main CrewAI orchestrator for the 4-step voice shopping pipeline
"""

import os
import logging
from crewai import Crew, Process
from src.agents.voice_shopping_agents import VoiceShoppingAgents
from src.tasks.voice_shopping_tasks import VoiceShoppingTasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceShoppingCrew:
    """
    Main CrewAI crew for the 4-step voice shopping assistant
    """
    
    def __init__(self):
        """Initialize the crew with agents and tasks"""
        self.agent_factory = VoiceShoppingAgents()
        self.task_factory = VoiceShoppingTasks()
        
        # Create the 3 main agents (skipping transcription for text input)
        self.agents = {
            'intent': self.agent_factory.intent_analysis_agent(),
            'search': self.agent_factory.database_search_agent(),
            'response': self.agent_factory.response_generation_agent()
        }
        
        logger.info("Voice Shopping Crew initialized with 3 agents")
    
    def process_text_request(self, text_input: str) -> str:
        """
        Process a text shopping request through the 3-step pipeline
        
        Args:
            text_input: User's text input (e.g., "I need red dresses for a party")
            
        Returns:
            Final natural language response for the user
        """
        logger.info(f"Processing text request: {text_input}")
        
        try:
            # Create the sequential task workflow
            tasks = self.task_factory.create_sequential_workflow(
                self.agents, 
                text_input
            )
            
            # Create and run the crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,  # Linear 3-step process
                verbose=True,
                memory=False,  # Keep it simple
                max_rpm=30
            )
            
            # Execute the crew with error handling
            try:
                result = crew.kickoff()
                logger.info("Voice shopping pipeline completed successfully")
                return str(result)
            except Exception as crew_error:
                logger.error(f"Crew execution failed: {crew_error}")
                # Try with a simpler approach
                return self._fallback_simple_response(text_input)
                
        except Exception as e:
            logger.error(f"Voice shopping pipeline failed: {e}")
            return self._fallback_simple_response(text_input)
    
    def _fallback_simple_response(self, text_input: str) -> str:
        """Fallback response when crew fails"""
        return f"I understand you're looking for products related to '{text_input}'. " \
               f"Let me help you find what you need. Please try your search again or " \
               f"contact our support team for assistance."
    
    def quick_test(self, test_input: str = "I need red dresses for a party"):
        """
        Quick test of the voice shopping pipeline
        """
        print("🎤 Voice Shopping Assistant - CrewAI Test")
        print("=" * 50)
        print(f"Input: '{test_input}'")
        print("-" * 50)
        
        result = self.process_text_request(test_input)
        
        print(f"Output: {result}")
        print("=" * 50)
        
        return result

# Main execution
if __name__ == "__main__":
    # Create and test the crew
    crew = VoiceShoppingCrew()
    
    # Run test cases
    test_cases = [
        "I need red dresses for a party",
        "Show me blue jeans for men",
        "Find black jackets for women"
    ]
    
    for test_case in test_cases:
        print(f"\\n🧪 Testing: {test_case}")
        crew.quick_test(test_case)
