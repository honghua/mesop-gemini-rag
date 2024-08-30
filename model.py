import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Google API key from the environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Define default values for generation parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 512
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.95

class Model:
    @staticmethod
    def call_api(input_text):
        # Configure the API key
        genai.configure(api_key=GOOGLE_API_KEY)

        # Set up generation configuration with default values
        generation_config = genai.types.GenerationConfig(
            temperature=DEFAULT_TEMPERATURE,
            max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS,
            stop_sequences=[],  # No stop sequences by default
            top_k=DEFAULT_TOP_K,
            top_p=DEFAULT_TOP_P
        )

        # Prepare text prompt
        text_prompt = [input_text] if input_text else []
        
        # Select the appropriate model (only text-based in this case)
        model_name = 'gemini-pro'
        model = genai.GenerativeModel(model_name)

        # Generate response from the model
        response = model.generate_content(
            text_prompt,
            stream=True,
            generation_config=generation_config
        )

        # Yield response chunks
        for message in response:
            yield message.text