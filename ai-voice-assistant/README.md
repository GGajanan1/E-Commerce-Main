# AI Voice Shopping Assistant

An intelligent voice-based shopping assistant powered by CrewAI agents, designed for e-commerce applications.

## Features

- **Voice Transcription**: Uses Deepgram API for accurate speech-to-text conversion
- **Intent Recognition**: Analyzes user queries to extract shopping intent and parameters
- **Product Search**: Searches MongoDB database for products matching user requirements
- **Multi-Agent Workflow**: Uses CrewAI to orchestrate multiple specialized agents
- **Schema-Compliant**: All tools return data matching the exact database schema

## Architecture

### Agents
- **Intent Agent**: Extracts shopping intent and parameters from user speech
- **Product Query Agent**: Searches database for matching products
- **Coordinator Agent**: Orchestrates the workflow and provides final response

### Tools
- **DeepgramTranscriptionTool**: Converts voice to text
- **IntentAnalysisTool**: Analyzes user intent and extracts parameters
- **ParameterExtractionTool**: Maps user queries to database schema
- **ProductSearchTool**: Searches MongoDB for products

## Setup

1. **Create virtual environment**
   ```bash
   python -m venv ai_voice_env
   source ai_voice_env/bin/activate  # On Windows: ai_voice_env\Scripts\activate
   ```

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file with:
   ```env
   DEEPGRAM_API_KEY=your_deepgram_key
   MONGO_URI=your_mongodb_connection_string
   GEMINI_API_KEY_1=your_gemini_key_1
   GEMINI_API_KEY_2=your_gemini_key_2
   ```

## Usage

### Configuration
- Agents: `src/config/agents.yaml`
- Tasks: `src/config/tasks.yaml`
- Tools: `src/config/tools.yaml`
- Main config: `src/config/config.yaml`


## Example Queries

- "I have a date tonight, give me something more special dresses"
- "Show me blue jeans for men"
- "Find formal shirts for office wear"

## API Keys Required

- **Deepgram**: For voice transcription
- **Google Gemini**: For AI agent reasoning (multiple keys for rate limiting)
- **MongoDB**: For product database

