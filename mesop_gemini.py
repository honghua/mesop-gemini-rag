import os
import time
from PIL import Image
import mesop as me
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Google API key from the environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Define default values for generation parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 512
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.95

@me.stateclass
class State:
    input: str
    output: str
    in_progress: bool

@me.page(path="/chatbot")
def page():
    with me.box(
        style=me.Style(
            background="#fff",
            min_height="calc(100% - 48px)",
            padding=me.Padding(bottom=16),
        )
    ):
        with me.box(
            style=me.Style(
                width="min(720px, 100%)",
                margin=me.Margin.symmetric(horizontal="auto"),
                padding=me.Padding.symmetric(
                    horizontal=16,
                ),
            )
        ):
            header_text()
            chat_input()
            output()
    footer()

def header_text():
    with me.box(
        style=me.Style(
            padding=me.Padding(
                top=64,
                bottom=36,
            ),
        )
    ):
        me.text(
            "Mesop Chatbot",
            style=me.Style(
                font_size=36,
                font_weight=700,
                background="linear-gradient(90deg, #4285F4, #AA5CDB, #DB4437) text",
                color="transparent",
            ),
        )

def chat_input():
    state = me.state(State)
    with me.box(
        style=me.Style(
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
            border=me.Border.all(
                me.BorderSide(width=0, style="solid", color="black")
            ),
            border_radius=12,
            box_shadow="0 10px 20px #0000000a, 0 2px 6px #0000000a, 0 0 1px #0000000a",
        )
    ):
        with me.box(
            style=me.Style(
                flex_grow=1,
            )
        ):
            me.native_textarea(
                value=state.input,
                autosize=True,
                min_rows=4,
                placeholder="Enter your prompt",
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    background="white",
                    outline="none",
                    width="100%",
                    overflow_y="auto",
                    border=me.Border.all(
                        me.BorderSide(style="none"),
                    ),
                ),
                on_blur=textarea_on_blur,
            )
        with me.content_button(type="icon", on_click=click_send):
            me.icon("send")

def textarea_on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.input = e.value

def click_send(e: me.ClickEvent):
    state = me.state(State)
    if not state.input:
        return
    state.in_progress = True
    input_text = state.input
    state.input = ""
    state.output = ""  # Clear previous output
    yield

    for chunk in call_api(input_text):
        state.output += chunk
        yield
    state.in_progress = False
    yield

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

def output():
    state = me.state(State)
    if state.output or state.in_progress:
        with me.box(
            style=me.Style(
                background="#F0F4F9",
                padding=me.Padding.all(16),
                border_radius=16,
                margin=me.Margin(top=36),
            )
        ):
            if state.output:
                me.markdown(state.output)
            if state.in_progress:
                with me.box(style=me.Style(margin=me.Margin(top=16))):
                    me.progress_spinner()

def footer():
    with me.box(
        style=me.Style(
            position="sticky",
            bottom=0,
            padding=me.Padding.symmetric(vertical=16, horizontal=16),
            width="100%",
            background="#F0F4F9",
            font_size=14,
        )
    ):
        me.html(
            "Made with <a href='https://google.github.io/mesop/'>Mesop</a>",
        )
