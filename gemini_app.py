import os
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Google API key from the environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Define default values for generation parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 512
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.95

def preprocess_image(image):
    # Implement any preprocessing needed for images
    return image

def chat(
    user_input,
    chatbot,
    files
):
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

    # Prepare text and image prompts
    text_prompt = [user_input] if user_input else []
    image_prompt = [preprocess_image(Image.open(file).convert('RGB')) for file in files] if files else []
    
    # Select the appropriate model
    model_name = 'gemini-1.5-flash' if files else 'gemini-pro'
    model = genai.GenerativeModel(model_name)

    # Generate response from the model
    response = model.generate_content(
        text_prompt + image_prompt,
        stream=True,
        generation_config=generation_config
    )

    # Process and return the response
    answer = ""
    for message in response:
        answer += message.text
    chatbot.append((user_input, answer))
    return chatbot

# Create Gradio interface
def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Chat with Google Gemini")
        
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(label="Your Message")
        files_input = gr.File(file_count="multiple", label="Upload Images (Optional)")
        
        submit_button = gr.Button("Send")
        
        def on_submit(*args):
            return chat(*args)
        
        submit_button.click(
            on_submit,
            inputs=[
                user_input,
                chatbot,
                files_input
            ],
            outputs=chatbot
        )
        
        gr.Markdown("### Instructions")
        gr.Markdown("""
            - Enter your message and optionally upload images to get a response from the model.
        """)
        
    demo.launch()

if __name__ == "__main__":
    main()
