import gradio as gr
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure your Google API key
# GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def preprocess_stop_sequences(stop_sequences):
    # Implement any preprocessing needed for stop sequences
    return stop_sequences

def preprocess_image(image):
    # Implement any preprocessing needed for images
    return image

def chat(
    user_input,
    chatbot,
    files,
    google_key,
    temperature=0.7,
    max_output_tokens=512,
    top_k=40,
    top_p=0.95,
    stop_sequences=None
):
    # Configure the API key
    genai.configure(api_key=google_key if google_key else GOOGLE_API_KEY)

    # Set up generation configuration
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        stop_sequences=preprocess_stop_sequences(stop_sequences=stop_sequences) if stop_sequences else [],
        top_k=top_k,
        top_p=top_p
    )

    # Prepare text and image prompts
    text_prompt = [user_input] if user_input else []
    image_prompt = [preprocess_image(Image.open(file).convert('RGB')) for file in files] if files else []
    
    # Select the appropriate model
    model_name = 'gemini-pro-vision' if files else 'gemini-pro'
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
        
        google_key_input = gr.Textbox(label="Google API Key", type="password")
        
        chatbot = gr.Chatbot()
        user_input = gr.Textbox(label="Your Message")
        files_input = gr.File(file_count="multiple", label="Upload Images (Optional)")
        
        with gr.Row():
            temperature_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature")
            max_tokens_slider = gr.Slider(1, 2048, value=512, step=1, label="Max Output Tokens")
        
        with gr.Row():
            top_k_slider = gr.Slider(0, 100, value=40, step=1, label="Top K")
            top_p_slider = gr.Slider(0.0, 1.0, value=0.95, label="Top P")
        
        stop_sequences_input = gr.Textbox(label="Stop Sequences (Comma-separated)", placeholder="e.g., 'Stop', 'End'")
        
        submit_button = gr.Button("Send")
        
        def on_submit(*args):
            return chat(*args)
        
        submit_button.click(
            on_submit,
            inputs=[
                user_input,
                chatbot,
                files_input,
                google_key_input,
                temperature_slider,
                max_tokens_slider,
                top_k_slider,
                top_p_slider,
                stop_sequences_input
            ],
            outputs=chatbot
        )
        
        gr.Markdown("### Instructions")
        gr.Markdown("""
            - Enter your message and optionally upload images to get a response from the model.
            - Adjust the parameters like Temperature, Max Output Tokens, Top K, and Top P to control the generation.
            - Provide stop sequences if you want the model to stop generating upon encountering specific phrases.
        """)
        
    demo.launch()

if __name__ == "__main__":
    main()
