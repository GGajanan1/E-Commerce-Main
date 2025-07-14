"""
Voice Shopping Tasks
Defines the 3-step sequential tasks for the CrewAI workflow
"""

from crewai import Task
from typing import Dict, Any

class VoiceShoppingTasks:
    """Factory for creating the 3-step pipeline tasks"""
    
    def create_sequential_workflow(self, agents: Dict[str, Any], input_text: str) -> list:
        """
        Create the sequential 3-step task workflow
        
        Args:
            agents: Dictionary of agent instances
            input_text: User input text
            
        Returns:
            List of sequential tasks
        """
        
        # Task 1: Intent Analysis (Text → Schema JSON)
        intent_task = Task(
            description=f"""
            Analyze the user input and convert it to a complete product schema JSON.
            
            User input: "{input_text}"
            
            Convert this text to a complete JSON schema with all fields:
            - intent_type, type, category, gender, colors, sizes, pattern, occasion, 
              material, brand, price_min, price_max, description, tags, limit
            
            Set unrecognized fields to null (not the string "null", but actual null/None values). 
            Always return valid JSON.
            """,
            agent=agents['intent'],
            expected_output="Complete JSON schema with all product fields"
        )
        
        # Task 2: Database Search (Schema → Products)
        search_task = Task(
            description="""
            You will receive a JSON schema from the previous task. Parse this schema and use it to search for products.
            
            CRITICAL INSTRUCTIONS:
            1. The previous task output contains a JSON schema - extract it carefully
            2. Parse the JSON to get: colors, type, category, gender, occasion, etc.
            3. Use the RealProductSearchTool with these extracted parameters
            4. Pass the schema_json parameter containing the full JSON from the previous task
            5. Do NOT search with empty filters - use the actual schema data
            
            Example: If the schema has {"colors": ["red"], "type": "dress", "gender": "women"}, 
            make sure those exact filters are applied to find red dresses for women.
            
            Always call the tool with the schema_json parameter set to the full JSON from the intent task.
            """,
            agent=agents['search'],
            expected_output="List of matching products from database with proper filtering applied based on the schema",
            context=[intent_task]  # Depends on intent task output
        )
        
        # Task 3: Response Generation (Products → Natural Language)
        response_task = Task(
            description="""
            Generate a natural, helpful response based on the found products.
            
            Create a conversational response that:
            - Acknowledges the user's request
            - Presents the found products in an appealing way
            - Includes relevant product details (colors, prices, etc.)
            - Offers helpful suggestions or alternatives if few results
            
            Make it sound natural and helpful, like a friendly shopping assistant.
            """,
            agent=agents['response'],
            expected_output="Natural language response for the user",
            context=[search_task]  # Depends on search task output
        )
        
        return [intent_task, search_task, response_task]
