import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from crewai.tools import BaseTool
import os

# --- Optimized Initialization ---
# This setup ensures the expensive model loading and embedding calculations
# only happen once when the application starts, not every time the tool is used.

# Suppress a harmless warning from the sentence-transformers library
#os.environ["TOKENIZERS_PARALLELISM"] = "false"

print("INTENT_TOOL: Loading sentence transformer model...")
# Load a pre-trained model optimized for semantic similarity.
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
print("INTENT_TOOL: Model loaded.")

# --- Define all possible values from your database schema ---
DB_SCHEMA = {
    'gender': ['men', 'women', 'boys', 'girls'],
    'type': ['bottomwear', 'ethnicwear', 'topwear', 'winterwear'],
    'category': [
        'Casual', 'Dresses', 'Ethnic Wear', 'Formal', 'Hoodies', 'Jackets',
        'Nightwear', 'Outdoor', 'Sports', 'T-Shirts'
    ],
    'pattern': ['floral', 'printed', 'solid', 'striped'],
    'occasion': [
        'traditional', 'summer', 'college', 'beach', 'daily', 'play',
        'date', 'party', 'vacation', 'dinner', 'brunch', 'casual',
        'formal', 'meeting', 'outdoor', 'trekking', 'evening', 'office',
        'business', 'professional', 'school', 'celebration', 'club',
        'festival', 'night', 'home', 'wedding', 'picnic', 'winter'
    ],
    'colors': [
        'green', 'red', 'grey', 'multicolor', 'white', 'blue',
        'purple', 'peach', 'navy', 'pink', 'yellow', 'maroon', 'black'
    ],
    'tags': [
        'checkered', 'nightwear', 'dinner', 'denim', 'black', 'lace',
        'party', 'summer', 'jeans', 'pink', 'purple', 'business', 'navy',
        'jacket', 'polo', 'casual', 'palazzo', 'dress', 'printed',
        'velvet', 'chiffon', 'graphic', 'grey', 'elegant', 'striped',
        'embroidered', 'girls', 'sports', 'shorts', 'winter', 'peach',
        'pinstripe', 'comfortable', 'shirt', 'leather', 'pants',
        'princess', 'pajama', 'green', 'weekend', 'butterfly', 'floral',
        'kurti', 'solid', 'unicorn', 'kids', 'tshirt', 'mirror', 'ethnic',
        'office', 'blue', 'cartoon', 'little', 'rainbow', 'utility',
        'formal', 'outdoor', 'polka', 'cargo', 'cute', 'embroidery',
        'white', 'colorful', 'festival', 'superhero', 'sequin', 'block',
        'pencil', 'blouse', 'warm', 'cotton', 'silk', 'flower', 'school',
        'blazer', 'daily', 'boys', 'hoodie', 'wedding', 'red', 'track', 'linen'
    ]
}

# --- Pre-compute embeddings for all database values for maximum efficiency ---
print("INTENT_TOOL: Pre-computing database schema embeddings...")
DB_EMBEDDINGS = {
    key: MODEL.encode(values) for key, values in DB_SCHEMA.items()
}
print("INTENT_TOOL: Embeddings computed successfully.")


class IntentAnalysisTool(BaseTool):
    name: str = "User Intent Analyzer"
    description: str = (
        "Analyzes a user's shopping query to extract key attributes "
        "like color, occasion, style, etc. It returns a structured JSON object "
        "that can be used to filter a product database. This is the primary tool "
        "for understanding customer needs."
    )

    def _run(self, user_prompt: str) -> dict:
        """
        The core logic of the tool. It takes the user's raw text and converts it to a
        structured dictionary of search filters.
        """
        similarity_threshold = 0.55
        prompt_tokens = user_prompt.lower().replace(',', '').replace('.', '').split()

        if not prompt_tokens:
            return {}

        intent_json = {}
        token_embeddings = MODEL.encode(prompt_tokens)

        for i, token in enumerate(prompt_tokens):
            token_embedding = token_embeddings[i:i+1]

            for key, db_values in DB_SCHEMA.items():
                db_embeddings = DB_EMBEDDINGS[key]
                similarities = cosine_similarity(token_embedding, db_embeddings)
                best_match_index = np.argmax(similarities)
                best_match_score = similarities[0, best_match_index]

                if best_match_score >= similarity_threshold:
                    matched_value = db_values[best_match_index]
                    if key not in intent_json:
                        intent_json[key] = set()
                    intent_json[key].add(matched_value)

        return {key: list(values) for key, values in intent_json.items()}
    
intent_analyzer_tool = IntentAnalysisTool()